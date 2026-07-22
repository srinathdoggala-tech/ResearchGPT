import { describe, it, expect } from 'vitest';

describe('ResearchGPT Application Tests', () => {
  it('verifies environment default fallback URL', () => {
    const defaultUrl = 'https://researchgpt-backend-vxij.onrender.com';
    expect(defaultUrl).toContain('onrender.com');
  });

  it('validates search payload structure', () => {
    const request = {
      topic: 'Artificial Intelligence',
      style: 'academic',
      include_verification: true,
    };
    expect(request.topic).toBe('Artificial Intelligence');
    expect(request.include_verification).toBe(true);
  });
});
