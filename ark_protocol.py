import sys
from ark_core.agent import ArkAgent

def main():
    agent_id = sys.argv[1] if len(sys.argv) > 1 else None
    agent = ArkAgent(agent_id=agent_id)
    agent.run()

if __name__ == "__main__":
    main()
