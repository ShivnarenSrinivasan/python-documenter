import os
import json
import tinydb

from langchain_openai import AzureChatOpenAI
import httpx
import dotenv

from python_documenter import explain

dotenv.load_dotenv(verbose=True)


def main() -> None:
    # with open('unique.json') as fp:
    #     _d = json.load(fp)
    source = tinydb.TinyDB('source.json')
    # for d in _d:
    #     source.insert(d)

    out = tinydb.TinyDB('out.json')
    data = source.all()
    model = _get_model(500)

    for call in data:
        explanation = explain.explain_code(call['code'], model)
        out.insert(call | {'explanation': explanation})
        all_ = out.all()
        with open('explanation.json', 'w') as fp:
            json.dump(all_, fp, indent=4)


def _get_model(max_tokens: int, model: str = 'gpt-4-32k') -> AzureChatOpenAI:
    llm = AzureChatOpenAI(
        temperature=0,
        http_client=httpx.Client(verify=False),
        azure_deployment=model,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        max_tokens=max_tokens,
    )
    return llm


if __name__ == '__main__':
    main()
