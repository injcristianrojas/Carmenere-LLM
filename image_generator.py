import argparse
import openvino_genai as ov_genai
from PIL import Image

parser = argparse.ArgumentParser(description="Local image generator")
parser.add_argument("prompt", nargs="?", help="Description of the image")
parser.add_argument("file", nargs="?", help="File to write the image to")
args = parser.parse_args()
prompt = args.prompt


def main():
    device = "GPU"
    pipe = ov_genai.Text2ImagePipeline("./models/flux_schnell_ov/", device)
    image_tensor = pipe.generate(
        prompt, width=512, height=512, guidance_scale=0.0, num_inference_steps=4
    )
    image = Image.fromarray(image_tensor.data[0])
    image.save("cat.png")


if __name__ == "__main__":
    main()
