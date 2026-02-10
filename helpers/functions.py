import os
import openvino_genai as ov_genai

MODELS_PATH = "models"
DEFAULT_MODEL_PATH = f"{MODELS_PATH}/qwen_coder_3b_ov"


def get_model_and_configs(
    model_path, max_tokens=512, do_sample=True, temperature=0.6, top_p=0.9
):
    device = "GPU"
    print(f"Loading {model_path} to {device}... ", end="")
    pipe = ov_genai.LLMPipeline(
        model_path, device, PERFORMANCE_HINT="LATENCY", CACHE_DIR="model_cache"
    )
    config = ov_genai.GenerationConfig()
    config.max_new_tokens = max_tokens
    config.do_sample = do_sample
    config.temperature = temperature
    config.top_p = top_p
    print("Ready (Iris Xe Optimized)\n")
    return pipe, config


def get_available_models():
    entries = os.listdir(MODELS_PATH)
    subfolders = [
        entry for entry in entries if os.path.isdir(os.path.join(MODELS_PATH, entry))
    ]
    return subfolders
