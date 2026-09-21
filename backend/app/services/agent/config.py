from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSafetyConfig:
    max_agent_steps: int = 10
    max_tool_calls: int = 5
    timeout_seconds: float = 30.0
    max_repeated_actions: int = 2
    max_plan_steps: int = 5

    def __post_init__(self) -> None:
        if self.max_agent_steps < 1:
            raise ValueError("max_agent_steps must be at least 1")

        if self.max_tool_calls < 0:
            raise ValueError("max_tool_calls cannot be negative")

        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than 0")

        if self.max_repeated_actions < 1:
            raise ValueError("max_repeated_actions must be at least 1")

        if self.max_plan_steps < 1:
            raise ValueError("max_plan_steps must be at least 1")