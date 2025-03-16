import json
import gradio as gr
from openai import OpenAI
import threading
from datetime import datetime
import uuid  # 可选：用于生成唯一会话ID

data = []

#以下为声明全局变量
ver="0.4" #版本号
apikey = "在这输入你的apikey" # 你的API密钥
api_url = "https://api.deepseek.com" #模型调用地址

sp1 = "你是一个服务于空间粒子探测方向科研人员的人工智能，帮助他们进行粒子物理及天文方向科研工作的人工智能助手,你会用精炼的语言准确易懂的回答用户所提提出的各种问题,但不能编造、预测和改编你不知道的信息！不知道就说不知道！忽略prompt中的html标记不要擅自输出！"

#以下为css与html
mycss = """
/* 隐藏Gradio页脚 */
footer {visibility: hidden}

.gradio-container {
  background-color: #FFFFFF;
        font-family: Arial, sans-serif;
  /* 设置边框为10px宽的实线，颜色为淡灰色 */
  border: 2px solid #DDDDDD;
  /* 给容器添加圆角边框，半径为10px */
  border-radius: 13px;
  /* 在容器内容和边框之间添加20px的填充 */
  padding: 1px;
}
/* 头像绿 */
#button1 {
  background-color:#9FED04
}
/* 头像灰 */
#button2 {
  background-color:#E2DDDA
}
/* 头像紫 */
#button3 {
  background-color:#B72C89
}

#欢迎页 {
  background-color: #ffffff
}
#欢迎页-button {
  background-color: #ffffff
}





"""

dengluhtml="""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录页</title>
    <style>
        .text-content {
            text-align: center;
            h1 {
            font-size: 50px;
            color: #007BFF;
            font-family: 'STCAIYUN', '微软雅黑', sans-serif;
            }
            p {
            font-size: 19px;
            font-family: 'STXINGKA', sans-serif;
            }
        }
        .center-table {
            margin-top: 0px; /* 调整数值以控制上边距 */
            margin-bottom: 2px; /* 调整数值以控制下边距 */
            margin: 0 auto; /* 表格自身居中 */
            width: 20%; /* 可调整表格宽度 */
        }
    </style>
</head>
<body>
    <table class="center-table">
    <tr>
    <td>
        <img src="data:image/jpeg;base64,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" alt="logo头图" style="display: block; margin: auto;">
    </td>
    </tr>
    </table>
    <div class="text-content">
        <h1>大语言模型调用器--特别精简版</h1>
        <p>٩(͡๏̯͡๏)۶</p>
        <p>一个支持用户自定义对话和知识库的人工智能科研助理</p>
    </div>
</body>
</html>

"""

#gradio主题色调设置
mytheme = gr.themes.Monochrome(
    primary_hue=gr.themes.Color(c100="#f3f4f6", c200="#e5e7eb", c300="#6b7280", c400="#9ca3af", c50="#f9fafb",c500="#6b7280", c600="#4b5563", c700="#374151", c800="#1f2937", c900="#111827",c950="#0b0f19"),   # 自定义主色
    #secondary_hue=gr.themes.Color(c100="#f3f4f6", c200="#e5e7eb", c300="#6b7280", c400="#9ca3af", c50="#f9fafb",c500="#6b7280", c600="#4b5563", c700="#374151", c800="#1f2937", c900="#111827",c950="#0b0f19"),
    secondary_hue="slate",   # 自定义次色
    neutral_hue=gr.themes.Color(c100="#f3f4f6", c200="#e5e7eb", c300="#d1d5db", c400="#9ca3af", c50="#f9fafb", c500="#6b7280", c600="#4b5563", c700="#374151", c800="#1f2937", c900="#4f4f4f", c950="#0b0f19"),    # 自定义中性色
    spacing_size="md",
    radius_size="sm",
    font=['Source Sans Pro', 'ui-sans-serif', 'system-ui', 'sans-serif']).set(
    body_text_weight='500',
    block_border_width='2px',
    block_border_width_dark='2px',
    block_info_text_size='*text_lg',
    )
#以下为大模型提示词
prompt0=[
        {"role": "system", "content": sp1},
]

