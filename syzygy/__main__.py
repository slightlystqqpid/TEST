from __future__ import annotations

from syzygy.bootstrap import bootstrap_environment, validate_environment
from syzygy.identity import AgentRegistry


def main() -> None:
    root = "."
    result = bootstrap_environment(root)
    print(f"bootstrap status: {result['status']}")
    validation = validate_environment(root)
    print(f"validation valid: {validation['valid']}")

    registry = AgentRegistry()
    registry.seed_default_agents()
    print([agent.agent_id for agent in registry.list()])


if __name__ == "__main__":
    main()
