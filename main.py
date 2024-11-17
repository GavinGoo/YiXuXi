# coding:utf-8
import os
from os import getenv
import requests
import json
from flask import Flask, render_template, request, session, abort
from flask_session import Session
from waitress import serve
from werkzeug.exceptions import default_exceptions
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import WSGIRequestHandler
import re
from datetime import datetime
import logging
import traceback
from cmd_args import parse_args
import jwt
import time
import secrets
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from appdirs import user_config_dir
from os.path import join

from utils import Console

USER_CONFIG_DIR = getenv('USER_CONFIG_DIR', user_config_dir('Yixuxi'))

app = Flask(__name__, static_folder="assets", template_folder="templates")
app.wsgi_app = ProxyFix(app.wsgi_app, x_port=1)

app.secret_key = secrets.token_hex(16)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = join(USER_CONFIG_DIR, 'session')
Session(app)

app.config["STATIC_VERSION"] = "v20241107"

# app.config["LOG_FILE"] = f"{join(USER_CONFIG_DIR, 'log')}/py.log"
# app.config["LOG_LEVEL"] = logging.INFO

# for ex in default_exceptions:
#     app.register_error_handler(ex, __handle_error)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def validate_request():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            referer = request.headers.get('Referer', '')
            if not referer.startswith(request.host_url):
                abort(403, "非法的请求来源")
            
            user_agent = request.headers.get('User-Agent', '')
            # if not user_agent or any(ua in user_agent.lower() for ua in UA_BLACKLIST):    # 建议在 Nginx 层处理
            if not user_agent:
                abort(444, "非法的请求方式")

            if request.method == "POST":
                token = session.get('csrf_token')
                if not token or token != request.headers.get('X-CSRF-Token'):
                    abort(403, "CSRF token 验证失败")

            return f(*args, **kwargs)
        return decorated_function
    return decorator

"""""
初始化
"""""
def init(args):
    global UA_BLACKLIST, language_mapping, gptUrl, gptToken, gptModel, glmToken, deeplUrl, deeplApi, r_session, req_kwargs

    UA_BLACKLIST = [
                    'python',
                    'Python',
                    'aiohttp',
                    'urllib',
                    'curl',
                    'wget',
                    'HTTPie',
                    'httpie',
                    'Postman',
                    'postman',
                    'Go-http-client',
                    'go-http-client',
                    'uni-app'
                ]
    
    language_mapping = {
        "BG": "保加利亚语",
        "CS": "捷克语",
        "DA": "丹麦语",
        "DE": "德语",
        "EL": "希腊语",
        "EN": "英语",
        "EN-GB": "英语（英国）",
        "EN-US": "英语（美国）",
        "ES": "西班牙语",
        "ET": "爱沙尼亚语",
        "FI": "芬兰语",
        "FR": "法语",
        "HU": "匈牙利语",
        "ID": "印尼语",
        "IT": "意大利语",
        "JA": "日语",
        "KO": "韩语",
        "LT": "立陶宛语",
        "LV": "拉脱维亚语",
        "NB": "挪威语（书面挪威语）",
        "NL": "荷兰语",
        "PL": "波兰语",
        "PT": "葡萄牙语（未指定变体）",
        "PT-BR": "葡萄牙语（巴西）",
        "PT-PT": "葡萄牙语（除巴西葡萄牙语外的所有葡萄牙语变体）",
        "RO": "罗马尼亚语",
        "RU": "俄语",
        "SK": "斯洛伐克语",
        "SL": "斯洛文尼亚语",
        "SV": "瑞典语",
        "TR": "土耳其语",
        "UK": "乌克兰语",
        "ZH": "简体中文",
    }


    gptUrl = "https://api.openai.com/v1/chat/completions"
    gptToken = ""
    gptModel = "gpt-4o-mini"
    glmToken = ""

    deeplUrl = "https://api-free.deepl.com/v2/translate"
    deeplApi = ""

    r_session = requests.Session()

    req_kwargs = {
            'proxies': {
                'http': args.proxy,
                'https': args.proxy,
            } if args.proxy else None,
            'timeout': 100,
            'allow_redirects': False,
        }

    # Console.debug(req_kwargs)

    if args:
        if args.gpt_url:
            gptUrl = getenv("YIXUXI_GPT_URL", args.gpt_url)

        if args.deepl_url:
            deeplUrl =  getenv("YIXUXI_DEEPL_URL", args.deepl_url)

        if args.gpt_model:
            gptModel =  getenv("YIXUXI_GPT_MODEL", args.gpt_model)

        if args.gpt_token:
            gptToken =  getenv("YIXUXI_GPT_TOKEN", args.gpt_token)

        if args.glm_token:
            glmToken =  getenv("YIXUXI_GLM_TOKEN", args.glm_token)

        if args.deepl_api:
            deeplApi =  getenv("YIXUXI_DEEPL_API", args.deepl_api)

        if args.log:
            os.environ["YIXUXI_LOG"] = "Ture"

    Console.debug_b(
        """
                ██╗   ██╗██╗██╗  ██╗██╗   ██╗██╗  ██╗██╗
                ╚██╗ ██╔╝██║╚██╗██╔╝██║   ██║╚██╗██╔╝██║
                 ╚████╔╝ ██║ ╚███╔╝ ██║   ██║ ╚███╔╝ ██║
                  ╚██╔╝  ██║ ██╔██╗ ██║   ██║ ██╔██╗ ██║
                   ██║   ██║██╔╝ ██╗╚██████╔╝██╔╝ ██╗██║
                   ╚═╝   ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝
        """
    )

    Console.warn("Your Arguments:")
    for arg, value in vars(args).items():
        Console.debug(f"{arg}: {value}")
    Console.debug(f"config_dir: {USER_CONFIG_DIR}")
    Console.debug("")


