from diffusers import DiffusionPipeline
import os
from datetime import datetime

pipe = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5")
pipe = pipe.to("mps")

# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt).images[0]

# Save the image to the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
image_path = os.path.join(desktop_path, "astronaut_on_horse.png")
image.save(image_path)

# Log the action
log_message = f"Image saved to {image_path} at {datetime.now()}"
print(log_message)
