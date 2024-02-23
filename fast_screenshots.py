import numpy as np
import mss

sct = mss.mss()

# app_coords (8, 44, 1288, 764)
box = {"top":    app_coords[1],
       "left":   app_coords[0],
       "width":  app_coords[2]-app_coords[0],
       "height": app_coords[3]-app_coords[1]}

sct_im = sct.grab(box)
im = np.asarray(sct_im)[:,:,:3] # < 2.5 ms

#plt.imshow(im)
