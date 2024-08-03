from collections.abc import Iterable
import typing


class FunctionMatcher(typing.Protocol):
    def __call__(self, function_path: str) -> bool:
        """Return if function is to be considered.

        `function_path` is the fully qualified path to the function."""


class FunctionCall(typing.NamedTuple):
    depth: int
    call_count: int
    caller: str
    filename: str
    function: str
    code: str


FunctionCalls = Iterable[FunctionCall]
