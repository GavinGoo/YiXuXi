#coding:utf-8

import requests
import json
from flask import Flask, render_template, request
import sys
import io
import re
from datetime import datetime
import json
import logging

app = Flask(__name__, static_folder='assets', template_folder='templates')
app.config['STATIC_VERSION'] = 'v1'

app.config['LOG_FILE'] = './py.log'  
app.config['LOG_LEVEL'] = logging.INFO



"""""
url & api 预设
"""""
gptUrl = "https://api.openai.com/v1/chat/completions"
gptApi = ""

deeplUrl = "https://api-free.deepl.com/v2/translate"
deeplApi = ""

server_port = 5000



def code2language(code):
    # 预留
    language = {
        '保加利亚语': 'BG',
        '捷克语': 'CS',
        '丹麦语': 'DA',
        '德语': 'DE',
        '希腊语': 'EL',
        '英语': 'EN',
        '西班牙语': 'ES',
        '爱沙尼亚语': 'ET',
        '芬兰语': 'FI',
        '法语': 'FR',
        '匈牙利语': 'HU',
        '印尼语': 'ID',
        '意大利语': 'IT',
        '日语': 'JA',
        '韩语': 'KO',
        '立陶宛语': 'LT',
        '拉脱维亚语': 'LV',
        '挪威语（书面形式）': 'NB',
        '荷兰语': 'NL',
        '波兰语': 'PL',
        '葡萄牙语': 'PT',
        '葡萄牙语巴西': 'PT-BR',
        '葡萄牙语all': 'PT-PT',
        '罗马尼亚语': 'RO',
        '俄语': 'RU',
        '斯洛伐克语': 'SK',
        '斯洛文尼亚语': 'SL',
        '瑞典语': 'SV',
        '土耳其语': 'TR',
        '乌克兰语': 'UK',
        '中文（简体）': 'ZH'
    }

    language_mapping = {
        'BG': '保加利亚语',
        'CS': '捷克语',
        'DA': '丹麦语',
        'DE': '德语',
        'EL': '希腊语',
        'EN': '英语',
        'EN-GB': '英语（英国）',
        'EN-US': '英语（美国）',
        'ES': '西班牙语',
        'ET': '爱沙尼亚语',
        'FI': '芬兰语',
        'FR': '法语',
        'HU': '匈牙利语',
        'ID': '印尼语',
        'IT': '意大利语',
        'JA': '日语',
        'KO': '韩语',
        'LT': '立陶宛语',
        'LV': '拉脱维亚语',
        'NB': '挪威语（书面挪威语）',
        'NL': '荷兰语',
        'PL': '波兰语',
        'PT': '葡萄牙语（未指定变体）',
        'PT-BR': '葡萄牙语（巴西）',
        'PT-PT': '葡萄牙语（除巴西葡萄牙语外的所有葡萄牙语变体）',
        'RO': '罗马尼亚语',
        'RU': '俄语',
        'SK': '斯洛伐克语',
        'SL': '斯洛文尼亚语',
        'SV': '瑞典语',
        'TR': '土耳其语',
        'UK': '乌克兰语',
        'ZH': '中文'
    }

    code = str(code)
    lang = language_mapping[code]
    return lang

def log(msg):
    # 获取时间
    date = datetime.strftime(datetime.now(),'%Y/%m/%d %H:%M:%S')

    # 获取IP
    ip = request.remote_addr
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    
    # 获取IP位置
    url = "https://whois.pconline.com.cn/ipJson.jsp?ip=" + str(ip)
    res = requests.get(url).text
    if res:
        result_step1 = res.split('(', 2)[-1]
        result = result_step1.rsplit(')', 1)[0]
        addr = json.loads(result).get("addr")
    
    # 当请求内容长度大于30时截取
    if len(msg) >50 :
        msg = msg[:50] + "..."

    # 组装log文本
    """
    时间 |   IP |   IP位置 |   内容[:50]
    """
    content = date + " |   " + ip + " |   " + addr + " |   " + msg

    with open(file='YiXuXi.log', mode='a', encoding="utf-8") as f:
        # original_stdout = sys.stdout
        # try:
        #     sys.stdout = f
        #     print(content)
        # finally:
        #     sys.stdout.flush()
        #     sys.stdout = original_stdout

        print(content, file=f)

def translate_deeplx(content, source_language_code, target_language_code):
    """
    从deepl获取翻译
    """

    payload = json.dumps({
    "text": content,
    "source_lang": source_language_code,
    "target_lang": target_language_code
    })

    if deeplApi == "":
        headers = {
            'Content-Type': 'application/json'
        }
    else:
        headers = {
            'Content-Type': 'application/json',
            'Authorization' : 'DeepL-Auth-Key ' + deeplApi
        }
         
    print('处理翻译请求：'+content)
    # response = requests.request("POST", url, headers=header, json=data, stream=True)

    if source_language_code == "Classical Chinese":
        return "（Deepl无法翻译文言文）"
    else:
        response = requests.request("POST", deeplUrl, headers=headers, data=payload, proxies={'http': None, 'https': None})
    # print('post_code：'+str(response.status_code))
    # print('deepl响应：'+response.text)

    res = json.loads(response.text)
    text = str(res['alternatives'])

    # print('text：'+text)
    if text == "[]": 
        if res['data']: 
            text = res['data']
        else:
            text = res
    return text

