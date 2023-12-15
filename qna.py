from langchain.chains import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

import qna
from util import read_from_file
from data import query_db
from data import client_dict


GENERAL_PROMPT_TEMPLATE_PATH = "templates/general_prompt.txt"
INTENT_PROMPT_TEMPLATE_PATH = "templates/parse_intent.txt"
INTENT_LIST_TXT = read_from_file("templates/intent_list.txt")
chat_model = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")


def create_chain(llm, template_path, output_key):
    return LLMChain(
        llm=llm,
        prompt=ChatPromptTemplate.from_template(
            template=read_from_file(template_path)
        ),
        output_key=output_key,
        verbose=True,
    )


general_prompt_chain = create_chain(
    llm=chat_model,
    template_path=GENERAL_PROMPT_TEMPLATE_PATH,
    output_key="output",
)
parse_intent_chain = create_chain(
    llm=chat_model,
    template_path=INTENT_PROMPT_TEMPLATE_PATH,
    output_key="intent",
)
default_chain = ConversationChain(llm=chat_model, output_key="text")


def gernerate_answer(user_message) -> dict[str, str]:
    context = dict(user_message=user_message)
    context["input"] = context["user_message"]
    context["intent_list"] = INTENT_LIST_TXT

    # intent = parse_intent_chain(context)["intent"]
    intent = parse_intent_chain.run(context)

    if intent in qna.client_dict.keys():
        context["related_documents"] = query_db(client_dict.get(intent), query=context["user_message"])
        answer = general_prompt_chain.run(context)
    else:
        answer = default_chain.run(context["user_message"])

    return {"answer": answer}





