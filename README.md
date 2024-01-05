# LapSRN_Pytorch
To test this method on low-resolution images, utilize the 'LapSRNtest.ipynb' file. Pay attention to the following warnings to obtain accurate results. 
Due to the high RAM requirements of this method, I recommend using Kaggle. Be aware that for this method, you don't need to create low-resolution images initially. By running 'test.py', it fetches all the images from the location specified by '--test_folder' and saves the results in the location specified by '--save_folder' (you can adjust these parameters in 'test.py'). The outputs of 'test.py' consist of five images in one picture: high-resolution image, low-resolution image (the width and height of images are reduced by 1/8 using the bicubic method), and super-resolved images of 2 by 2, 4 by 4, and 8 by 8. This file might throw one error due to line 57; it should be 'LR = GT.resize((y.size[0]//8, y.size[1]//8), Image.BICUBIC)'. As I only wanted to obtain the 4 by 4 super-resolved images as output, I ran the 'changed_test.py' file, which is located in my files. After cloning the GitHub repository to your Google Drive, you can place this file next to 'test.py'. To change the value of low resolution, you can adjust the 80th line in 'changed_test.py'.
As I tested this method on noisy images, I added the code for adding noise in the 'NoisyImages.ipynb' notebook. The first cell contains Gaussian noise, and the second cell adds 'salt and pepper' noise to the images.
