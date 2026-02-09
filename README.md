# Carmenere-LLM

Personal project designed to have a multi-purpose local LLM
running in my limited GPU machine (Intel Iris Xe). It has two
components:

* Local chatbot for the terminal
* Local LLM server for IDE use ([Zed](https://zed.dev/), specifically)

This works in a Linux laptop, using Intel Iris Xe Graphics (RPL-U).

# Setup

This project uses [UV](https://docs.astral.sh/uv/). Install the dependencies:

```shell
uv sync
```

You will need a OpenVINO-compatible model. A catalog of them
is available in [this HuggingFace repository](https://huggingface.co/OpenVINO). 
I recommend downloading INT4-compressed models. Download
the application's default model using the hf tool:

```shell
hf download OpenVINO/Qwen2.5-Coder-3B-Instruct-int4-ov --local-dir models/qwen_coder_3b_ov
```

# Execute

## Local chatbot

Run using:

```shell
uv run chat.py [model_path]
```

Where `model_path` is the downloaded model's path. Defaults to models/qwen_coder_3b_ov.

![Chatbot running in terminal](chat.gif)

## Local server

Run using:

```shell
uv run server.py [model_path]
```

Where `model_path` is the downloaded model's path. Defaults to models/qwen_coder_3b_ov.
When using your IDE, configure it to point to an OpenAI-compatible API. The address is
http://127.0.0.1:8000/v1. Set whatever API key you want. The model's name
is `local_openvino`.


![Running in Zed](zed.png)
