import { useEffect, useRef } from "react";

interface InteractiveBackgroundProps {
  isSearching?: boolean;
  theme?: "dark" | "light";
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  baseAlpha: number;
  color: string;
  pulseSpeed: number;
  pulsePhase: number;
}

const PALETTES = {
  light: [
    "rgba(79, 70, 229, ",   // Indigo
    "rgba(124, 58, 237, ",  // Violet
    "rgba(14, 165, 233, ",  // Sky
    "rgba(99, 102, 241, ",  // Accent Indigo
  ],
  dark: [
    "rgba(99, 102, 241, ",  // Indigo
    "rgba(168, 85, 247, ",  // Purple
    "rgba(56, 189, 248, ",  // Cyan
    "rgba(236, 72, 153, ",  // Pink accent
  ],
};

export default function InteractiveBackground({
  isSearching = false,
  theme = "light",
}: InteractiveBackgroundProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const mouse = {
      x: width / 2,
      y: height / 2,
      targetX: width / 2,
      targetY: height / 2,
      radius: 180,
      active: false,
    };

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    const handleMouseMove = (e: MouseEvent) => {
      mouse.targetX = e.clientX;
      mouse.targetY = e.clientY;
      mouse.active = true;
    };

    const handleMouseLeave = () => {
      mouse.active = false;
    };

    window.addEventListener("resize", handleResize);
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseleave", handleMouseLeave);

    // Create particle network
    const particleCount = Math.min(Math.floor((width * height) / 12000), 80);
    const colors = PALETTES[theme];

    const particles: Particle[] = Array.from({ length: particleCount }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.8,
      vy: (Math.random() - 0.5) * 0.8,
      radius: Math.random() * 2.5 + 1.2,
      baseAlpha: Math.random() * 0.4 + 0.3,
      color: colors[Math.floor(Math.random() * colors.length)],
      pulseSpeed: Math.random() * 0.03 + 0.01,
      pulsePhase: Math.random() * Math.PI * 2,
    }));

    let step = 0;

    const render = () => {
      step++;
      ctx.clearRect(0, 0, width, height);

      // Smooth mouse lerp
      mouse.x += (mouse.targetX - mouse.x) * 0.08;
      mouse.y += (mouse.targetY - mouse.y) * 0.08;

      const speedMultiplier = isSearching ? 2.2 : 1.0;

      // Update & render particles
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        p.x += p.vx * speedMultiplier;
        p.y += p.vy * speedMultiplier;

        // Bounce off canvas boundaries
        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        // Mouse influence / interactive push
        if (mouse.active) {
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < mouse.radius && dist > 0) {
            const force = (1 - dist / mouse.radius) * 1.5;
            p.x += (dx / dist) * force * 2;
            p.y += (dy / dist) * force * 2;
          }
        }

        p.pulsePhase += p.pulseSpeed;
        const currentAlpha =
          p.baseAlpha + Math.sin(p.pulsePhase) * 0.2 * (isSearching ? 1.8 : 1.0);

        // Draw particle node
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius * (isSearching ? 1.3 : 1.0), 0, Math.PI * 2);
        ctx.fillStyle = `${p.color}${Math.max(0.1, Math.min(0.9, currentAlpha))})`;
        ctx.shadowColor = p.color + "0.8)";
        ctx.shadowBlur = isSearching ? 12 : 6;
        ctx.fill();
        ctx.shadowBlur = 0; // Reset shadow

        // Draw connections between nearby nodes
        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          const maxDist = isSearching ? 160 : 130;

          if (dist < maxDist) {
            const connectionAlpha = (1 - dist / maxDist) * 0.25 * (isSearching ? 1.5 : 1.0);
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `${p.color}${Math.min(0.7, connectionAlpha)})`;
            ctx.lineWidth = (1 - dist / maxDist) * 1.2;
            ctx.stroke();
          }
        }

        // Draw line to cursor if in range
        if (mouse.active) {
          const dx = p.x - mouse.x;
          const dy = p.y - mouse.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < mouse.radius) {
            const cursorAlpha = (1 - dist / mouse.radius) * 0.45;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.strokeStyle = `${p.color}${cursorAlpha})`;
            ctx.lineWidth = 1.4;
            ctx.stroke();
          }
        }
      }

      // Draw cursor glow halo
      if (mouse.active) {
        const glowGradient = ctx.createRadialGradient(
          mouse.x,
          mouse.y,
          0,
          mouse.x,
          mouse.y,
          mouse.radius * 0.7
        );
        glowGradient.addColorStop(
          0,
          theme === "dark"
            ? "rgba(129, 140, 248, 0.15)"
            : "rgba(99, 102, 241, 0.12)"
        );
        glowGradient.addColorStop(1, "rgba(99, 102, 241, 0)");

        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, mouse.radius * 0.7, 0, Math.PI * 2);
        ctx.fillStyle = glowGradient;
        ctx.fill();
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseleave", handleMouseLeave);
    };
  }, [isSearching, theme]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none z-0 transition-opacity duration-700"
      style={{ opacity: 0.9 }}
    />
  );
}