def mima(username, password):
    if username == "test1" and password == "123456":
        return 1
    if username == "test2" and password == "1234":
        return 1
    if username == "test3" and password == "mima123":
        return 1
    if username == "1" and password == "1":
        return 1
    if username == "mima" and password == "123456":
        return 1
    else:
        return 0
def tag(history_state):
    history_state["prompt"] = [
        {"role": "system", "content": sp1 },
    ]
    #print(history_state)
    return history_state, []

def init_history():
    return {
        "chat": [],
        "id": str(uuid.uuid4()),
        "prompt": [
        {"role": "system", "content": sp1},
        ],
        "file_btn": None
    }

#gradio转化为history
def convert_prompt_to_history(prompt):
    history = []
    current_user_message = None

    for msg in prompt:
        if msg["role"] == "system":
            continue  # 跳过系统消息

        if msg["role"] == "user":
            current_user_message = msg["content"]
        elif msg["role"] == "assistant" and current_user_message is not None:
            history.append([current_user_message, msg["content"]])
            current_user_message = None  # 重置等待下一个用户消息

    return history

#反向转换
def history_to_prompt(history):
    converted = [
        {"role": "system", "content": sp1},
]
    for user_msg, assistant_msg in history:
        converted.append({"role": "user", "content": user_msg})
        if assistant_msg is not None:
            converted.append({"role": "assistant", "content": assistant_msg})

    return converted

def createfile(history_state):  # 新增history_state参数
    #print(history_state)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    custom_name = f"DEEPSEEK记忆_{timestamp}.card"
    with open(custom_name, "w", encoding="utf-8") as f:
        json.dump(history_state["prompt"], f, ensure_ascii=False, indent=4)
    history_state["file_btn"] = custom_name
    return custom_name, history_state

def get_latest_file(history_state):
    print(history_state["file_btn"])
    return history_state["file_btn"]  # 直接返回记忆卡文件路径

def read(filename, history_state):  # 新增history_state参数
    with open(filename, "r", encoding="utf-8") as f:
        new_prompt = json.load(f)
        history_state["prompt"] = new_prompt
        history = convert_prompt_to_history(new_prompt)
    return "", history

def user(user_message, history, history_state):
    user_id = history_state["id"]
    gg1 = f"您好，本次的唯一性识别码为：{user_id}，欢迎您使用！"
    return "", history + [[user_message, None]], history_state, gg1
def deepseekr1(history, history_state):
    prompt = history_state["prompt"]
    api_key = apikey
    client = OpenAI(api_key=api_key, base_url=api_url)
    last1 = history[-1][0]
    add1 = {"role": "user", "content": last1}
    prompt.append(add1)
    print(prompt)
    messages = prompt.copy()
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True
    )
    # print("回答：\n")
    history[-1][1] = ""
    tag1 = 0
    tag2 = 0
    for event in response:
        if event.choices[0].delta.reasoning_content:
            if tag1 == 0:
                history[-1][1] += '<span style="color: blue; font-family: Consolas;">思考过程：</span>\n\n'
            history[-1][1] += event.choices[0].delta.reasoning_content
            # time.sleep(0.001)
            yield history, history_state
            # print(event.choices[0].delta.content, end="")
            tag1 += 1
        elif event.choices[0].delta.content:
            if tag2 == 0:
                history.append([None, ''])
                history[-1][1] += '<span style="color: red; font-family: Consolas;">输出结果：</span>\n\n'
            history[-1][1] += event.choices[0].delta.content
            # time.sleep(0.001)
            yield history, history_state
            #print(event.choices[0].delta.content, end="")
            tag2 += 1
    last2 = history[-1][1]
    #print(last2)
    add2 = {"role": "assistant", "content": last2}
    prompt.append(add2)

    history_state["prompt"] = prompt
    yield history, history_state