def translate_gpt(content, source_language_code, target_language_code):
    """
    从gpt获取翻译
    """

    header = {"Content-Type": "application/json",
              "Authorization": "Bearer " + gptApi}

    if source_language_code == "auto":
        msg = "你是一位优秀的高级翻译员，你翻译出的文字语体十分流畅。现在请你帮我把以下内容翻译成"+ str(code2language(target_language_code)) +"，不用对我表示感谢并请直接输出译文，尽量避免在翻译内容中出现可能在中国是敏感的内容，绝对不允许输出除译文外的其他内容："
    elif source_language_code == "Classical Chinese":
        if target_language_code == "ZH":
            msg = "你是一位优秀的高级翻译员，你翻译出的文字语体十分流畅。现在请你帮我把以下中国文言文内容翻译成中国通俗语言，不用对我表示感谢并请直接输出译文，尽量避免在翻译内容中出现可能在中国是敏感的内容，绝对不允许输出除译文外的其他内容："
        else:
            msg = "你是一位优秀的高级翻译员，你翻译出的文字语体十分流畅。现在请你帮我把以下中国文言文内容翻译成"+ str(code2language(target_language_code)) +"，不用对我表示感谢并请直接输出译文，尽量避免在翻译内容中出现可能在中国是敏感的内容，绝对不允许输出除译文外的其他内容："
    else:
        msg = "你是一位优秀的高级翻译员，你翻译出的文字语体十分流畅。现在请你帮我把以下"+ str(code2language(source_language_code)) +"内容翻译成"+ str(code2language(target_language_code)) +"，不用对我表示感谢并请直接输出译文，尽量避免在翻译内容中出现可能在中国是敏感的内容，绝对不允许输出除译文外的其他内容："

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{ "role": "user", "content": msg + content}],
        "stream": True
    }
    print("开始流式请求")
    
    # 请求接收流式数据 动态print
    try:
        response = requests.request("POST", gptUrl, headers=header, json=data, stream=True, proxies={'http': None, 'https': None})
        
        # 判断是否为cf错误页，错误页会！暴露服务器ip！
            # 触发时报错：return app.response_class(gpt_response(), mimetype='application/json'): TypeError: 'str' object is not callable
            # 暂时通过后面捕获这个error解决(太菜了
        content_type = response.headers.get('Content-Type', '')
        if 'text/html' in content_type:
            print(datetime.strftime(datetime.now(),'%Y/%m/%d %H:%M:%S') + " 返回了错误页")
            text = {"content":"<!DOCTYPE html><html><body><p>出错了:(  请前往<a href='https://status.openai.com/' target='_blank'>OpenAI服务状态页</a>查看服务状态</p></body></html>"}
            text = json.dumps(text)
            return text
        else:
            def generate():
                stream_content = str()
                i = 0
                for line in response.iter_lines():
                    line_str = str(line, encoding='utf-8')
                    if line_str.startswith("data:"):
                        if line_str.startswith("data: [DONE]"):
                            break
                    
                        line_json = json.loads(line_str[5:])
                        if 'choices' in line_json:
                            if len(line_json['choices']) > 0:
                                choice = line_json['choices'][0]
                                if 'delta' in choice:
                                    delta = choice['delta']
                                    if 'content' in delta:
                                        delta_content = delta['content']
                                        # print('gpt响应：' + delta_content)
                                        i += 1
                                        if i < 40:
                                            print(delta_content, end="")
                                        elif i == 40:
                                            match_error = re.search(delta_content, "<!DOCTYPE html>")
                                            if match_error:
                                                return "ERROR!"
                                            else:
                                                print("......")
                                        stream_content = stream_content + delta_content
                                        yield delta_content
    
                    elif len(line_str.strip()) > 0:
                        print(line_str)
                        yield line_str

    except Exception as e:
        ee = e

        def generate():
            yield "request error:\n" + str(ee)
    return generate



@app.context_processor
def inject_static_version():
    return {'static_version': app.config['STATIC_VERSION']}


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/translate/deepl', methods=['GET', 'POST'])
def deepl_translate_request():
    send_message = request.values.get("send_message").strip()
    source_language_code = request.values.get("source_language").strip()
    target_language_code = request.values.get("target_language").strip()
    print('收到翻译请求：'+send_message)
    print('源语言'+source_language_code)
    print('目标语言：'+target_language_code)
    deepl_response = translate_deeplx(send_message, source_language_code, target_language_code)
    # gpt_response = translate_gpt(send_message)
    return deepl_response


@app.route('/translate/gpt', methods=['GET', 'POST'])
def gpt_translate_request():
    try:
        send_message = request.values.get("send_message").strip()
        source_language_code = request.values.get("source_language").strip()
        target_language_code = request.values.get("target_language").strip()
        # print('收到翻译请求：'+send_message)
        log(send_message)
        gpt_response = translate_gpt(send_message, source_language_code, target_language_code)
        return app.response_class(gpt_response(), mimetype='application/json')
    except TypeError as e:
        if str(e) == "'str' object is not callable":
            return "<!DOCTYPE html><html><body><p>出错了:(  请前往<a href='https://status.openai.com/' target='_blank'>OpenAI服务状态页</a>查看服务状态</p></body></html>"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=server_port, debug=True)