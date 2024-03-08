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
        "--debug",
        help="Enable debug mode",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--gpt-token",
        default="",
        help="OpenAI ChatGPT Token",
    )
    parser.add_argument(
        "--deepl-api",
        default="",
        help="DeepL API endpoint",
    )

    args, _ = parser.parse_known_args()
    return args
