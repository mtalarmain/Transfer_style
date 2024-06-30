import gradio as gr 
from diffusers import AutoPipelineForImage2Image
import json
from pathlib import Path

def load_prompt_presets(path_img_style):
    prompt_presets = {}
    for preset_path in Path(path_img_style).glob('*'):
        preset = json.loads(preset_path.read_text())
        prompt_presets[preset_path.stem] = preset
    return prompt_presets

# use from_pipe to avoid consuming additional memory when loading a checkpoint
pipeline_image2image = AutoPipelineForImage2Image.from_pretrained('stabilityai/sdxl-turbo').to("cuda")

path_img_style = './prompts/'
prompt_presets = load_prompt_presets(path_img_style)
preset_list = list(prompt_presets.keys())

def diffusion_model(prompt, img_input):
    image = pipeline_image2image(prompt, image=img_input, strength=0.5, guidance_scale=0.0, num_inference_steps=2).images[0]
    return image


with gr.Blocks() as demo:

    with gr.Row():
        img_input = gr.Image('Input')
        img_output = gr.Image('Output')

    gen_button = gr.Button('Generate')
    gen_button.click(diffusion_model, img_input, img_output)

    style_group = gr.Radio(
            label="Image style",
            choices=preset_list,
            interactive=True,
            value="Realistic"
        )