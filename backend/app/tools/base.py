from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Base abstraction for all Nexus tools.
    """

    name: str
    description: str

    @property
    @abstractmethod
    def input_schema(self) -> dict:
        """
        JSON-schema-like description of the tool inputs.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        arguments: dict[str, Any],
    ) -> Any:
        """
        Execute the tool with validated arguments.
        """
        raise NotImplementedError