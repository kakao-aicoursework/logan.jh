import json
import openai
import tkinter as tk
import pandas as pd
from tkinter import scrolledtext
import tkinter.filedialog as filedialog
import chromadb
import os

openai.api_key = os.environ['API_KEY']

client = chromadb.PersistentClient()
kakaotalk_channel_collection = client.create_collection(
    name='kakaotalk_channel',
    metadata={"hnsw:space": "cosine"} # l2 is the default
)

kakaotalk_channel_text = """카카오톡 채널:

#이해하기
이 문서는 카카오톡 채널 API를 소개합니다.

#기능 소개
카카오톡 채널(구:플러스친구)은 카카오톡 사용자들에게 다양한 서비스 소식을 메시지와 게시물 형태로 전파할 수 있는 서비스입니다. 카카오톡 채널은 친구인 사용자들에게 마케팅(Marketing) 메시지를 보내는 기능을 제공합니다. 친구란 카카오톡 채널을 친구로 추가한 사용자를 말합니다. 카카오톡 채널 메시지는 비용 절감을 위해 사용자의 성별, 나이, 지역, 등급 등 정보를 토대로 친구 그룹을 만들어서 보다 높은 효과가 기대되는 사용자들에게만 발송하는 것도 가능합니다.
카카오톡 채널을 활용하여 서비스와 사용자의 관계를 더욱 긴밀하게 유지할 수 있습니다. 예를 들면 카카오톡 채널 메시지를 통해 사용자에게 서비스 웹 페이지 방문을 유도하거나 유익한 상품 정보의 링크를 제공하는 것이 가능합니다. 1:1 채팅, 스마트채팅, 봇 등 유용한 추가 기능들도 이용할 수 있습니다.

카카오톡 채널 API는 크게 두 가지의 기능을 제공합니다. 카카오톡 사용자를 위한 카카오톡 채널 추가 및 채팅 API, 다른 카카오톡 채널 관리자가 보다 편리하게 고객 그룹을 관리할 수 있도록 도와주는 카카오톡 채널 고객 관리 API가 있습니다. 두 API 모두 카카오톡 채널 프로필 ID를 사용해 요청하지만, 각각 역할과 제공 방식이 다릅니다.

카카오톡 채널 API를 사용하려면 앱과 카카오톡 채널이 연결되어 있어야 합니다. 또한 사용자의 '카카오톡 채널 추가 상태' 제공 동의가 필요합니다. 자세한 안내 및 설정 방법은 설정하기를 참고합니다.

참고: 카카오톡 채널 프로필 ID 확인 방법
[카카오톡 채널 관리자센터] > [관리] > [상세설정]에서 카카오톡 채널의 채널 URL을 확인할 수 있습니다. 채널 URL에서 https://pf.kakao.com/ 부분을 제외한 뒷자리 값이 해당 카카오톡 채널의 프로필 ID입니다. 다음 예시를 참고합니다.


#카카오톡 채널 추가와 채팅
Kakao SDK를 통해 제공되는 카카오톡 채널 추가와 채팅 API는 카카오톡 채널로 이동할 수 있는 연결 페이지(Bridge page)를 띄우는 기능입니다. 연결 페이지는 사용자 진입 시 카카오톡 채널로 이동할지 묻는 팝업을 띄우고, 사용자가 이동에 동의하면 커스텀 URL 스킴(Custom URL Scheme)을 통해 카카오톡을 실행하고 해당 카카오톡 채널 화면으로 이동합니다. 사용자는 카카오톡 채널 화면에서 해당 카카오톡 채널을 친구로 추가하거나 1:1 채팅을 시작할 수 있습니다.

이 기능은 카카오톡 사용자만 이용할 수 있습니다. 카카오톡을 사용하지 않는 카카오계정으로 로그인한 사용자에게는 "이 계정과 연결된 카카오톡이 없습니다."라는 문구가 포함된 안내 화면이 나타납니다.

왜 사용자를 카카오톡으로 이동시키지 않고 연결 페이지만 띄우나요?
일부 플랫폼은 OS 정책상 사용자를 특정 애플리케이션으로 이동시키는 행위가 제한돼 있습니다. 사용자가 직접 특정 웹 페이지나 애플리케이션을 한 번 실행시키는 것까지는 문제없지만, 여러 차례 사용자를 임의로 이동시키는 건 정책상 문제가 될 수 있습니다. OS 정책에 따라 오픈마켓 리뷰가 거절(Reject)되는 경우와 같은 문제를 피하기 위해 이 API는 연결 페이지 실행 기능만 제공합니다.

#카카오톡 채널 고객 관리
카카오톡 채널 고객 관리 API를 사용하여 카카오톡 채널 관리자센터에서 제공하는 카카오톡 채널 고객 파일 등록 및 관리 기능을 API 방식으로 이용할 수 있습니다.

카카오톡 채널 고객 관리 API는 마케팅 시 보다 정교한 사용자 타게팅을 가능하게 합니다. 카카오 로그인이나 카카오싱크 간편가입을 적용한 서비스는 사용자 정보를 바탕으로 카카오톡 채널 고객 관리 API를 사용해 고객 파일을 등록하고, 해당 고객 파일을 대상으로 카카오톡 채널 관리자센터에서 원하는 조건에 따라 친구 그룹을 생성하여 타깃 메시지를 보낼 수 있습니다. 자세한 사항은 카카오톡 채널 관리자센터 공지사항을 참고합니다.

이 기능은 REST API 방식으로만 제공되며, 서버에서만 호출해야 합니다. 설정하기(https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/prerequisite#admin-api)와 REST API(https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api)를 참고합니다.

#더 효과적인 활용 방법
사용자가 카카오 로그인을 통해 서비스에 연결되면, 카카오톡 채널 관계 확인하기를 통해 각 사용자의 카카오톡 채널 추가 상태를 확인할 수 있습니다. 사용자의 카카오톡 채널 추가 상태에 따라 카카오톡 채널과 친구가 아닌 사용자에게 친구 추가를 유도하거나 고객 파일에서 사용자를 제외할 수 있습니다. 
다음 url을 참고합니다.

-REST API : https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#check-relationship
-JavaScript : https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/js#check-relationship
-Android : https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/android#check-relationship
-iOS : https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/ios#check-relationship


이와 더불어 카카오톡 채널 관계 알림 기능을 적용하면 사용자가 서비스와 연결된 카카오톡 채널을 추가 또는 차단했을 때 알림을 받을 수 있습니다.

앱과 연결된 카카오톡 채널을 추가한 사용자들에게 카카오톡 채널 메시지를 보낼 때, 현재 해당 카카오톡 채널을 차단한 사용자나 별도로 카카오톡에서 친구 추가한 사용자는 자체적으로 파악이 어려울 수 있습니다. 이 경우에도 채널 관계 알림을 사용하면 알림을 통해 변동 사항을 파악할 수 있습니다.

카카오 로그인과 관계없이 [친구 추가] 버튼을 서비스에 노출하고 싶다면 Kakao SDK가 지원하는 카카오톡 채널 추가하기 기능을 사용합니다. 사용자는 서비스 이용 중 이 버튼을 눌러 쉽게 상담을 위한 1:1 대화를 시작할 수 있습니다.


#지원하는 기능
각 API 및 기능의 Kakao SDK 지원 여부는 지원 범위에서 확인할 수 있습니다.

API 및 기능 : 설명 : 문서 URL
카카오톡 채널 추가하기 |사용자가 지정된 카카오톡 채널을 친구로 추가할 수 있는 연결 페이지를 제공합니다. | JavaScript:https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/js#add-channel
카카오톡 채널 채팅하기 | 사용자가 지정된 카카오톡 채널과의 1:1 채팅방으로 진입할 수 있는 연결 페이지를 제공합니다. | JavaScript:https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/js#add-chat
카카오톡 채널 관계 확인하기 | 현재 로그인한 사용자와 앱에 연결된 카카오톡 채널의 친구 관계를 확인합니다. | REST API: https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#check-relationship
여러 사용자 카카오톡 채널 관계 확인하기 | 앱에 연결된 카카오톡 채널과 여러 사용자의 친구 관계를 확인합니다. | REST API:https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#check-multiple-relationship
카카오톡 채널 관계 알림 | 사용자가 앱에 연결된 카카오톡 채널을 추가하거나 차단했을 때 서비스 서버에 알려줍니다. | 콜백:https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/callback#relationship
고객 관리:고객 파일 등록하기 | 새로운 고객 파일을 만듭니다. | REST API:https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#create-user-file
고객 관리:고객 파일 보기 | 카카오톡 채널에 등록된 고객 파일 정보들을 확인합니다. | REST API:https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#view-user-file
고객 관리:사용자 추가하기 | 고객 파일에 사용자 정보를 추가합니다. | REST API:https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#add-user
고객 관리:사용자 삭제하기 | 카카오톡 채널에 등록된 고객 파일에서 특정 사용자를 삭제합니다. | REST API:https://developers.kakao.com/docs/latest/ko/kakaotalk-channel/rest-api#delete-user
"""

