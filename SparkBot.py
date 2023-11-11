import streamlit as st
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import Count_db


import websocket  # 使用websocket_client
answer = ""

# appid = "2aa903c6"     #填写控制台中获取的 APPID 信息
# api_secret = "NmQxOTUzYWQ4YTBkNjZjZTZlOWQyMGFl"   #填写控制台中获取的 APISecret 信息
# api_key ="7f20fa7bdc0a1eb59141f6c240a793f8"    #填写控制台中获取的 APIKey 信息

# #用于配置大模型版本，默认“general/generalv2”
# #和云端环境的服务地址
# # domain = "general"   # v1.5版本
# # Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# domain = "generalv2"    # v2.0版本
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,one,two):
    print(" ")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain= ws.domain,question=ws.question))
    ws.send(data)

# 收到websocket消息的处理
def on_message(ws, message):
    # global all_message
    
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        # print(content,end ="")
        
        global answer
        answer += content
        # print(1)
        if status == 2:
            # st.info(all_message)
            ws.close()
            


def gen_params(appid, domain,question):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "random_threshold": 0.5,
                "max_tokens": 2048,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def main(appid, api_key, api_secret, Spark_url,domain, question):
    # print("星火:")
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

text =[]

# length = 0

def getText(role,content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    
# def get_response(input_text):
#     text.clear()
#     question = checklen(getText("user", input_text))
#     SparkApi.answer = ""
#     response = SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
#     getText("assistant", SparkApi.answer)
#     return response

if __name__ == '__main__':
    st.title("🦜🔗 Spark Quickstart App")
    st.markdown(f"""
                <style>
                .stApp {{background-image: url("https://p.sda1.dev/13/626f8613d929e132f877b7baaff7341c/cool-background _1_.png"); 
                        background-attachment: fixed;
                        background-size: cover}}
            </style>
            """, unsafe_allow_html=True)
    st.markdown('#### 请在下方输入您的问题，我将尽力为您解答。')
    sidebar = st.sidebar

    # 在侧边栏上添加标题和一些文本
    sidebar.title('SideBar!')
    sidebar.markdown("""
    - **按下回车键或点击Send发送消息**。

    - 后续功能正在开发中，敬请期待😋。
    """)
    sidebar.markdown(f'- This page has been run for `{Count_db.count_main()}` times!😋')
    sidebar.markdown('`Thanks for your support!😋`')
    Input = st.text_input('您想问些什么?')
    question = checklen(getText("user",Input))
    # SparkApi.answer =""
    answer = ""

    if st.button('Send') or question:
        # st.info(Input)
        # SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
        main(appid,api_key,api_secret,Spark_url,domain,question)
        # getText("assistant",SparkApi.answer)
        getText("assistant",answer)
        st.info(answer)
