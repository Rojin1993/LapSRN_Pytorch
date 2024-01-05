#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 10:07:14 2017

@author: ldy
"""

from __future__ import print_function
from os.path import exists, join, basename
from os import makedirs, remove
import argparse
import torch
from torch.autograd import Variable
from PIL import Image
from torchvision.transforms import ToTensor
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
from pylab import rcParams
rcParams['figure.figsize'] = 40, 24
rcParams.update({'font.size': 22})
# Training settings
parser = argparse.ArgumentParser(description='PyTorch LapSRN')
parser.add_argument('--test_folder', type=str, default='./Noisy_LR2', help='input image to use')
parser.add_argument('--model', type=str, default='model/model_epoch_50.pth', help='model file to use')
parser.add_argument('--save_folfer', type=str, default='./results', help='input image to use')
# parser.add_argument('--output_filename', type=str, help='where to save the output image')
parser.add_argument('--cuda', action='store_true', help='use cuda')

opt = parser.parse_args()

print(opt)

def centeredCrop(img):
    width, height = img.size   # Get dimensions
    new_width = width - width % 8
    new_height = height - height % 8 
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2
    return img.crop((left, top, right, bottom))

def process(out, cb, cr):
    out_img_y = out.data[0].numpy()
    out_img_y *= 255.0
    out_img_y = out_img_y.clip(0, 255)
    out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')
    
    out_img_cb = cb.resize(out_img_y.size, Image.BICUBIC)
    out_img_cr = cr.resize(out_img_y.size, Image.BICUBIC)
    out_img = Image.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')
    return out_img

def save_image(HR_2, HR_4, HR_8, GT, name):
    LR = GT.resize((int(y.size[0]/4), int(y.size[1]/4)), Image.BICUBIC)
   
    if not exists(opt.save_folfer):
        makedirs(opt.save_folfer)
    
    HR_4.save(join(opt.save_folfer, f'{name}.jpeg'))
    print(f'HR_4 image: {name} saved!')

    
    

    
images_list = glob(opt.test_folder+'/*.jpeg')
print (len(images_list))
torch.nn.Module.dump_patches = True
model = torch.load(opt.model, map_location=torch.device('cpu'))
if opt.cuda:
    model = model.cuda()
for image_path in images_list:
    img_name = image_path.split('/')[-1].split('.')[0]
    img = Image.open(image_path).convert('YCbCr')
    # img = centeredCrop(img)
    y, cb, cr = img.split()
    LR = y.resize((int(y.size[0]/1), int(y.size[1]/1)), Image.BICUBIC)
    print (LR.size)
    LR = Variable(ToTensor()(LR)).view(1, -1, LR.size[1], LR.size[0])
    if opt.cuda:
        LR = LR.cuda()
    HR_2, HR_4, HR_8 = model(LR)
    print(HR_4.shape)
    HR_2 = HR_2.cpu()
    HR_4 = HR_4.cpu()
    HR_8 = HR_8.cpu()
    HR_2 = process(HR_2, cb, cr)
    HR_4 = process(HR_4, cb, cr)
    HR_8 = process(HR_8, cb, cr)
    img = img.convert("RGB")
    save_image(HR_2, HR_4, HR_8, img, img_name)
    

