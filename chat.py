import sys
import argparse
import subprocess

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from helpers.functions import (
    DEFAULT_MODEL_PATH,
    get_available_models,
    get_model_and_configs,
)

PROMPT_HISTORY_FILE = ".prompt_history"

parser = argparse.ArgumentParser(description="Local LLM chat")
parser.add_argument(
    "model_path", nargs="?", default=DEFAULT_MODEL_PATH, help="The model path"
)
parser.add_argument(
    "-m", "--models", action="store_true", help="List available models and exit"
)
parser.add_argument(
    "-c", "--clear-model-cache", action="store_true", help="Clear model cache"
)
args = parser.parse_args()
if args.models:
    print("Available models:")
    for model in get_available_models():
        print(model)
    sys.exit(0)
if args.clear_model_cache:
    print("Model cache cleanup... ", end="")
    result = subprocess.run(
        ["rm", "-f", "model_cache/*"], capture_output=True, text=True, check=True
    )
    returncode = result.returncode
    if returncode == 0:
        print("done.")
    else:
        print(f"Error: {returncode}")
    sys.exit(result.returncode)
model_path = args.model_path


def main():
    pipe, config = get_model_and_configs(model_path)
    history = FileHistory(PROMPT_HISTORY_FILE)
    try:
        while True:
            user_input = prompt("Prompt> ", history=history)
            print("AI: ", end="", flush=True)
            pipe.generate(user_input, config, lambda x: print(x, end="", flush=True))
            print("\n")
    except (EOFError, KeyboardInterrupt):
        pass


if __name__ == "__main__":
    main()
