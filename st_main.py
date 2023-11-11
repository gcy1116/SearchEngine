import streamlit as st
import SparkBot
import Count_db
import QnA_db

# appid = "2aa903c6"     #填写控制台中获取的 APPID 信息
# api_secret = "NmQxOTUzYWQ4YTBkNjZjZTZlOWQyMGFl"   #填写控制台中获取的 APISecret 信息
# api_key ="7f20fa7bdc0a1eb59141f6c240a793f8"    #填写控制台中获取的 APIKey 信息

appid = "c4075a29"
api_secret = "YmFlMTIwN2U3MDQzNWVmZTIyMzgxZjk5"
api_key = "6a074c0ded4929138650038b0125a7f7"

# 用于配置大模型版本，默认“general/generalv2”
# 和云端环境的服务地址
domain = "generalv3"   # v3.0版本
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
# domain = "generalv2"    # v2.0版本
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
st.title("🧐🔗 Search Assitant")
st.markdown("***Powered by Spark-API !!***")
st.markdown("---")

st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://p.sda1.dev/13/626f8613d929e132f877b7baaff7341c/cool-background _1_.png"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)
st.markdown('##### 请在下方输入您的问题，我将尽力为您解答。')

with st.sidebar:

# if sidebar.button('***Change Model to v2***'):
#     domain = "generalv2"
#     Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"
#     st.markdown('Model changed to general v2.0')
#     # st.info('Model changed to general v2.0')

# if sidebar.button('***Change Back***'):
#     domain = "general"
#     Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"
#     st.markdown('Model changed to general v1.5')
#     # st.info('Model changed to general v1.5')

# 在侧边栏上添加标题和一些文本
    st.title('*侧栏提示 !*')
    st.markdown("""
    - **按下*回车键* 或点击`提交`发送消息**

    """)
    expander = st.expander("***用法提示🤗！！***")
    expander.markdown("""
    - 在使用时用户可以先输入：
    ```
    现在开始你将扮演一位法律领域的专家，我将向你询问法律相关的问题，希望你尽可能高质量地回答
    ```
    ***
    - 用户可以在描述完问题后让ai助手给出若干关键词，用户可以用这些关键词在搜索引擎中检索相关链接
        - 例如：
        ```
        我想知道blabla...请给出相关关键词，用于我在搜索引擎中检索
        ```
    """)
    
    st.markdown(f'- This page has been run for `{Count_db.count_main()}` times!🤫')
    st.markdown('- 后续功能正在开发中，敬请期待😈')
    st.markdown('`Thanks for your support!😆`')
    css_style = """
    <style>
    .text{
        font-size: 15px;
        text-shadow: 5px 5px 5px;
        background-color: rgba(179, 179, 179, 0.5);
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)
    st.markdown('<p class="text">该网页的作者是<i><strong>喜多郁代 CODE.ver aka.KKKita😎</strong><br>  欢迎访问  </i><a href="https://github.com/gcy1116">GitHub</a></p>', unsafe_allow_html=True)

QnA_db.generate_user_id()
userID = st.session_state['user_id']

with st.form("my_form"):
    Input = st.text_input('您想问些什么?')
    send = st.form_submit_button("提交")
question = SparkBot.checklen(SparkBot.getText("user",Input))
SparkBot.answer = ""

if send:
    SparkBot.main(appid,api_key,api_secret,Spark_url,domain,question)
    SparkBot.getText("assistant",SparkBot.answer)
    # st.info(SparkBot.answer)
    QnA_db.insert_text_db(userID, Input,SparkBot.answer)
    QnA_db.show_text_db(userID)

if st.button("清除历史记录"):
    QnA_db.delete_records_by_user_id(userID)
    st.empty()
    # st.rerun()
    st.info('History Cleared')
