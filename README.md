<div align="center">
<img src="./assets/img/header.jpg" style="width:80px;height:80px;" />

<h1 align="center">译吁嚱</h1>

<h5 align="center">一个支持Deepl & ChatGPT翻译的网页</h5>

<h6 align="center">青天难上，仍慕青山</h6>
</div>

----

# 特性

- 自动 / 手动 切换夜间模式(Pico.css)
- ChatGPT/ChatGLM翻译支持流式输出
- 自动根据译文长度同步拉伸文本框
- 可自由调节原文 / 译文 文本框高度
- 当源语言选定为"自动识别"时，gpt自己识别(随缘)
- 一键复制
- 一键粘贴原文(浏览器需授权读取剪贴板，移动端除Safari外可能无效)
- 悬挂猫一键滚动至顶部
- 甚至能让ChatGPT/ChatGLM翻译文言文(源语言选择"文言文")(质量不如文心一言(仅图一乐)
- 日志输出(仅当调用ChatGPT/ChatGLM翻译时，可通过日志进行越狱行为审查)(格式：时间 |  IP |  IP位置 |  请求内容[:30])



# 界面预览

## PC

![dark](./screenshot/dark.jpg)

![light](./screenshot/light.jpg)

## Phone

<div style="display: flex;">
<img src="./screenshot/mobie_light.png" alt="mobie" style="zoom: 50%;width:400px;" />
<img src="./screenshot/mobie_dark.png" alt="mobie" style="zoom: 50%;width:400px;" />
</div>

> width < 1100px



# 使用

*开发环境的python版本为3.10.0，理论3.8及以上都可以(使用Docker的朋友无视此条)

> 检查python版本：`python --version`
>
> 附：[linux升级python2为python3_python2 升级python3-CSDN博客](https://blog.csdn.net/weixin_40283268/article/details/133797294)
>
> 不明白/嫌麻烦的朋友们可以直接先往下走试试:)
>



程序参数：

```
--port: 监听端口，默认：5000
--host: 监听地址，默认：0.0.0.0
--proxy: 代理设置，格式：protocol://user:pass@ip:port
--gpt-url: ChatGPT/ChatGLM API 地址，默认：https://api.openai.com/v1/chat/completions
--gpt-token: ChatGPT API Key
--glm-token: ChatGLM API Key
--deepl-url: Deepl API 地址，默认：https://api-free.deepl.com/v2/translate
--deepl-api: Deepl API Key
--log: 请求ChatGPT/ChatGLM时记录请求内容，默认不启用
```



环境变量：

```
YIXUXI_PORT: 监听端口，默认：5000
YIXUXI_HOST: 监听地址，默认：0.0.0.0
YIXUXI_PROXY: 代理设置，格式：protocol://user:pass@ip:port
YIXUXI_GPT_URL: ChatGPT/ChatGLM API 地址，默认：https://api.openai.com/v1/chat/completions
YIXUXI_GPT_TOKEN: ChatGPT API Key
YIXUXI_GLM_TOKEN: ChatGLM API Key
YIXUXI_DEEPL_URL: Deepl API 地址，默认：https://api-free.deepl.com/v2/translate
YIXUXI_DEEPL_API: Deepl API Key
YIXUXI_LOG_SWITCH: 请求ChatGPT/ChatGLM时记录请求内容，默认不启用
```

> 使用Docker仅配置环境变量即可，无视上述`程序参数`。



## 运行

- Docker运行

    ```
    docker pull gavingooo/yixuxi:latest
    ```
	```
	#以Deeplx+ChatGLM为例: 
	
	docker run -d --restart=unless-stopped --name yixuxi -p 5000:5000 -e YIXUXI_DEEPL_URL=<Your Deeplx API Url> -e YIXUXI_GPT_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions -e YIXUXI_GLM_TOKEN=<Your Zhipu AI key> gavingooo/yixuxi:latest
	```



- 本地运行

    1. 下载本项目到本地
       ```bash
       $ git clone https://github.com/GavinGoo/YiXuXi.git
       ```

    2. 终端下进入本项目根目录
       ```bash
       $ cd YiXuXi
       ```

    3. 安装依赖
       ```bash
       pip install -r requirements.txt
       ```

       >
       > 或使用venv：
       >
       > Python: `python -m venv venv`
       >
       > Windows: `./venv/Scripts/activate`
       >
       > Linux: `source ./venv/bin/activate`

    5. 运行
       ```bash
       python main.py --gpt-token <your-gpt-token> --deepl-api <your-deepl-api>
       ```

       >
       > 端口默认5000，可通过 `--port <port>` 更改
       >
       > 更多选项请使用 `--help` 查看

    6. 浏览器访问`http://127.0.0.1:5000`即可享用:)
       >
       >另：后台运行：`nohup python ./main.py --gpt-token <your-gpt-token> --deepl-api <your-deepl-api> &`，终端日志会输出到项目根目录下的`nohup.out`
       >
       >关闭后台：`ps aux | grep python`，第二列的数字即进程PID，`kill -9 <PID>`
       
       

> 还有很多待完善的地方，在此表示抱歉



# 技巧

1. 通过[DeepLX](https://github.com/OwO-Network/DeepLX)项目(无需token!)作为Deepl接口(感谢`OwO-Network`大佬)

2. 通过`zhile`大佬[wozulong](https://github.com/wozulong)的接口[DeepLX 使用 | FakeOpen Doc](https://fakeopen.org/DeepLX/)作为Deepl接口(可避免"rate limit") & [OpenAI API 相关 | FakeOpen Doc](https://fakeopen.org/Pandora/#openai-api-相关)作为GPT接口(感谢`zhile`大佬)

> 如果使用了大佬的项目/接口，建议修改页面中页脚`footer`的链接&名称



# 感谢

- [DeepLX](https://github.com/OwO-Network/DeepLX)项目`OwO-Network`大佬，项目灵感的起源
- `zhile`大佬[wozulong](https://github.com/wozulong)，fakeopen接口
- [ChatGPT-Web](https://github.com/LiangYang666/ChatGPT-Web)项目，流式输出的实现
- [injet-zhou](https://github.com/injet-zhou)的PR
- 切图仔群友们
