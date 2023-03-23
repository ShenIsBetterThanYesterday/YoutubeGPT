import openai
import os


def get_open_ai_api_chat_response(prompt):
    # 讀出 open api key
    # 先在terminal裡面設定環境變量： export OPEN_API_KEY=你的apikey  ，名字可以換成你想要的
    # 範例： export OPEN_API_KEYYYYYY=lsfwncdsjcw
    # 之後下面的程式碼會自動讀出你當下環境裡面的指定變量
    openai.api_key = os.environ.get("OPEN_API_KEY")

    # 範例文件
    # openai.ChatCompletion.create(
    #   model="gpt-3.5-turbo",
    #   messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Who won the world series in 2020?"},
    #         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #         {"role": "user", "content": "Where was it played?"}
    #     ]
    # )

    # 把用戶輸入的prompt拼裝成像上面的範例文件
    user_prompt = {}
    user_prompt["role"] = "user"
    user_prompt["content"] = prompt
    messages = []
    messages.append(
        {
            "role": "assistant",
            "content": "You are a funny Youtube comment replay assistant",
        }
    )
    messages.append(user_prompt)

    # 送出api request (點完菜，送給服務生，服務生送去給廚房)
    # 廚房這邊就是Open AI 他們的GPT-3.5 TURBO
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    # response的範例
    #   {
    #  'id': 'chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve',
    #  'object': 'chat.completion',
    #  'created': 1677649420,
    #  'model': 'gpt-3.5-turbo',
    #  'usage': {'prompt_tokens': 56, 'completion_tokens': 31, 'total_tokens': 87},
    #  'choices': [
    #    {
    #     'message': {
    #       'role': 'assistant',
    #       'content': 'The 2020 World Series was played in Arlington, Texas at the Globe Life Field, which was the new home stadium for the Texas Rangers.'},
    #     'finish_reason': 'stop',
    #     'index': 0
    #    }
    #   ]
    # }
    # 服務身上菜了，我們開始吃想要吃的菜，這邊想要吃的菜就是傳回來的答案
    ai_answer = response["choices"][0]["message"]["content"].replace("\n", "<br>")
    # 把答案返迴給呼叫這個方程的地方
    return ai_answer
