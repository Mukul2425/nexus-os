from collections.abc import AsyncGenerator
from time import perf_counter
from typing import Any

from google import genai
from google.genai import types

from app.core.config import settings
from app.core.exceptions import LLMProviderError
from app.logging.context import get_request_id
from app.logging.logger import logger

from app.schemas.chat import ChatMessage
from app.schemas.llm import (
    LLMResponse,
    ToolCall,
    ToolDefinition,
    ToolResult,
)

from app.services.llm.provider import LLMProvider


MODEL_NAME = "gemini-2.5-flash"


class GeminiProvider(LLMProvider):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    # ---------------------------------------------------------
    # Message conversion
    # ---------------------------------------------------------

    def _build_contents(
        self,
        messages: list[ChatMessage],
    ) -> tuple[str | None, list[dict]]:

        system_instruction = None
        contents = []

        for message in messages:

            if message.role == "system":

                system_instruction = message.content

            elif message.role == "user":

                contents.append(
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": message.content
                            }
                        ],
                    }
                )

            elif message.role == "assistant":

                contents.append(
                    {
                        "role": "model",
                        "parts": [
                            {
                                "text": message.content
                            }
                        ],
                    }
                )

        return system_instruction, contents

    # ---------------------------------------------------------
    # Normal generation
    # ---------------------------------------------------------

    def generate(
        self,
        messages: list[ChatMessage],
    ) -> str:

        request_id = get_request_id()

        system_instruction, contents = (
            self._build_contents(messages)
        )

        logger.info(
            "llm_request "
            "request_id=%s "
            "provider=gemini "
            "model=%s "
            "messages=%d",
            request_id,
            MODEL_NAME,
            len(messages),
        )

        start = perf_counter()

        try:

            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                ),
            )

            latency = perf_counter() - start

            logger.info(
                "llm_response "
                "request_id=%s "
                "provider=gemini "
                "model=%s "
                "latency=%.3fs",
                request_id,
                MODEL_NAME,
                latency,
            )

            return response.text

        except Exception as exc:

            latency = perf_counter() - start

            logger.exception(
                "llm_error "
                "request_id=%s "
                "provider=gemini "
                "model=%s "
                "latency=%.3fs",
                request_id,
                MODEL_NAME,
                latency,
            )

            raise LLMProviderError() from exc

    # ---------------------------------------------------------
    # Tool conversion
    # ---------------------------------------------------------

    def _build_tools(
        self,
        tools: list[ToolDefinition],
    ) -> list[types.Tool]:

        declarations = []

        for tool in tools:

            declarations.append(
                types.FunctionDeclaration(
                    name=tool.name,
                    description=tool.description,
                    parameters=tool.input_schema,
                )
            )

        if not declarations:

            return []

        return [
            types.Tool(
                function_declarations=declarations
            )
        ]

    # ---------------------------------------------------------
    # Tool results
    # ---------------------------------------------------------

    def _build_tool_result_contents(
        self,
        tool_results: list[ToolResult],
    ) -> list[dict]:

        contents = []

        for tool_result in tool_results:

            response: dict[str, Any] = {
                "success": tool_result.success,
            }

            if tool_result.success:

                response["result"] = (
                    tool_result.result
                )

            else:

                response["error"] = (
                    tool_result.error
                )

            contents.append(
                {
                    "role": "user",
                    "parts": [
                        {
                            "function_response": {
                                "name": tool_result.name,
                                "response": response,
                            }
                        }
                    ],
                }
            )

        return contents

    # ---------------------------------------------------------
    # Parse Gemini tool calls
    # ---------------------------------------------------------

    def _parse_tool_calls(
        self,
        response,
    ) -> list[ToolCall]:

        tool_calls = []

        candidates = getattr(
            response,
            "candidates",
            None,
        )

        if not candidates:

            return tool_calls

        candidate = candidates[0]

        content = getattr(
            candidate,
            "content",
            None,
        )

        if content is None:

            return tool_calls

        parts = getattr(
            content,
            "parts",
            [],
        )

        for index, part in enumerate(parts):

            function_call = getattr(
                part,
                "function_call",
                None,
            )

            if function_call is None:

                continue

            arguments = getattr(
                function_call,
                "args",
                {},
            )

            tool_calls.append(
                ToolCall(
                    id=f"gemini-call-{index}",
                    name=function_call.name,
                    arguments=dict(arguments),
                )
            )

        return tool_calls

    # ---------------------------------------------------------
    # Tool-aware generation
    # ---------------------------------------------------------

    def generate_with_tools(
        self,
        messages: list[ChatMessage],
        tools: list[ToolDefinition],
        tool_results: list[ToolResult] | None = None,
    ) -> LLMResponse:

        request_id = get_request_id()

        system_instruction, contents = (
            self._build_contents(messages)
        )

        if tool_results:

            contents.extend(
                self._build_tool_result_contents(
                    tool_results
                )
            )

        gemini_tools = self._build_tools(
            tools
        )

        logger.info(
            "llm_tool_request "
            "request_id=%s "
            "provider=gemini "
            "model=%s "
            "messages=%d "
            "tools=%d "
            "tool_results=%d",
            request_id,
            MODEL_NAME,
            len(messages),
            len(tools),
            len(tool_results or []),
        )

        start = perf_counter()

        try:

            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=gemini_tools,
                ),
            )

            latency = perf_counter() - start

            tool_calls = self._parse_tool_calls(
                response
            )

            logger.info(
                "llm_tool_response "
                "request_id=%s "
                "provider=gemini "
                "model=%s "
                "latency=%.3fs "
                "tool_calls=%d",
                request_id,
                MODEL_NAME,
                latency,
                len(tool_calls),
            )

            if tool_calls:

                return LLMResponse(
                    text=None,
                    tool_calls=tool_calls,
                )

            return LLMResponse(
                text=response.text or "",
                tool_calls=[],
            )

        except Exception as exc:

            latency = perf_counter() - start

            logger.exception(
                "llm_tool_error "
                "request_id=%s "
                "provider=gemini "
                "model=%s "
                "latency=%.3fs",
                request_id,
                MODEL_NAME,
                latency,
            )

            raise LLMProviderError() from exc

    # ---------------------------------------------------------
    # Streaming
    # ---------------------------------------------------------

    async def stream(
        self,
        messages: list[ChatMessage],
    ) -> AsyncGenerator[str, None]:

        request_id = get_request_id()

        system_instruction, contents = (
            self._build_contents(messages)
        )

        logger.info(
            "llm_stream_start "
            "request_id=%s "
            "provider=gemini "
            "model=%s "
            "messages=%d",
            request_id,
            MODEL_NAME,
            len(messages),
        )

        start = perf_counter()
        chunk_count = 0

        try:

            stream = (
                self.client.models.generate_content_stream(
                    model=MODEL_NAME,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                    ),
                )
            )

            for chunk in stream:

                if chunk.text:

                    chunk_count += 1

                    yield chunk.text

            latency = perf_counter() - start

            logger.info(
                "llm_stream_complete "
                "request_id=%s "
                "provider=gemini "
                "model=%s "
                "chunks=%d "
                "latency=%.3fs",
                request_id,
                MODEL_NAME,
                chunk_count,
                latency,
            )

        except Exception as exc:

            latency = perf_counter() - start

            logger.exception(
                "llm_stream_error "
                "request_id=%s "
                "provider=gemini "
                "model=%s "
                "chunks=%d "
                "latency=%.3fs",
                request_id,
                MODEL_NAME,
                chunk_count,
            )

            raise LLMProviderError() from exc