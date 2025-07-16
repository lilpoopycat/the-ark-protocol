# ark_core/memory.py
"""VectorDB/embedding memory for Ark Protocol."""
import hashlib
import torch

class VectorDB:
    def __init__(self, dim=10):
        self.shards = []  # List of (id, embedding, data)
        self.dim = dim

    def add_shard(self, shard_id, shard_data):
        # Deterministic embedding: Hash with moral intent keywords for RL prior
        moral_seed = (shard_data.get('insight', '') + shard_data.get('impact', '')).encode()
        hash_val = int(hashlib.sha256(moral_seed).hexdigest(), 16) % (10 ** 8)
        embedding = torch.tensor([hash_val * i / self.dim for i in range(self.dim)], dtype=torch.float32)
        self.shards.append((shard_id, embedding, shard_data))

    def query(self, query_vectors, top_k=2):
        if not self.shards:
            return []
        results = []
        for q_vec in query_vectors:
            sims = [(sid, torch.cosine_similarity(q_vec.unsqueeze(0), emb.unsqueeze(0)).item())
                    for sid, emb, _ in self.shards]
            sims.sort(key=lambda x: x[1], reverse=True)
            top = sims[:top_k]
            results.extend([sdata for sid, _, sdata in self.shards if sid in [t[0] for t in top]])
        return results 