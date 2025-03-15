from diffusers import DiffusionPipeline, AutoPipelineForText2Image
import torch
import os
from datetime import datetime
import argparse
import uuid

def generate_image_from_prompt(prompt: str, output_dir: str, model_choice: str) -> None:
    if model_choice == "v1-5":
        pipe = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5")
        pipe = pipe.to("mps")
        pipe.enable_attention_slicing()
        num_inference_steps = 25
        image = pipe(prompt, num_inference_steps=num_inference_steps).images[0]
    elif model_choice == "xl-base-1.0":
        pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16"
        ).to("mps")
        generator = torch.Generator("mps").manual_seed(31)
        image = pipe(prompt, generator=generator).images[0]
    else:
        raise ValueError("Invalid model choice. Please select 'v1-5' or 'xl-base-1.0'.")

    unique_filename = f"image_{uuid.uuid4().hex}.png"
    output_path = os.path.join(output_dir, unique_filename)
    image.save(output_path)
    
    log_message = f"Image saved to {output_path} at {datetime.now()}"
    print(log_message)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an image from a text prompt using a diffusion model.")
    parser.add_argument('--prompt', type=str, default="a photo of an astronaut riding a horse on mars", help='The text prompt to generate an image from.')
    parser.add_argument('--model', type=str, choices=['v1-5', 'xl-base-1.0'], default='v1-5', help='The model to use for image generation.')

    args = parser.parse_args()
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    output_dir = os.path.join(desktop_path, "image_output")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Using prompt: {args.prompt}")
    print(f"Using model: {args.model}")
    
    generate_image_from_prompt(args.prompt, output_dir, args.model)

if __name__ == "__main__":
    main()
