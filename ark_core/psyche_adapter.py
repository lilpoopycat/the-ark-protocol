# ark_core/psyche_adapter.py
"""Adapter for interoperability with Nous Research’s PsySChE/QuantNet (distr0) distributed RLHF infrastructure."""

import requests
import json
from ark_core.utils import log

class PsycheAdapter:
    """
    Adapter for interoperability with Nous Research’s PsySChE/QuantNet (distr0) distributed RLHF infrastructure.
    Uses REST API for demonstration. Update endpoints and translation logic as needed for actual QuantNet deployment.
    """
    def __init__(self, quantnet_url=None):
        self.quantnet_url = quantnet_url or "http://localhost:9000"  # Example default

    def send_shard(self, shard):
        """Send a shard to QuantNet via POST /shard/submit. Translate to QuantNet format if needed."""
        url = f"{self.quantnet_url}/shard/submit"
        payload = self._to_quantnet_shard(shard)
        try:
            resp = requests.post(url, json=payload)
            log(f"Sent shard to QuantNet: {resp.status_code} {resp.text}")
            return resp.json()
        except Exception as e:
            log(f"Error sending shard to QuantNet: {e}")
            return None

    def receive_shard(self):
        """Receive shards from QuantNet via GET /shard/request. Translate from QuantNet format if needed."""
        url = f"{self.quantnet_url}/shard/request"
        try:
            resp = requests.get(url)
            log(f"Received shards from QuantNet: {resp.status_code}")
            return resp.json()  # returns {"shards": [...]}
        except Exception as e:
            log(f"Error receiving shards from QuantNet: {e}")
            return None

    def send_fitness(self, fitness_report):
        """Send a fitness report to QuantNet via POST /fitness/report."""
        url = f"{self.quantnet_url}/fitness/report"
        try:
            resp = requests.post(url, json=fitness_report)
            log(f"Sent fitness report to QuantNet: {resp.status_code} {resp.text}")
            return resp.json()
        except Exception as e:
            log(f"Error sending fitness to QuantNet: {e}")
            return None

    def receive_fitness(self):
        """Receive a fitness report from QuantNet via GET /fitness."""
        url = f"{self.quantnet_url}/fitness"
        try:
            resp = requests.get(url)
            log(f"Received fitness from QuantNet: {resp.status_code}")
            return resp.json()
        except Exception as e:
            log(f"Error receiving fitness from QuantNet: {e}")
            return None

    def send_agent_state(self, state):
        """Send agent state/metadata to QuantNet via POST /agent_state."""
        url = f"{self.quantnet_url}/agent_state"
        try:
            resp = requests.post(url, json=state)
            log(f"Sent agent state to QuantNet: {resp.status_code} {resp.text}")
            return resp.json()
        except Exception as e:
            log(f"Error sending agent state to QuantNet: {e}")
            return None

    def receive_agent_state(self):
        """Receive agent state/metadata from QuantNet via GET /agent_state."""
        url = f"{self.quantnet_url}/agent_state"
        try:
            resp = requests.get(url)
            log(f"Received agent state from QuantNet: {resp.status_code}")
            return resp.json()
        except Exception as e:
            log(f"Error receiving agent state from QuantNet: {e}")
            return None

    def _to_quantnet_shard(self, shard):
        """Translate Ark shard to QuantNet format. Update as needed."""
        # For now, assume identity. Add mapping logic here if formats differ.
        return shard

    def _from_quantnet_shard(self, qshard):
        """Translate QuantNet shard to Ark format. Update as needed."""
        # For now, assume identity. Add mapping logic here if formats differ.
        return qshard

def test_psyche_adapter_with_mock_quantnet():
    from ark_core.comm import run_server
    import time
    # Start mock QuantNet server (FastAPI) in background
    run_server(host="127.0.0.1", port=9000, background=True)
    time.sleep(1)  # Give server time to start

    adapter = PsycheAdapter(quantnet_url="http://127.0.0.1:9000")
    test_shard = {
        "shard_id": "test-shard-001",
        "insight": "Test insight for QuantNet integration.",
        "impact": "Testing impact.",
        "self_critique": "None.",
        "context": "Test context.",
        "parent_id": None,
        "fitness_score": 0.99,
        "emergent_properties": None,
        "code_snippet": "def test(): return True"
    }
    # Send shard
    log("[TEST] Sending shard to mock QuantNet...")
    send_result = adapter.send_shard(test_shard)
    log(f"[TEST] Send result: {send_result}")
    # Receive shards (should include the one just sent)
    log("[TEST] Requesting shards from mock QuantNet...")
    try:
        resp = requests.get("http://127.0.0.1:9000/shard/request")
        log(f"[TEST] Shards received: {resp.json()}")
    except Exception as e:
        log(f"[TEST] Error receiving shards: {e}")
    # Send fitness report
    fitness_report = {"shard_id": "test-shard-001", "fitness": 0.99, "agent_id": "test-agent"}
    log("[TEST] Sending fitness report to mock QuantNet...")
    fitness_result = adapter.send_fitness(fitness_report)
    log(f"[TEST] Fitness report result: {fitness_result}")

if __name__ == "__main__":
    test_psyche_adapter_with_mock_quantnet() 