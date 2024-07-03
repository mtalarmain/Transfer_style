# Transfer_style

## 0. Install and launch Gradio App

Git clone the repo. Then install the dependencies:

```
pip install -r requirements.txt
```

To launch gradio interface:

```
python gradio_app.py
```

## 1. Load Input Image

You can load the input image on the Input section. Then it is possible to choose the parameter of the model depending on your needs. 

![](https://github.com/mtalarmain/Transfer_style/blob/main/image/ouput/condition_scale/couple_pixar_03.jpgs)

## 2. Parameters

Generation steps: Control the trade-off between quality and speed. Higher values means more quality but more processing time.<br />

10 number of iterations                            |  30 number of iterations              |  60 number of iterations       
:-------------------------------------------------:|:-------------------------------------:|:-------------------------------------:
![](image/output/steps/couple_pixar_step_10.jpg)   | ![](image/output/image_style/couple_pixar_05.jpg) | ![](image/output/steps/couple_pixar_step_60.jpg)

Guidance Scale: Higher values means the generated image will be closer to text prompt.<br />

Guidance Scale=1                                                     |  Guidance Scale=5                                 |  Guidance Scale=9         
:-------------------------------------------------------------------:|:-------------------------------------------------:|:-------------------------------------:
![](image/output/guidance_scale/couple_pixar_guidance_scale_1.jpg)   | ![](image/output/image_style/couple_pixar_05.jpg) | ![](image/output/guidance_scale/couple_pixar_guidance_scale_9.jpg)

Controlnet Conditioning: Higher values means the generated image will be closer to input image in terms of canny image. 0.5 is the best trade-off.<br />

Condition Scale=0.3                                    |  Condition Scale=0.5                              |  Condition Scale=0.9         
:-----------------------------------------------------:|:-------------------------------------------------:|:-----------------------------------:
![](image/output/guidance_scale/couple_pixar_03.jpg)   | ![](image/output/image_style/couple_pixar_05.jpg) | ![](image/output/guidance_scale/couple_pixar_09.jpg)


## 3. Generate Image Transfer Style

Click on Generate Button. It will use a SDXL model use along a ControlNet model that will ensure to keep the mai features of the input images. 