from dto import ChatbotRequest
import time
import logging
import os
import requests

from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    SystemMessage
)

# 환경 변수 처리 필요!
os.environ['OPENAI_API_KEY'] = ''
SYSTEM_MSG = "당신은 카카오 서비스 제공자입니다."
logger = logging.getLogger("Callback")

def read_from_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()

kakaotalk_sync_txt = read_from_file('project_data_kakaosync.txt')

def callback_handler(request: ChatbotRequest) -> dict:
    system_message = "assistant는 챗봇으로 동작한다. 챗봇은 '제품정보' 내용을 참고하여, user의 질문 혹은 요청에 따라 적절한 답변을 제공합니다."
    human_template = (request.userRequest.utterance)

    system_message_prompt = SystemMessage(content=system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat = ChatOpenAI(temperature=0.8, max_tokens=3000)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=chat, prompt=chat_prompt)

    output_text = chain.run(product_data=kakaotalk_sync_txt)

   # 참고링크 통해 payload 구조 확인 가능
    payload = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": output_text
                    }
                }
            ]
        }
    }
    # ===================== end =================================
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/ai_chatbot_callback_guide
    # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

    print(payload)

    url = request.userRequest.callbackUrl

    if url:
        return requests.post(url, json=payload).json()
