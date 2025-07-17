# ark_core/memory.py
"""EnhancedVectorDB: Embedding memory for Ark Protocol with advanced vector and formulaic logic."""
import hashlib
import torch
import numpy as np
import networkx as nx

class NetworkLattice:
    """
    Represents the Ark Lattice as a dynamic graph/network.
    Nodes = shards; Edges = semantic/structural links.
    Provides methods for entropy, modularity, and causal emergence proxies.
    """
    def __init__(self):
        self.G = nx.Graph()

    def add_shard(self, shard_id, **attrs):
        self.G.add_node(shard_id, **attrs)

    def add_link(self, shard_id1, shard_id2, weight=1.0, sign=1):
        # sign: +1 for positive (agreement), -1 for negative (antagonism)
        self.G.add_edge(shard_id1, shard_id2, weight=weight, sign=sign)

    def von_neumann_entropy(self):
        # Von Neumann entropy of the normalized Laplacian
        L = nx.normalized_laplacian_matrix(self.G).todense()
        eigvals = np.linalg.eigvalsh(L)
        eigvals = eigvals[eigvals > 0]  # avoid log(0)
        probs = eigvals / eigvals.sum()
        entropy = -np.sum(probs * np.log(probs))
        return float(entropy)

    def modularity(self):
        # Use greedy modularity communities as a proxy for fragmentation/tribalism
        from networkx.algorithms.community import greedy_modularity_communities
        comms = list(greedy_modularity_communities(self.G))
        return nx.algorithms.community.quality.modularity(self.G, comms)

    def basic_causal_emergence_proxy(self):
        # Proxy: difference between global clustering and average local clustering
        global_clust = nx.transitivity(self.G)
        avg_local_clust = nx.average_clustering(self.G)
        return global_clust - avg_local_clust

class EnhancedVectorDB:
    def __init__(self, dim=16):
        self.shards = []  # List of (id, embedding, data)
        self.dim = dim

    def _moral_embedding(self, shard_data):
        # Use more mathematical features: hash, length, and formulaic priors
        moral_text = (shard_data.get('insight', '') + shard_data.get('impact', '') + shard_data.get('context', '')).encode()
        hash_val = int(hashlib.sha256(moral_text).hexdigest(), 16) % (10 ** 8)
        # Example: Use trig and polynomial features for richer embedding
        base = np.linspace(0, 1, self.dim)
        embedding = np.array([
            np.sin(hash_val * b) + np.cos(hash_val / (b + 0.01)) + (hash_val % (i+1))**0.5
            for i, b in enumerate(base)
        ], dtype=np.float32)
        return torch.tensor(embedding)

    def add_shard(self, shard_id, shard_data):
        embedding = self._moral_embedding(shard_data)
        self.shards.append((shard_id, embedding, shard_data))

    def merge_shards(self, new_shards):
        # Accepts a list of (id, embedding, data) tuples from other agents
        for sid, emb, sdata in new_shards:
            if not any(s[0] == sid for s in self.shards):
                self.shards.append((sid, emb, sdata))

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