# response에 CSV 형식이 있는지 확인하고 있으면 저장하기
def save_to_csv(df):
    file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    if file_path:
        df.to_csv(file_path, sep=';', index=False, lineterminator='\n')
        return f'파일을 저장했습니다. 저장 경로는 다음과 같습니다. \n {file_path}\n'
    return '저장을 취소했습니다'


def save_playlist_as_csv(playlist_csv):
    if ";" in playlist_csv:
        lines = playlist_csv.strip().split("\n")
        csv_data = []

        for line in lines:
            if ";" in line:
                csv_data.append(line.split(";"))

        if len(csv_data) > 0:
            df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
            return save_to_csv(df)

    return f'저장에 실패했습니다. \n저장에 실패한 내용은 다음과 같습니다. \n{playlist_csv}'


def send_message(message_log, functions, gpt_model="gpt-3.5-turbo", temperature=0.1):
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=message_log,
        temperature=temperature,
        functions=functions,
        function_call='auto',
    )

    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        available_functions = {
            "save_playlist_as_csv": save_playlist_as_csv,
        }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        # 사용하는 함수에 따라 사용하는 인자의 개수와 내용이 달라질 수 있으므로
        # **function_args로 처리하기
        function_response = fuction_to_call(**function_args)

        # 함수를 실행한 결과를 GPT에게 보내 답을 받아오기 위한 부분
        message_log.append(response_message)  # GPT의 지난 답변을 message_logs에 추가하기
        message_log.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # 함수 실행 결과도 GPT messages에 추가하기
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=message_log,
            temperature=temperature,
        )  # 함수 실행 결과를 GPT에 보내 새로운 답변 받아오기
    return response.choices[0].message.content