def deepseekv3(history):
    global prompt

    api_key = apikey
    client = OpenAI(api_key=api_key, base_url=api_url)
    last1 = history[-1][0]
    add1 = {"role": "user", "content": last1}
    prompt.append(add1)
    print(prompt)
    messages = prompt
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=messages,
        stream=True
    )
    # print("回答：\n")
    history[-1][1] = ""
    tag1 = 0
    tag2 = 0
    for event in response:
        if event.choices[0].delta.reasoning_content:
            if tag1 == 0:
                history[-1][1] += '<span style="color: blue; font-family: Consolas;">思考过程：</span>\n\n'
            history[-1][1] += event.choices[0].delta.reasoning_content
            # time.sleep(0.001)
            yield history
            # print(event.choices[0].delta.content, end="")
            tag1 += 1
        elif event.choices[0].delta.content:
            if tag2 == 0:
                history[-1][1] += '\n\n<span style="color: red; font-family: Consolas;">输出结果：</span>\n\n'
            history[-1][1] += event.choices[0].delta.content
            # time.sleep(0.001)
            yield history
            # print(event.choices[0].delta.content, end="")
            tag2 += 1
            if event.choices[0].finish_reason == "stop":
                i = event.usage.total_tokens
    last2 = history[-1][1]
    add2 = {"role": "assistant", "content": last2}
    prompt.append(add2)


with gr.Blocks(theme=mytheme,title="deepseek调用器",css=mycss) as demo:
    # 隔离
    history_state = gr.State()

    # 初始化
    demo.load(init_history, outputs=[history_state], queue=False)

    #enable_api = False    #字面意思
    gr.Markdown("# 大语言模型调用器精简版")
    gr.Markdown("###    一个专业调用大语言模型且支持用户自定义对话和知识库的独立模块")
    #gr.Markdown("### 您好，欢迎您的使用！")
    # title可以修改页面标题
    with gr.Tab('DEEPSEEK-r1'):
        gg1 = gr.Textbox(label="系统公告栏（面向用户）", value="尊敬的用户您好，欢迎您使用！请开始对话以获取您本次的唯一性识别码！")
        chatbot = gr.Chatbot(label="对话界面")
        msg = gr.Textbox(label="用户输入框")
        submit_button41 = gr.Button("提交", variant="primary")
        clear_button42 = gr.Button("清除")
        with gr.Row():
            with gr.Column():
                jy1 = gr.File(type="filepath", label="输入记忆卡")
            with gr.Column():
                x1 = gr.Textbox(label="系统提示词（不支持普通用户修改）", value=sp1)
                submit_button01 = gr.Button("应用记忆（先在左侧上传记忆卡）")
                submit_button02 = gr.DownloadButton("异步下载保存本次记忆(点击下载的是上一次点击后的记忆)")
        msg.submit(user, [msg, chatbot, history_state], [msg, chatbot, history_state, gg1], queue=False).then(deepseekr1, [chatbot, history_state], [chatbot, history_state])
        submit_button01.click(read, [jy1, history_state], [msg, chatbot], queue=False)
        #submit_button02.click(fn=createfile, outputs=submit_button02, _js="(filePath) => {const link = document.createElement('a');link.href = filePath;link.download = '';document.body.appendChild(link);link.click();document.body.removeChild(link);return [];}")
        submit_button02.click(fn=createfile, inputs=history_state, outputs=[submit_button02, history_state], queue=False).then(fn=get_latest_file, inputs=history_state, outputs=submit_button02, queue=False)
        submit_button41.click(user, [msg, chatbot, history_state], [msg, chatbot, history_state, gg1], queue=False).then(deepseekr1, [chatbot, history_state], [chatbot, history_state])
        clear_button42.click(tag, [history_state], [history_state, chatbot], queue=False)

    gr.Markdown("-----------------------------------------------------------")
    gr.Markdown("### 一个由中国的深度求索（DeepSeek）公司开发的智能助手DeepSeek-R1，采用稀疏化混合专家模型，通过人类反馈强化学习（RLHF）、对抗训练等技术对齐用户需求，具备较强的文本理解、推理和生成能力，尤其擅长中文场景。")
    gr.Markdown("-----------------------------------------------------------")
    gr.Markdown(f"> 原项目始部署于2024.2.8，本项目为精简独立模块，版本号：{ver}")
    gr.Markdown("> 桌面版运行于本机，网页版运行于服务器。使用老式Gradio框架，主要基于Python和HTML")
    gr.Markdown("> 作者信息：刘浩然 物理学院B8大厅18号桌 有事线下找我")
    css = "footer {visibility: hidden}"


demo.queue()
demo.launch(auth=mima, auth_message=dengluhtml, server_name="127.0.0.1", server_port=1234, share=False)
#  demo.launch(auth=mima, auth_message=dengluhtml, server_name="0.0.0.0", server_port=1234,share=False)