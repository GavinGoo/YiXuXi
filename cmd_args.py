import argparse

def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--port",
        help="Port to listen on",
        default=5000,
        type=int,
    )
    parser.add_argument(
        "--host",
        help="Host to listen on",
        default="0.0.0.0",
        type=str,
    )
    parser.add_argument(
        '--proxy',
        help='Use a proxy. Format: protocol://user:pass@ip:port',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        "--debug",
        help="Enable debug mode",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--gpt-url",
        default="https://api.openai.com/v1/chat/completions",
        help="OpenAI ChatGPT Url",
    )
    parser.add_argument(
        "--gpt-token",
        default="",
        help="OpenAI ChatGPT Token",
    )
    parser.add_argument(
        "--glm-token",
        default="",
        help="Zhipu AI Token",
    )
    parser.add_argument(
        "--deepl-url",
        default="https://api-free.deepl.com/v2/translate",
        help="DeepL API Url",
    )
    parser.add_argument(
        "--deepl-api",
        default="",
        help="DeepL API Key",
    )

    args, _ = parser.parse_known_args()
    return args