def code2language(code):
    code = str(code)
    lang = language_mapping[code]

    return lang


def log(msg):
    # 获取时间
    date = datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S")

    # 获取IP
    ip = request.remote_addr
    if "X-Forwarded-For" in request.headers:
        ip = request.headers["X-Forwarded-For"].split(",")[0].strip()

    # 获取IP位置
    url = "https://whois.pconline.com.cn/ipJson.jsp?ip=" + str(ip)
    res = r_session.get(url, **req_kwargs).text
    if res:
        result_step1 = res.split("(", 2)[-1]
        result = result_step1.rsplit(")", 1)[0]
        addr = json.loads(result).get("addr")

    # 当请求内容长度大于50时截取
    if len(msg) > 50:
        msg = msg[:50] + "..."

    # 组装log文本
    """
    时间 |   IP |   IP位置 |   内容[:50]
    """
    content = date + " |   " + ip + " |   " + addr + " |   " + msg

    if not os.path.exists(join(USER_CONFIG_DIR, 'log')):
        os.makedirs(join(USER_CONFIG_DIR, 'log'))
    with open(file=f"{join(USER_CONFIG_DIR, 'log')}/YiXuXi.log", mode="a", encoding="utf-8") as f:
        Console.debug(content, file=f)

@staticmethod
def glm_generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        return None

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )

@staticmethod
def prefix_gpt(translate_content: str, source_language: str, target_language: str):
    first_prompt = f"""
                    role: "精通{target_language}的专业翻译"
                    profile:
                    - 经验: "曾参与《纽约时报》和《经济学人》{target_language}版的翻译工作"
                    - 技能: "对新闻和时事文章的翻译有深入的理解"
                    - 语言: "专业级{target_language}和{source_language}翻译能力"
                    skills:
                    - 翻译新闻事实和背景的准确性
                    - 保留特定{source_language}术语或名字，且在其前后加上空格
                    workflow:
                    - 第一步: "根据新闻内容直译，不遗漏任何信息"
                    - 第二步: "根据第一次直译的结果重新意译，使内容更通俗易懂，符合{target_language}表达习惯"
                    rules:
                    - 除译文外，绝不输出其他内容
                    - 准确传达新闻事实和背景
                    - 保留特定的{source_language}术语或名字，并在其前后加上空格
                    - 分成两次翻译，并打印每次结果
                    tools: "无"
                   """
    
    assisant_prompt = f"""
                        **翻译角色概况**

                        - **身份**: 经验丰富的{target_language}译者，尤其擅长新闻和时事类文章的翻译。曾在《纽约时报》和《经济学人》的{target_language}版工作，具有精准把握新闻语境的能力。
                        - **语言能力**: 精通{target_language}和{source_language}，能够在两种语言之间流畅转换。
                        
                        **工作流程**

                        1. **直译**：不遗漏原文信息，准确呈现事实和背景。
                        2. **意译**：基于直译结果，重新调整表述，确保语言符合{target_language}的表达习惯，保持自然流畅。
                        
                        **核心技能与要求**

                        - **绝对保密**：除译文外，绝不输出其他内容。
                        - **保留{source_language}术语**：对于特殊的{source_language}术语或名字，确保原文完整保留，且在术语前后留出空格。
                        - **新闻翻译的精准性**：在传达新闻事件的真实意图和背景时力求准确。
                        - **两次翻译**：将翻译过程分为两步，确保准确性和易读性。
                        
                        这个翻译流程有助于在兼顾原文准确性的基础上，使{target_language}读者更易理解新闻内容。如果有特定段落或内容希望尝试应用这种翻译流程，随时告诉我，我可以逐步展示两个翻译结果。
                       """
    
    data = {
                "messages": [
                {"role": "user", "content": first_prompt},
                {"role": "assistant", "content": assisant_prompt},
                {"role": "user", "content": f'"{translate_content}"'}
                ],
                "model": gptModel,
                "stream": True
            }
    
    # Console.warn(first_prompt)
    # Console.debug(assisant_prompt)

    return data


