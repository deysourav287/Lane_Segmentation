# -*- coding: utf-8 -*-
"""make_video.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/darkrubiks/Lane_Segmentation/blob/main/make_video.ipynb

# Make Video
"""

import os
from tqdm import tqdm
import cv2 
import numpy as np 
import segmentation_models as sm
import tensorflow as tf
import matplotlib.pyplot as plt

plt.ioff()

model = tf.keras.models.load_model('model_resnet18_512x256.h5')
BACKBONE = 'resnet18'
preprocess_input = sm.get_preprocessing(BACKBONE)

ixs = [17,36,55,74,90,111,117,124]
outputs = [model.layers[i].output for i in ixs]
model_intermed = tf.keras.models.Model(inputs=model.inputs, outputs=outputs)

out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'XVID'), 30, (1280,720))

for clips in sorted(os.listdir('./test_set/clips/')):
    for folders in sorted(os.listdir('./test_set/clips/'+clips)):
        for files in range(1,21):
            
            frame_original = cv2.imread('./test_set/clips/'+clips+'/'+folders+'/'+str(files)+'.jpg')
            frame = cv2.cvtColor(frame_original, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame,(512,256))
            
            frame_p = preprocess_input(frame)
            frame_p = np.expand_dims(frame_p, axis=0)
            
            pr_mask = model.predict(frame_p).round() 
            
            mask = cv2.cvtColor(pr_mask[..., 0].squeeze(),cv2.COLOR_GRAY2RGB)
            mask = np.array(mask*255,'uint8')
            
            r = mask[:,:,0]
            g = mask[:,:,1]
            b = mask[:,:,2]
            
            r[r==255] = 0
            g[g==255] = 255
            b[b==255] = 25
            
            mask = np.stack([r,g,b],axis=-1)
            mask = cv2.GaussianBlur(mask,(5,5),0)
            
            kernel = np.ones((4,4),np.uint8)
            mask = cv2.erode(mask,kernel,iterations = 1)
            
            mask[0:105,...] = 0
            
            mask = cv2.resize(mask,(1280,720))
            te = cv2.addWeighted(frame_original,1,mask,5,0)
            
            feature_maps = model_intermed.predict(frame_p)
            fig, axs = plt.subplots(1, len(ixs), figsize=(35,12))
            for i,fmap in enumerate(feature_maps):
                axs[i].set_xticks([])
                axs[i].set_yticks([])
                axs[i].imshow(fmap[0, :, :, 1], cmap='gray')
            plt.tight_layout()
            fig.savefig('teste.png', dpi=100, transparent=True)
            plt.close()
            
            s_img = cv2.imread("teste.png",-1)
            s_img = cv2.resize(s_img,(1280,720))
            s_img = s_img[300:410,0:1280]
            
            x_offset=0
            y_offset=600

            y1, y2 = y_offset, y_offset + s_img.shape[0]
            x1, x2 = x_offset, x_offset + s_img.shape[1]

            alpha_s = s_img[:, :, 3] / 255.0
            alpha_l = 1.0 - alpha_s

            for c in range(0, 3):
                te[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] + alpha_l * te[y1:y2, x1:x2, c])
            
            out.write(te)  
            
out.release()