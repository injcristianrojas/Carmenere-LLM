import openvino_genai as ov_genai

DEFAULT_MODEL_PATH = "models/qwen_coder_3b_ov"


def get_model_and_configs(model_path):
    device = "GPU"
    print(f"Loading {model_path} to {device}... ", end="")
    pipe = ov_genai.LLMPipeline(
        model_path, device, PERFORMANCE_HINT="LATENCY", CACHE_DIR="model_cache"
    )
    config = ov_genai.GenerationConfig()
    config.max_new_tokens = 512
    config.do_sample = True
    config.temperature = 0.6
    config.top_p = 0.9
    print("Ready (Iris Xe Optimized)\n")
    return pipe, config
