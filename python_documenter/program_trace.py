from __future__ import annotations
import copy
import sys
import inspect
from collections.abc import Callable

from . import _model


def _default_matcher(function_path: str) -> bool:
    """Return true always."""
    return True


def trace_execution(
    program: Callable[[], None], matcher: _model.FunctionMatcher = _default_matcher
) -> _model.FunctionCalls:
    collector = _FunctionCallCollector(matcher)
    sys.settrace(collector.trace_calls)
    program()
    sys.settrace(None)
    function_calls = collector.get_function_calls()
    return function_calls


class _FunctionCallCollector:
    def __init__(self, matcher: _model.FunctionMatcher) -> None:
        self._function_calls: list[_model.FunctionCall] = []
        self._call_stack_depth = 0
        self._call_count = 0
        self._matcher = matcher

    def trace_calls(self, frame, event, arg):
        handlers = {
            'call': self._handle_call_event,
            'return': self._handle_return_event,
        }
        handler = handlers.get(event)
        if handler:
            handler(frame)

        return self.trace_calls

    def _handle_call_event(self, frame) -> None:
        code = frame.f_code
        function_name = code.co_name
        if function_name == 'write':
            # Ignore internal write calls to avoid recursion
            return
        filename = code.co_filename

        function = frame.f_globals.get(function_name, None)

        if not function:
            return None

        source_lines, _ = inspect.getsourcelines(function)

        source_code = ''.join(source_lines)
        module_name = frame.f_globals['__name__']
        full_qualified_name = f"{module_name}.{function_name}"

        if not self._matcher(full_qualified_name):
            return None
        self._call_stack_depth += 1
        self._call_count += 1

        caller_frame = frame.f_back
        if caller_frame:
            caller_code = caller_frame.f_code
            caller_function_name = caller_code.co_name
            caller_module_name = caller_frame.f_globals['__name__']
            full_caller_name = f"{caller_module_name}.{caller_function_name}"
        else:
            full_caller_name = 'N/A'

        self._function_calls.append(
            _model.FunctionCall(
                self._call_stack_depth,
                self._call_count,
                full_caller_name,
                filename,
                full_qualified_name,
                source_code,
            )
        )

    def _handle_return_event(self, frame) -> None:
        if self._matcher(frame.f_code.co_filename):
            self._call_stack_depth -= 1

    def get_function_calls(self) -> _model.FunctionCalls:
        return copy.deepcopy(self._function_calls)