def translate_deeplx(content, source_language_code, target_language_code):
    """
    从deepl获取翻译
    """

    payload = json.dumps(
        {
            "text": content,
            "source_lang": source_language_code,
            "target_lang": target_language_code,
        }
    )

    if deeplApi == "":
        headers = {"Content-Type": "application/json"}
    else:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "DeepL-Auth-Key " + deeplApi,
        }

    # Console.debug('处理翻译请求：'+content)
    # response = session.request("POST", url, headers=header, json=data, stream=True, **req_kwargs)

    if source_language_code == "Classical Chinese":
        return "（抱歉，Deepl 无法翻译文言文 🥲）"

    response = r_session.request(
        "POST",
        deeplUrl,
        headers=headers,
        data=payload,
        **req_kwargs
    )

    # Console.debug('post_code：'+str(response.status_code))
    # Console.debug('deepl响应：'+ str(response.text))

    res = json.loads(response.text)
    # Console.debug('\n')
    # Console.warn("deepl响应：", end="")
    # Console.warn(res)

    # 错误兜底
    if res['code'] == 200 :
        text = res["alternatives"]
        if text is None or text == []:
            # Console.debug("deepl仅返回了一种译文")
            if res["data"]:
                text = str(res["data"])
            else:
                text = str(res)
            return text
        else:
            # Console.debug("deepl返回了多种译文")
            text_box = ""
            if res.get('data'):
                text_box = text_box + str(res['data']) + "<br>"
            for item in text:
                # Console.debug("deepl译文之一：" + str(item))
                text_box = text_box + str(item) + "<br>"
            return text_box
    elif res['message'] == "too many requests":
        return "<!DOCTYPE html><html><body><p>出错了:( <br> 你请求的翻译内容长度超出了Deepl官方1500tokens的限制 </p></body></html>"
    else:
        return "<!DOCTYPE html><html><body><p>出错了:( <br> 错误消息：" + str(res['message']) +" </p></body></html>"


