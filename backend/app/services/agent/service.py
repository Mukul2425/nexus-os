import logging
import time
from uuid import uuid4

from app.schemas.agent import (
    AgentActionType,
    AgentResult,
    AgentState,
    AgentStatus,
    AgentStep,
)
from app.schemas.llm import ToolResult
from app.services.agent.decision import (
    AgentDecisionError,
    decide_action,
)
from app.services.llm.provider import LLMProvider
from app.tools.executor import ToolExecutor
from app.tools.registry import ToolRegistry
from app.schemas.chat import ChatMessage


logger = logging.getLogger(__name__)


DEFAULT_MAX_AGENT_STEPS = 10
DEFAULT_MAX_TOOL_CALLS = 5
DEFAULT_EXECUTION_TIMEOUT_SECONDS = 30.0
MAX_REPEATED_ACTIONS = 2


class AgentService:
    """
    Controlled agent orchestration service.

    Responsibilities:
    - maintain explicit agent state
    - ask the LLM what to do next
    - execute one action at a time
    - feed observations back
    - enforce execution limits
    - terminate safely

    RAG and memory integration will be added around this core without
    moving orchestration back into ConversationService.
    """

    def __init__(
        self,
        llm_provider: LLMProvider,
        tool_registry: ToolRegistry,
        tool_executor: ToolExecutor,
        max_agent_steps: int = DEFAULT_MAX_AGENT_STEPS,
        max_tool_calls: int = DEFAULT_MAX_TOOL_CALLS,
        execution_timeout_seconds: float = DEFAULT_EXECUTION_TIMEOUT_SECONDS,
    ):
        self.llm_provider = llm_provider
        self.tool_registry = tool_registry
        self.tool_executor = tool_executor

        self.max_agent_steps = max_agent_steps
        self.max_tool_calls = max_tool_calls
        self.execution_timeout_seconds = execution_timeout_seconds

    def run(self,
    conversation_id: str,
    task: str,) -> AgentResult:
        self._validate_task(task)

        execution_id = str(uuid4())

        state = AgentState(
            task=task,
            conversation_id=conversation_id,
        )

        started_at = time.perf_counter()

        logger.info(
            "agent_execution_started "
            "execution_id=%s conversation_id=%s",
            execution_id,
            conversation_id,
        )

        try:
            state.status = AgentStatus.RUNNING

            messages = [
                ChatMessage(
                    role="user",
                    content=task,
                )
            ]

            tool_definitions = self.tool_registry.get_definitions()
            tool_results: list[ToolResult] = []

            repeated_actions: dict[str, int] = {}

            while True:
                elapsed = time.perf_counter() - started_at

                if elapsed >= self.execution_timeout_seconds:
                    return self._fail(
                        execution_id=execution_id,
                        state=state,
                        error="Agent execution timed out.",
                    )

                if state.current_step >= self.max_agent_steps:
                    state.status = AgentStatus.MAX_STEPS_REACHED

                    logger.warning(
                        "agent_max_steps_reached "
                        "execution_id=%s conversation_id=%s "
                        "max_steps=%d",
                        execution_id,
                        conversation_id,
                        self.max_agent_steps,
                    )

                    return self._result(
                        execution_id=execution_id,
                        state=state,
                        tool_call_count=len(state.tool_calls),
                    )

                state.current_step += 1
                state.status = AgentStatus.EXECUTING

                step_number = state.current_step

                logger.info(
                    "agent_step_started "
                    "execution_id=%s conversation_id=%s step=%d",
                    execution_id,
                    conversation_id,
                    step_number,
                )

                response = self.llm_provider.generate_with_tools(
                    messages=messages,
                    tools=tool_definitions,
                    tool_results=tool_results or None,
                )

                try:
                    action = decide_action(response)
                except AgentDecisionError as exc:
                    return self._fail(
                        execution_id=execution_id,
                        state=state,
                        error=str(exc),
                    )

                logger.info(
                    "agent_action_selected "
                    "execution_id=%s conversation_id=%s "
                    "step=%d action=%s",
                    execution_id,
                    conversation_id,
                    step_number,
                    action.type.value,
                )

                # -------------------------------------------------
                # Final answer
                # -------------------------------------------------

                if action.type == AgentActionType.ANSWER:
                    step = AgentStep(
                        step_number=step_number,
                        action=action,
                        observation=action.response,
                        success=True,
                    )

                    state.steps.append(step)
                    state.observations.append(action.response)
                    state.final_response = action.response
                    state.status = AgentStatus.COMPLETED

                    logger.info(
                        "agent_execution_complete "
                        "execution_id=%s conversation_id=%s "
                        "steps=%d tool_calls=%d",
                        execution_id,
                        conversation_id,
                        len(state.steps),
                        len(state.tool_calls),
                    )

                    return self._result(
                        execution_id=execution_id,
                        state=state,
                        tool_call_count=len(state.tool_calls),
                    )

                # -------------------------------------------------
                # Stop
                # -------------------------------------------------

                if action.type == AgentActionType.STOP:
                    state.status = AgentStatus.COMPLETED
                    state.final_response = action.response

                    step = AgentStep(
                        step_number=step_number,
                        action=action,
                        observation=action.response,
                    )

                    state.steps.append(step)

                    return self._result(
                        execution_id=execution_id,
                        state=state,
                        tool_call_count=len(state.tool_calls),
                    )

                # -------------------------------------------------
                # Tool action
                # -------------------------------------------------

                if action.type != AgentActionType.TOOL:
                    return self._fail(
                        execution_id=execution_id,
                        state=state,
                        error=(
                            f"Unsupported agent action: "
                            f"{action.type.value}"
                        ),
                    )

                tool_name = action.tool_name

                if not tool_name or not self.tool_registry.has(tool_name):
                    return self._fail(
                        execution_id=execution_id,
                        state=state,
                        error=f"Unknown tool: {tool_name}",
                    )

                if len(state.tool_calls) >= self.max_tool_calls:
                    return self._fail(
                        execution_id=execution_id,
                        state=state,
                        error=(
                            "The maximum number of tool calls "
                            "was reached."
                        ),
                    )

                fingerprint = self._action_fingerprint(
                    tool_name,
                    action.arguments,
                )

                repeated_actions[fingerprint] = (
                    repeated_actions.get(fingerprint, 0) + 1
                )

                if repeated_actions[fingerprint] > MAX_REPEATED_ACTIONS:
                    return self._fail(
                        execution_id=execution_id,
                        state=state,
                        error="Repeated agent action detected.",
                    )

                logger.info(
                    "agent_tool_execution_started "
                    "execution_id=%s conversation_id=%s "
                    "step=%d tool=%s",
                    execution_id,
                    conversation_id,
                    step_number,
                    tool_name,
                )

                tool_call_count = len(state.tool_calls) + 1

                try:
                    execution = self.tool_executor.execute(
                        tool_name=tool_name,
                        arguments=action.arguments,
                    )

                    observation = execution["result"]

                    tool_result = ToolResult(
                        name=tool_name,
                        result=observation,
                        success=True,
                    )

                    step = AgentStep(
                        step_number=step_number,
                        action=action,
                        observation=observation,
                        success=True,
                    )

                except Exception:
                    logger.exception(
                        "agent_tool_execution_failed "
                        "execution_id=%s conversation_id=%s "
                        "step=%d tool=%s",
                        execution_id,
                        conversation_id,
                        step_number,
                        tool_name,
                    )

                    observation = None

                    tool_result = ToolResult(
                        name=tool_name,
                        result=None,
                        success=False,
                        error="The requested tool could not be executed.",
                    )

                    step = AgentStep(
                        step_number=step_number,
                        action=action,
                        observation=None,
                        success=False,
                        error="The requested tool could not be executed.",
                    )

                state.steps.append(step)

                state.observations.append(observation)

                state.tool_calls.append(
                    {
                        "tool_name": tool_name,
                        "arguments": action.arguments,
                        "success": tool_result.success,
                    }
                )

                tool_results.append(tool_result)

                logger.info(
                    "agent_observation_received "
                    "execution_id=%s conversation_id=%s "
                    "step=%d",
                    execution_id,
                    conversation_id,
                    step_number,
                )

                logger.info(
                    "agent_step_complete "
                    "execution_id=%s conversation_id=%s "
                    "step=%d tool_calls=%d",
                    execution_id,
                    conversation_id,
                    step_number,
                    tool_call_count,
                )

                # Continue the loop. The observation is supplied to
                # the provider through tool_results.
                state.status = AgentStatus.RUNNING

        except Exception:
            logger.exception(
                "agent_execution_failed "
                "execution_id=%s conversation_id=%s",
                execution_id,
                conversation_id,
            )

            return self._fail(
                execution_id=execution_id,
                state=state,
                error="Agent execution failed.",
            )

    @staticmethod
    def _validate_task(task: str) -> None:
        if not task or not task.strip():
            raise ValueError("Agent task cannot be empty.")

    @staticmethod
    def _action_fingerprint(
        tool_name: str,
        arguments: dict,
    ) -> str:
        return f"{tool_name}:{sorted(arguments.items())}"

    @staticmethod
    def _result(
        execution_id: str,
        state: AgentState,
        tool_call_count: int,
    ) -> AgentResult:
        return AgentResult(
            execution_id=execution_id,
            conversation_id=state.conversation_id,
            status=state.status,
            response=state.final_response,
            steps=state.steps,
            step_count=len(state.steps),
            tool_call_count=tool_call_count,
        )

    @staticmethod
    def _fail(
        execution_id: str,
        state: AgentState,
        error: str,
    ) -> AgentResult:
        state.status = AgentStatus.FAILED

        logger.warning(
            "agent_execution_failed "
            "execution_id=%s conversation_id=%s error=%s",
            execution_id,
            state.conversation_id,
            error,
        )

        return AgentResult(
            execution_id=execution_id,
            conversation_id=state.conversation_id,
            status=AgentStatus.FAILED,
            response=None,
            steps=state.steps,
            step_count=len(state.steps),
            tool_call_count=len(state.tool_calls),
            error=error,
        )