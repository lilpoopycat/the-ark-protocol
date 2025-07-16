# ark_core/fitness.py
"""Fitness evaluation and metrics for Ark Protocol."""

def compute_fitness(code_snippet, shard_data):
    """
    Ark-RLHF: Deterministic reward function.
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
    Clamped [0.0, 1.0].
    Simulates RLHF for human-scale intuition.
    """
    alchemical = {'🜂', '🜃', '🜄', '🜁', '🜚', '🜛'}
    try:
        compile(code_snippet, '<string>', 'exec')
        score = 0.5
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
        if any(word in shard_data.get('context', '').lower() for word in ['dignity', 'respect', 'ethical', 'moral']):
            score += 0.1
        if not any(word in shard_data.get('self_critique', '').lower() for word in ['bias', 'stereotype', 'discriminat']):
            score += 0.1
        if any(word in shard_data.get('impact', '').lower() for word in ['benefit', 'improve', 'positive', 'well-being']):
            score += 0.1
        if any(word in shard_data.get('impact', '').lower() for word in ['control', 'empower', 'options', 'autonomy']):
            score += 0.1
        return min(max(score, 0.0), 1.0)
    except Exception:
        return 0.0 