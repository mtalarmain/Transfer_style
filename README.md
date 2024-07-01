# Transfer_style

## 1. Load Input Image

You can load the input image on the Input section. Then it is possible to choose the parameter of the model depending on your needs. 

## 2. Parameters

Generation steps: Control the trade-off between quality and speed. Higher values means more quality but more processing time.
Guidance Scale: Higher values means the generated image will be closer to text prompt.
Controlnet Conditioning: Higher values means the generated image will be closer to input image in terms of canny image. 0.5 is the best trade-off.

## 3. Generate Image Transfer Style

Click on Generate Button. It will use a SDXL model use along a ControlNet model that will ensure to keep the mai features of the input images. 