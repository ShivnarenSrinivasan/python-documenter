import pathlib
import json
import tinydb
from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.language_models import chat_models

from . import _model, _output

_SYS_PROMPT = pathlib.Path(__file__).parent.joinpath('prompts', 'explain_code.md')


def explain_all(
    function_calls: _model.FunctionCalls,
    llm: chat_models.BaseChatModel,
    outfile: pathlib.Path,
) -> None:
    tmp_file = pathlib.Path('_tmp_cache.json')
    out = tinydb.TinyDB(tmp_file)

    for call in function_calls:
        _explanation = explain_code(call.code, llm)
        out.insert(_output.dict_from_call(call) | {'explanation': _explanation})
        all_ = out.all()

        # we don't want to overwrite existing data
        if outfile.exists():
            raise FileExistsError('will overwrite data')

        # we write the results after each explanation to ensure we do not lose
        # data if the program crashes midway
        with open(outfile, 'w') as fp:
            json.dump(all_, fp, indent=4)

    # remove intermediate tinydb instance after explanation
    tmp_file.unlink()


def explain_code(code: str, llm: chat_models.BaseChatModel) -> str:
    human_prompt = '''
    ```python3
    {code}
    ```
    '''
    system_prompt = _SYS_PROMPT.read_text()

    chat_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(human_prompt),
        ]
    )

    messages = chat_template.format_messages(code=code)
    res = llm.invoke(messages)
    content = res.content
    return content
