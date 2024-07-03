import gradio as gr 
from diffusers import ControlNetModel, AutoencoderKL, StableDiffusionXLControlNetPipeline
import json
from pathlib import Path
import numpy as np
import cv2
from PIL import Image
import torch

def load_prompt_presets(path_img_style):
    prompt_presets = {}
    for preset_path in Path(path_img_style).glob('*'):
        preset = json.loads(preset_path.read_text())
        prompt_presets[preset_path.stem] = preset
    return prompt_presets

cache_dir = ".hf_cache/" #path to load Stable Diffusion models
# use from_pipe to avoid consuming additional memory when loading a checkpoint
controlnet = ControlNetModel.from_pretrained("diffusers/controlnet-canny-sdxl-1.0", torch_dtype=torch.float16, cache_dir=cache_dir)
vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", torch_dtype=torch.float16, cache_dir=cache_dir)
pipe_sdxl_controlnet = StableDiffusionXLControlNetPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", controlnet=controlnet, vae=vae, torch_dtype=torch.float16, cache_dir=cache_dir).to("cuda")
pipe_sdxl_controlnet.enable_model_cpu_offload()
#pipe_controlnet.enable_xformers_memory_efficient_attention()

path_img_style = './prompts/'
prompt_presets = load_prompt_presets(path_img_style)
preset_list = list(prompt_presets.keys())

def diffusion_model(img_input, style_group, steps_slider, guidance_scale, controlnet_conditioning_scale):
    prompt_style_positive = prompt_presets[style_group]['positive']
    prompt_style_negative = prompt_presets[style_group]['negative']
    image = cv2.Canny(img_input, 100, 200)
    image = image[:, :, None]
    image = np.concatenate([image, image, image], axis=2)
    canny_image = Image.fromarray(image)
    #controlnet_conditioning_scale = 0.5  # recommended for good generalization
    image = pipe_sdxl_controlnet(prompt=prompt_style_positive, negative_prompt=prompt_style_negative, image=canny_image, controlnet_conditioning_scale=controlnet_conditioning_scale, guidance_scale = guidance_scale, num_inference_steps=steps_slider).images[0]

    return image


with gr.Blocks() as demo:

    with gr.Row():
        img_input = gr.Image('Input')
        img_output = gr.Image('Output')

    gen_button = gr.Button('Generate')

    style_group = gr.Radio(
            label="Image style",
            info="Choose image style",
            choices=preset_list,
            interactive=True,
            value="Realistic"
        )

    steps_slider = gr.Slider(
            label="Generation steps",
            info="Control the trade-off between quality and speed. Higher "
                 "values means more quality but more processing time",
            interactive=True,
            minimum=10,
            maximum=100,
            value=30,
            step=1,
        )

    guidance_scale = gr.Slider(
            label="Guidance Scale",
            info="Higher values means the generated image will be closer to text prompt.",
            interactive=True,
            minimum=0,
            maximum=10,
            value=5.0,
            step=0.5,
        )
    
    controlnet_conditioning_scale = gr.Slider(
            label="Controlnet Conditioning",
            info="Higher values means the generated image will be closer to input image in terms of canny image. 0.5 is the best trade-off.",
            interactive=True,
            minimum=0.1,
            maximum=0.9,
            value=0.5,
            step=0.1,
        )

    gen_button.click(diffusion_model, [img_input, style_group, steps_slider, guidance_scale, controlnet_conditioning_scale], img_output)

demo.launch()