def main():
    temp_chunks = kakaotalk_channel_text.split('\n#')
    ids = []
    metadatas = []
    contents =[]
    for idx, e in enumerate(temp_chunks):
        lines = e.split('\n', maxsplit=1)
        title = lines[0]
        content = lines[1]
        metadata = {
            'title': title,
            'content': content
        }

        ids.append(title)
        metadatas.append(metadata)
        contents.append(content)

    kakaotalk_channel_collection.add(
        ids=ids,
        metadatas=metadatas,
        documents=contents
    )

    message_log = [
        {
            "role": "system",
            "content": '''
            당신은 카카오톡 채널 서비스 챗봇입니다. 사용자가 질문을 하면 전문적인 상담가처럼 친절하고 자세하게 답변해주세요.
            '''
        }
    ]

    functions = [
        {
            "name": "save_playlist_as_csv",
            "description": "Saves the given playlist data into a CSV file when the user confirms the playlist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "playlist_csv": {
                        "type": "string",
                        "description": "A playlist in CSV format separated by ';'. It must contains a header and the release year should follow the 'YYYY' format. The CSV content must starts with a new line. The header of the CSV file must be in English and it should be formatted as follows: 'Title;Artist;Released'.",
                    },
                },
                "required": ["playlist_csv"],
            },
        }
    ]

    def get_content_from_vectordb(search_word: str):
        return kakaotalk_channel_collection.query(
            query_texts=[search_word],
            n_results=2
        )

    def show_popup_message(window, message):
        popup = tk.Toplevel(window)
        popup.title("")

        # 팝업 창의 내용
        label = tk.Label(popup, text=message, font=("맑은 고딕", 12))
        label.pack(expand=True, fill=tk.BOTH)

        # 팝업 창의 크기 조절하기
        window.update_idletasks()
        popup_width = label.winfo_reqwidth() + 20
        popup_height = label.winfo_reqheight() + 20
        popup.geometry(f"{popup_width}x{popup_height}")

        # 팝업 창의 중앙에 위치하기
        window_x = window.winfo_x()
        window_y = window.winfo_y()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        popup_x = window_x + window_width // 2 - popup_width // 2
        popup_y = window_y + window_height // 2 - popup_height // 2
        popup.geometry(f"+{popup_x}+{popup_y}")

        popup.transient(window)
        popup.attributes('-topmost', True)

        popup.update()
        return popup

    def on_send():
        user_input = user_entry.get()
        content_from_vectordb = get_content_from_vectordb(user_input)
        user_entry.delete(0, tk.END)

        if user_input.lower() == "quit":
            window.destroy()
            return

        message_log.append({"role": "user", "content": content_from_vectordb['documents'][0]})
        message_log.append({"role": "user", "content": user_input})
        conversation.config(state=tk.NORMAL)  # 이동
        conversation.insert(tk.END, f"You: {user_input}\n", "user")  # 이동
        thinking_popup = show_popup_message(window, "처리중...")
        window.update_idletasks()
        # '생각 중...' 팝업 창이 반드시 화면에 나타나도록 강제로 설정하기
        response = send_message(message_log, functions)
        thinking_popup.destroy()

        message_log.append({"role": "assistant", "content": response})

        # 태그를 추가한 부분(1)
        conversation.insert(tk.END, f"gpt assistant: {response}\n", "assistant")
        conversation.config(state=tk.DISABLED)
        # conversation을 수정하지 못하게 설정하기
        conversation.see(tk.END)

    window = tk.Tk()
    window.title("카카오 서비스 챗봇")

    font = ("맑은 고딕", 10)

    conversation = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg='#f0f0f0', font=font)
    # width, height를 없애고 배경색 지정하기(2)
    conversation.tag_configure("user", background="black")
    # 태그별로 다르게 배경색 지정하기(3)
    conversation.tag_configure("assistant", background="red")
    # 태그별로 다르게 배경색 지정하기(3)
    conversation.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    # 창의 폭에 맞추어 크기 조정하기(4)

    conversation.insert(tk.END, f"assistant: 저는 카카오 서비스 챗봇입니다\n", "assistant")  # 이동

    input_frame = tk.Frame(window)  # user_entry와 send_button을 담는 frame(5)
    input_frame.pack(fill=tk.X, padx=10, pady=10)  # 창의 크기에 맞추어 조절하기(5)

    user_entry = tk.Entry(input_frame)
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)

    send_button = tk.Button(input_frame, text="Send", command=on_send)
    send_button.pack(side=tk.RIGHT)

    window.bind('<Return>', lambda event: on_send())
    window.mainloop()


if __name__ == "__main__":
    main()