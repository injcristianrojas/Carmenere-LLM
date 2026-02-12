import time
import json
import queue
import uvicorn
import threading
import argparse
import openvino_genai as ov_genai
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict
from helpers.functions import get_model_and_configs, DEFAULT_MODEL_PATH

parser = argparse.ArgumentParser()
parser.add_argument(
    "model_path", nargs="?", default=DEFAULT_MODEL_PATH, help="The model path"
)
args = parser.parse_args()
model_path = args.model_path

pipe, gen_config = get_model_and_configs(model_path)

app = FastAPI()


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    model: str
    messages: list
    stream: bool = False


def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join([b.get("text", "") for b in content if b.get("type") == "text"])
    return str(content)


@app.get("/v1/models")
async def list_models():
    return {"object": "list", "data": [{"id": "local_openvino", "object": "model"}]}


@app.post("/v1/chat/completions")
async def chat(request: ChatRequest):
    prompt = extract_text(request.messages[-1]["content"])
    chat_id = f"chat-{int(time.time())}"

    if not request.stream:
        # Standard non-streaming logic
        result = pipe.generate(prompt, gen_config)
        return {
            "id": chat_id,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": str(result)},
                    "finish_reason": "stop",
                }
            ],
        }

    # --- STREAMING LOGIC ---
    token_queue = queue.Queue()

    def streamer_callback(token: str):
        # This is called by the OpenVINO engine for every new word
        token_queue.put(token)
        return ov_genai.StreamingStatus.RUNNING

    def run_inference():
        # Run the heavy GPU work in a separate thread so the web server doesn't freeze
        pipe.generate(prompt, gen_config, streamer_callback)
        token_queue.put(None)  # Sentinel to signal the end

    def event_generator():
        threading.Thread(target=run_inference).start()

        while True:
            token = token_queue.get()
            if token is None:
                break

            # Format the data chunk for Zed/OpenAI format
            chunk = {
                "id": chat_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": request.model,
                "choices": [
                    {"index": 0, "delta": {"content": token}, "finish_reason": None}
                ],
            }
            yield f"data: {json.dumps(chunk)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
