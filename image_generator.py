import openvino_genai as ov_genai
from PIL import Image

device = "GPU"
pipe = ov_genai.Text2ImagePipeline("./models/flux_schnell_ov/", device)

prompt = "A military pin that is an owl instead of an eagle"
image_tensor = pipe.generate(
    prompt, width=512, height=512, guidance_scale=0.0, num_inference_steps=4
)
image = Image.fromarray(image_tensor.data[0])
image.save("cat.png")
