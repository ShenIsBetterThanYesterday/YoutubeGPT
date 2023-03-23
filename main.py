import os
import json
import YoutubeModule
import time

from openAiAPI import get_open_ai_api_chat_response
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Google API的json檔案路徑
creds_file = "./youtube_gpt.json"

# 用json檔案來做一個google 登入認證
flow = InstalledAppFlow.from_client_secrets_file(
    creds_file, scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
)

# 把認證完的資料存到本地的一個新檔案，這樣子就不用每次執行的時後都要重新認證一次
# 如果檔案已經存在了，就覆寫過去
creds = None
if os.path.exists("./creds.json"):
    creds_data = json.load(open("./creds.json"))
    creds = Credentials.from_authorized_user_info(info=creds_data)

# 如果檔案不存在，就創一個新的
if not creds or not creds.valid:
    creds = flow.run_local_server(port=0)
    with open("./creds.json", "w") as f:
        f.write(creds.to_json())

# 建新youtube的物件
youtube = build("youtube", "v3", credentials=creds)
# 影片的id，這個可以從影片的url裡面的最後部份拿出來
# 範例：假的影片的url是 https://www.youtube.com/watch?v=W8erNabcz04 ，那 "="之後的就是影片id
video_id = "W8erNabcz04"


# 無限迴圈
while True:
    # 用youtube的api拿把影片裡面的留言都抓出來
    comment_thread_response = (
        youtube.commentThreads()
        .list(part="snippet", maxResults=1000, videoId=video_id)
        .execute()
    )

    # Youtube影片response結構參考，感謝 叼菸YT 留言分享，祝他中獎:D
    # {
    #     "videoId": "W8erNabcz04",
    #     "topLevelComment": {
    #         "kind": "youtube#comment",
    #         "etag": "_S-U7UZ7wR-pbIugGmR3P_kb9Ac",
    #         "id": "UgxMzf1cUjqWPsHve0V4AaABAg",
    #         "snippet": {
    #             "videoId": "W8erNabcz04",
    #             "textDisplay": "不要在乎別人怎麼看你 <br>因為根本沒有人在看你<br>😄😄😄抽我抽我",
    #             "textOriginal": "不要在乎別人怎麼看你 \n因為根本沒有人在看你\n😄😄😄抽我抽我",
    #             "authorDisplayName": "叼菸YT",
    #             "authorProfileImageUrl": "https://yt3.ggpht.com/ytc/AL5GRJXDNOLSTJ0sG4rKdMneKUSDFHv7yVn0do6mY8Fy7Q=s48-c-k-c0x00ffffff-no-rj",
    #             "authorChannelUrl": "http://www.youtube.com/channel/UCOaOtnyUqRUZS3iIdiMCD7A",
    #             "authorChannelId": {"value": "UCOaOtnyUqRUZS3iIdiMCD7A"},
    #             "canRate": True,
    #             "viewerRating": "none",
    #             "likeCount": 0,
    #             "publishedAt": "2023-03-20T16:19:02Z",
    #             "updatedAt": "2023-03-20T16:19:02Z",
    #         },
    #     },
    #     "canReply": True,
    #     "totalReplyCount": 0,
    #     "isPublic": True,
    # }

    print("有 " + str(len(comment_thread_response["items"])) + " 個留言")
    # 遍歷API傳回來的資料，依造json的結構，把需要的資料拿出來
    for item in comment_thread_response["items"]:
        # 把回應的總數拿出來
        total_replay_count = item["snippet"]["totalReplyCount"]
        # 把留言拿出來
        user_comment_text = item["snippet"]["topLevelComment"]["snippet"][
            "textOriginal"
        ]
        # 把留言的id拿出來，要利用這個給下一個api來做留言回應
        user_comment_id = item["snippet"]["topLevelComment"]["id"]

        # 如果回應的總數是0，表示還沒被回應過
        if total_replay_count == 0:
            # 跟總程式沒關係，用來錄影片用的XD
            print(user_comment_text)
            print(" ")

            # # 用留言跟留言id製做一個youtube_comment留言物件
            youtube_comment = YoutubeModule.YoutubeComment(
                user_comment_id, user_comment_text
            )

            # 把留言文字送去給Open API，並存下GPT傳回來的文字
            gpt_response = get_open_ai_api_chat_response(
                "請你用幽默的口氣回覆這個留言：" + youtube_comment.user_comment_text
            )

            # 把youtube的api物件、GPT傳回來的文字還有留言id送到youtube_comment留言物件裡面的一個方程
            # 那個方程會執行回覆功能
            youtube_comment.gpt_send_comment_to_youtube(
                youtube, gpt_response, youtube_comment.user_comment_id
            )
            # 暫停個十五秒，讓免費的API用量緩一緩
            time.sleep(15)
    # 暫停60秒在重新重來整個過程
    time.sleep(60)
