import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

model=models.resnet18(pretrained=True)
model.eval()

#preprocessing 
# This allows you to make multiple image transformation into a pipeline.

preprocess=transforms.Compose([
    #Most pre-trained models Resnet, MobileNet expect images to have a fixed size as an input,
    #It makes all the image of the same size.
    # The image is then converted into
    transforms.Resize(224,224,3),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
    # all the images on which the model was trained on was normalized_pixel
    # normalized_pixel=(pixel-mean)/std
])

img=Image.open()
img_tensor=preprocess(img).unsqueeze(0)