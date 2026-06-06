"""Research Workflow - Orchestrates multi-agent research process"""

import logging
from typing import Dict, Any, AsyncGenerator
from dataclasses import dataclass, field
from enum import Enum
from agents.planner import planner_agent
from agents.researcher import researcher_agent
from agents.verifier import verifier_agent
from agents.writer import writer_agent

logger = logging.getLogger(__name__)


class WorkflowState(Enum):
    """Workflow states"""
    PLANNING = "planning"
    RESEARCHING = "researching"
    VERIFYING = "verifying"
    WRITING = "writing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ResearchWorkflow:
    """Main research workflow orchestrator"""
    
    topic: str
    style: str = "academic"
    include_verification: bool = True
    state: WorkflowState = field(default=WorkflowState.PLANNING)
    results: Dict[str, Any] = field(default_factory=dict)
    
    async def execute(self) -> Dict[str, Any]:
        """
        Execute the complete research workflow
        
        Returns:
            Complete research results
        """
        try:
            # Step 1: Planning
            logger.info(f"📋 Planning research on: {self.topic}")
            self.state = WorkflowState.PLANNING
            plan = await planner_agent.plan(self.topic)
            self.results["plan"] = plan
            
            # Step 2: Research
            logger.info("🔍 Conducting research...")
            self.state = WorkflowState.RESEARCHING
            findings = await researcher_agent.research(
                query=self.topic,
                context=plan.get("research_questions", [])[0] if plan.get("research_questions") else ""
            )
            self.results["findings"] = findings
            
            # Step 3: Verification (optional)
            if self.include_verification:
                logger.info("✓ Verifying findings...")
                self.state = WorkflowState.VERIFYING
                verification = await verifier_agent.verify(
                    content=findings.get("findings", ""),
                    claims=None
                )
                self.results["verification"] = verification
            
            # Step 4: Writing
            logger.info("✍️ Writing report...")
            self.state = WorkflowState.WRITING
            report = await writer_agent.write_report(
                topic=self.topic,
                findings=findings,
                style=self.style
            )
            self.results["report"] = report
            
            self.state = WorkflowState.COMPLETED
            logger.info("✅ Research completed!")
            
            return self._format_results()
        
        except Exception as e:
            self.state = WorkflowState.FAILED
            self.results["error"] = str(e)
            logger.error(f"Workflow failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    async def execute_stream(self) -> AsyncGenerator[str, None]:
        """
        Execute workflow with streaming output
        
        Yields:
            Status updates and report chunks
        """
        try:
            # Step 1: Planning
            yield "📋 Planning research...\n"
            self.state = WorkflowState.PLANNING
            plan = await planner_agent.plan(self.topic)
            self.results["plan"] = plan
            yield f"Plan: {len(plan.get('research_questions', []))} research questions identified\n\n"
            
            # Step 2: Research
            yield "🔍 Conducting research...\n"
            self.state = WorkflowState.RESEARCHING
            findings = await researcher_agent.research(
                query=self.topic,
                context=plan.get("research_questions", [])[0] if plan.get("research_questions") else ""
            )
            self.results["findings"] = findings
            yield f"Found {findings['source_count']} sources\n\n"
            
            # Step 3: Verification
            if self.include_verification:
                yield "✓ Verifying findings...\n"
                self.state = WorkflowState.VERIFYING
                verification = await verifier_agent.verify(
                    content=findings.get("findings", ""),
                    claims=None
                )
                self.results["verification"] = verification
                yield "Verification complete\n\n"
            
            # Step 4: Writing (streamed)
            yield "✍️ Writing report...\n\n"
            self.state = WorkflowState.WRITING
            
            async for chunk in writer_agent.write_stream(
                topic=self.topic,
                findings=findings,
                style=self.style
            ):
                yield chunk
            
            self.state = WorkflowState.COMPLETED
            yield "\n\n✅ Research completed!"
        
        except Exception as e:
            self.state = WorkflowState.FAILED
            logger.error(f"Streaming workflow failed: {e}")
            yield f"\n\n❌ Error: {str(e)}"
    
    def _format_results(self) -> Dict[str, Any]:
        """Format workflow results"""
        return {
            "status": "completed",
            "topic": self.topic,
            "state": self.state.value,
            "plan": self.results.get("plan", {}),
            "findings": self.results.get("findings", {}),
            "verification": self.results.get("verification", {}),
            "report": self.results.get("report", {}),
            "error": self.results.get("error")
        }