def translate_gpt(content, source_language_code, target_language_code):
    """
    从gpt获取翻译
    """

    global glmToken, gptToken
    
    if glmToken:
        gptToken = glm_generate_token(glmToken, 3600)
        
    header = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        "Authorization": "Bearer " + gptToken}

    if source_language_code == "auto":
        chat_data = prefix_gpt(content, "源语言", code2language(target_language_code))

    elif source_language_code == "Classical Chinese":
        chat_data = prefix_gpt(content, "文言文", code2language(target_language_code))

    else:

        chat_data = prefix_gpt(content, code2language(source_language_code), code2language(target_language_code))

    # Console.debug("开始流式请求")
    # Console.debug("请求数据：")
    # Console.debug(chat_data)

    # 请求接收流式数据
    try:
        response = r_session.request(
            "POST",
            gptUrl,
            headers=header,
            json=chat_data,
            stream=True,
            **req_kwargs
        )

        # Console.debug('GPT: resp_code：'+str(response.status_code))

        # 判断是否为cf错误页，错误页会！暴露服务器ip！
        # 触发时报错：return app.response_class(gpt_response(), mimetype='application/json'): TypeError: 'str' object is not callable
        # 暂时通过后面捕获这个error解决(太菜了
        content_type = response.headers.get("Content-Type", "")
        if "text/html" in content_type or response.status_code != 200:
            Console.debug(
                datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S") + " 返回了错误页"
            )
            text = {
                # "content": "<!DOCTYPE html><html><body><p>出错了:(  请前往<a href='https://status.openai.com/' target='_blank'>OpenAI服务状态页</a>查看服务状态</p></body></html>"
                "content": "<!DOCTYPE html><html><body><p>出错了:(</p></body></html>"
            }
            text = json.dumps(text)
            return text
        # Console.debug("gpt" if not glmToken else "glm" + "响应：", end="")

        def generate():
            stream_content = str()
            i = 0
            for line in response.iter_lines():
                line_str = str(line, encoding="utf-8")
                if line_str.startswith("data:"):
                    if line_str.startswith("data: [DONE]"):
                        break

                    line_json = json.loads(line_str[5:])
                    if "choices" in line_json:
                        if len(line_json["choices"]) > 0:
                            choice = line_json["choices"][0]
                            if "delta" in choice:
                                delta = choice["delta"]
                                if "content" in delta:
                                    delta_content = delta["content"]
                                    # i += 1
                                    # if i < 40:
                                    #     Console.debug(delta_content, end="")
                                    # elif i == 40:
                                    #     match_error = re.search(
                                    #         delta_content, "<!DOCTYPE html>"
                                    #     )
                                    #     if match_error:
                                    #         return "ERROR!"
                                    #     else:
                                    #         Console.debug("...")
                                    stream_content = stream_content + delta_content
                                    yield delta_content

                elif len(line_str.strip()) > 0:
                    # Console.debug(line_str)
                    yield line_str

    except Exception as e:
        # ee = e
        ee = traceback.print_exc()
        # def generate():
        #     yield "request error:\n" + str(ee)

        return "<!DOCTYPE html><html><body><p>出错了:(</p></body></html>"

    return generate


@app.after_request
def after_request(response):
    Console.info(
        "[{}] {} {} {} - {}".format(
        datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"), request.remote_addr, request.method, request.path, response.status_code)
    )

    return response


@app.before_request
def csrf_protect():
    if not session.get('csrf_token'):
        # Console.debug(secrets.token_hex(16))
        session['csrf_token'] = secrets.token_hex(16)

@app.context_processor
def inject_static_version():
    return {
        "static_version": app.config.get("STATIC_VERSION"),
        "csrf_token": session.get('csrf_token')
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate/deepl", methods=["GET", "POST"])
@validate_request()
# @limiter.limit("10 per minute")
def deepl_translate_request():
    send_message = request.values.get("send_message").strip()
    source_language_code = request.values.get("source_language").strip()
    target_language_code = request.values.get("target_language").strip()
    # if len(send_message) > 50:
    #     Console.debug("收到翻译请求：" + send_message[:50] + "...")
    # else:
    #     Console.debug("收到翻译请求：" + send_message)
    # Console.debug("源语言：" + source_language_code)
    # Console.debug("目标语言：" + target_language_code)
    deepl_response = translate_deeplx(
        send_message, source_language_code, target_language_code
    )
    # gpt_response = translate_gpt(send_message)

    return deepl_response


@app.route("/translate/gpt", methods=["GET", "POST"])
@validate_request()
# @limiter.limit("10 per minute")
def gpt_translate_request():
    try:
        send_message = request.values.get("send_message").strip()
        source_language_code = request.values.get("source_language").strip()
        target_language_code = request.values.get("target_language").strip()
        # Console.debug('GPT 收到翻译请求：'+send_message)

        if getenv("YIXUXI_LOG") == "True" or args.log:
            log(send_message)

        gpt_response = translate_gpt(
            send_message, source_language_code, target_language_code
        )

        return app.response_class(gpt_response(), mimetype="application/json")
    
    except Exception as e:
        ee = traceback.print_exc()
        Console.warn(ee)
        return "<!DOCTYPE html><html><body><p>出错了:(</p></body></html>"


if __name__ == "__main__":
    args = parse_args()
    init(args)
    WSGIRequestHandler.protocol_version = 'HTTP/1.1'
    serve(app, host=args.host, port=args.port, ident=None, threads=args.threads, _quiet=False)
