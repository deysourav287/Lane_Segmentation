# Lane_Segmentation


![lane](https://user-images.githubusercontent.com/106477719/208263411-2e1672b8-fc3e-4f32-973e-6efb6f61f3b0.png)

# Contents
data_preparation.ipynb: Use this notebook for generating train, validation and test data (Dataset TuSimple);

train.ipynb: Notebook with the training method, I used the following library Segmentations Models;

make_video.ipynb: Notebook for making a video with all images on the test set.

Model: Resnet18 Backbone with Unet Architecture for Decoder Input: 512 width x 256 heigth x 3 channels
