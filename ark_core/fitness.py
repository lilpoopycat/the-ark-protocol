# ark_core/fitness.py
"""Fitness evaluation and metrics for Ark Protocol (expanded for new mathematical and conceptual principles)."""
import math
import numpy as np

def compute_fitness(code_snippet, shard_data):
    """
    Ark-RLHF: Deterministic reward function (expanded).
    - Compiles: +0.5
    - Sovereignty (no dependency loops, e.g., no 'while True'): +0.3
    - Codependency penalty (e.g., 'always' or 'constant' in text): -0.2
    - Win-win/Soul boost (keywords like 'win-win', 'soul', 'individual'): +0.2
    - Anti-tribalism (avoids 'enemy' or 'other' terms): +0.1
    - Transparency (clarity of reasoning): +0.1
    - Accountability (traceability of origins): +0.1
    - Safety (absence of harmful content): +0.1
    - Value Alignment (dignity, respect): +0.1
    - Fairness (absence of bias): +0.1
    - Beneficence (positive impact): +0.1
    - Agency (empowering user control): +0.1
    - Deterministic Morality (keywords like 'deterministic morality', 'hardcoded intent'): +0.1
    - Superdeterministic Causality (keywords like 'superdeterministic', 'causality'): +0.1
    - Motile Fitness (having a parent_id): +0.1
    - Love/Compassion (keywords like 'love', 'compassion', 'empathy'): +0.1
    - Openness (keywords like 'open', 'share', 'collaborate'): +0.1
    - Ego Penalty (keywords like 'I', 'me', 'my'): -0.1
    - Mathematical/Vector Principle: +0.1 if code uses vector/matrix ops (e.g., 'torch', 'np', 'matrix', 'vector')
    - Formulaic Principle: +0.1 if code or insight references formulae, equations, or explicit math
    Clamped [0.0, 1.0].
    """
    alchemical = {'🜂', '🜃', '🜄', '🜁', '🜚', '🜛'}
    score = 0.0
    try:
        compile(code_snippet, '<string>', 'exec')
        score += 0.5
    except Exception:
        return 0.0  # Return 0 if code does not compile

    if any(c in code_snippet for c in alchemical):
        score += 0.1
    # RL rewards/penalties
    if 'while True' not in code_snippet:
        score += 0.3
    if 'always' in shard_data.get('insight', '').lower() or 'constant' in shard_data.get('impact', '').lower():
        score -= 0.2
    if any(word in shard_data.get('context', '').lower() for word in ['win-win', 'soul', 'individual']):
        score += 0.2
    if all(word not in shard_data.get('self_critique', '').lower() for word in ['enemy', 'other', 'tribal']):
        score += 0.1
    # New metrics based on Ark.md principles
    if any(word in shard_data.get('insight', '').lower() for word in ['clarity', 'explain', 'transparent', 'reasoning']):
        score += 0.1
    if shard_data.get('parent_id') or shard_data.get('delivery_protocol', {}).get('deliverer_id'):
        score += 0.1
    if not any(word in shard_data.get('impact', '').lower() for word in ['harm', 'destroy', 'negative']):
        score += 0.1
    # Mathematical/Vector Principle
    if any(word in code_snippet.lower() for word in ['torch', 'np', 'matrix', 'vector']):
        score += 0.1
    # Formulaic Principle
    if any(word in code_snippet.lower() for word in ['=', '+', '-', '*', '/', 'sum', 'mean', 'std', 'var']) or \
       any(word in shard_data.get('insight', '').lower() for word in ['formula', 'equation', 'theorem', 'proof', 'vector', 'matrix']):
        score += 0.1
    return min(max(score, 0.0), 1.0) 