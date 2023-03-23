class YoutubeComment:
    def __init__(self, user_comment_id, user_comment_text):
        self.user_comment_id = user_comment_id
        self.user_comment_text = user_comment_text

    # 發送YT留言的程式：
    def gpt_send_comment_to_youtube(
        self, youtube_object, user_comment_text, user_comment_id
    ):
        # 設定好youtube回覆API的送出結構
        final_comment_text = (
            user_comment_text + " - 以上言論不代表Shen. 我是它的回覆GPT, 祝你中獎！請期待他的下一隻影片:)"
        )
        send_comment = {
            "snippet": {"parentId": user_comment_id, "textOriginal": final_comment_text}
        }

        # 送出API request，然後把回覆存到response(可存可不存，主要用來debug用)
        response = (
            youtube_object.comments()
            .insert(part="snippet", body=send_comment)
            .execute()
        )
        print(response)
