import pathlib
import json
from . import _model


def save_function_calls(
    calls: list[_model.FunctionCall], output_file: pathlib.Path
) -> None:
    out = []
    done: set[_model.FunctionCall] = set()
    for call_ in calls:
        if call_ not in done:
            out.append(dict_from_call(call_))
            done.add(call_)

    with open(output_file, 'w') as f:
        json.dump(out, f, indent=4)


def dict_from_call(call_: _model.FunctionCall) -> dict[str, str | int]:
    return {
        'call_stack_depth': call_.depth,
        'call_count': call_.call_count,
        'calling_function': call_.caller,
        'filename': call_.filename,
        'function': call_.function,
        'code': call_.code,
    }
