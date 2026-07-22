"""API Routes - RESTful endpoints for ResearchGPT"""

import json
import logging
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from graph.workflow import ResearchWorkflow
from agents.planner import planner_agent
from agents.researcher import researcher_agent
from agents.verifier import verifier_agent
from agents.writer import writer_agent

logger = logging.getLogger(__name__)
router = APIRouter(tags=["research"])


class ResearchRequest(BaseModel):
    """Research request model"""
    topic: str
    style: str = "academic"
    include_verification: bool = True


class ResearchResponse(BaseModel):
    """Research response model"""
    status: str
    topic: str
    plan: dict
    findings: dict
    verification: Optional[dict] = None
    report: dict


@router.post("/research")
async def research(request: ResearchRequest):
    """
    Execute complete research workflow
    
    Args:
        request: ResearchRequest with topic and options
    
    Returns:
        Complete research results
    """
    try:
        logger.info(f"Starting research for: {request.topic}")
        workflow = ResearchWorkflow(
            topic=request.topic,
            style=request.style,
            include_verification=request.include_verification
        )
        
        results = await workflow.execute()
        logger.info(f"Research completed for: {request.topic}")
        return results
    
    except Exception as e:
        logger.error(f"Research failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/research/stream")
async def research_stream(request: ResearchRequest):
    """
    Execute research workflow with streaming output
    
    Args:
        request: ResearchRequest with topic and options
    
    Returns:
        Server-sent events stream with research updates
    """
    async def generate():
        try:
            logger.info(f"Starting streaming research for: {request.topic}")
            workflow = ResearchWorkflow(
                topic=request.topic,
                style=request.style,
                include_verification=request.include_verification
            )
            
            async for chunk in workflow.execute_stream():
                if isinstance(chunk, dict):
                    yield f"data: {json.dumps(chunk)}\n\n"
                else:
                    yield f"data: {json.dumps({'type': 'report', 'content': chunk})}\n\n"
        
        except Exception as e:
            logger.error(f"Streaming research failed: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/research/quick")
async def quick_research(
    topic: str = Query(..., description="Research topic"),
    max_results: int = Query(5, ge=1, le=20, description="Maximum search results")
):
    """
    Quick research without verification
    
    Args:
        topic: Research topic
        max_results: Maximum results to return
    
    Returns:
        Quick research findings
    """
    try:
        logger.info(f"Quick research for: {topic}")
        findings = await researcher_agent.research(query=topic)
        
        return {
            "status": "success",
            "topic": topic,
            "findings": findings["findings"],
            "source_count": findings["source_count"],
            "sources": findings["sources"][:max_results]
        }
    
    except Exception as e:
        logger.error(f"Quick research failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/plan")
async def plan_research(topic: str = Query(..., description="Research topic")):
    """
    Get research plan for a topic
    
    Args:
        topic: Research topic
    
    Returns:
        Research plan with questions and steps
    """
    try:
        logger.info(f"Planning research for: {topic}")
        plan = await planner_agent.plan(topic)
        return {"status": "success", "plan": plan}
    
    except Exception as e:
        logger.error(f"Planning failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify")
async def verify_content(
    content: str = Query(..., description="Content to verify"),
    claims: Optional[list] = None
):
    """
    Verify research content
    
    Args:
        content: Content to verify
        claims: Specific claims to verify
    
    Returns:
        Verification results
    """
    try:
        logger.info("Verifying content")
        results = await verifier_agent.verify(content=content, claims=claims)
        return {"status": "success", "verification": results}
    
    except Exception as e:
        logger.error(f"Verification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/summarize")
async def summarize_content(
    content: str = Query(..., description="Content to summarize"),
    length: str = Query("medium", pattern="^(short|medium|long)$")
):
    """
    Summarize content
    
    Args:
        content: Content to summarize
        length: Summary length
    
    Returns:
        Summary result
    """
    try:
        logger.info(f"Summarizing content ({length})")
        result = await writer_agent.write_summary(content=content, length=length)
        return {"status": "success", "summary": result}
    
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ResearchGPT API",
        "version": "1.0.0"
    }
