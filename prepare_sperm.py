import cv2 
import os 
import numpy as np 

img_path = os.path.join(os.getcwd(), 'data/sperm_dataset')
print(img_path)

for root, dir, files in os.walk(img_path):
    for f in files:
        if '.yaml' not in f: 
            current_img = os.path.join(root, f)
            im = cv2.imread(current_img)
            im_height, im_width, c = im.shape
            
            # Create black background 
            background = np.zeros(shape=(420, 380, 3), dtype=np.uint8) 
            bg_height, bg_width, bg_c = background.shape

            # Add sperm onto black backgorund
            x_offset = (bg_width - im_width) // 2
            y_offset = (bg_height - im_height) // 2
            
            background[y_offset:y_offset+im_height, x_offset:x_offset+im_width, 0] = im[:,:,0]
            background[y_offset:y_offset+im_height, x_offset:x_offset+im_width, 1] = im[:,:,1]
            background[y_offset:y_offset+im_height, x_offset:x_offset+im_width, 2] = im[:,:,2]

            