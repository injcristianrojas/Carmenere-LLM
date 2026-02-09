import argparse
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from helpers.functions import get_model_and_configs, DEFAULT_MODEL_PATH

PROMPT_HISTORY_FILE = ".prompt_history"

parser = argparse.ArgumentParser(description="Test")
parser.add_argument(
    "model_path", nargs="?", default=DEFAULT_MODEL_PATH, help="The model path"
)
args = parser.parse_args()
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
