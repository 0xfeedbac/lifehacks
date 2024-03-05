%matplotlib widget 
#%matplotlib inline 
import torch
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def project(im, an):

    h, w = im.shape
    h = torch.tensor(h) 
    w = torch.tensor(w)

    # buffer length for 1D projection
    p_len = torch.abs( torch.cos(an) * w ) + torch.abs( torch.sin(an) * h )
    p_len = torch.abs(p_len)
    
    p_len = p_len.int()
    pp = torch.zeros(p_len) # projected points

    # lookup table to project points to the destination position
    xdim = torch.arange(w).unsqueeze(0).repeat(h, 1).float()
    ydim = torch.arange(h).unsqueeze(1).repeat(1, w).float()

    xdim *= torch.cos(an)
    ydim *= torch.sin(an)
    
    pdim = xdim + ydim
    pdim = pdim.int()
    pdim = pdim - pdim.min() # normalize to positive indicies only
    
    pp = torch.zeros(p_len)
    
    for i, dim in enumerate(pdim):
        pp.index_add_(0, dim, im[i])

    return pp

# visialization
def animate(t):   
    
    im0 = im
    im1 = im.clone()
    im2 = im.clone()*0

    an = (t%rot_steps) / rot_steps
    an = an * 2*3.14159265359
    an = torch.tensor(an)

    pp = project(im, an)

    height, width = im.shape

    sin_an = torch.sin(an)
    cos_an = torch.cos(an)
    
    for i, p in enumerate(pp):
    
        i = i - len(pp)/2
        
        xpos = i * cos_an
        ypos = i * sin_an
        
        xpos = xpos + (width )/2
        ypos = ypos + (height)/2
        
        xpos = int(xpos)
        ypos = int(ypos)
        
        if 0 <= xpos < width and 0 <= ypos < height:   
            im1[ypos, xpos] += p
            im2[ypos, xpos] += p

    img0.set_array(im0)
    img1.set_array(im1)
    img2.set_array(im2)

    ax1.set_title("t = {}".format(t))
    
    return img0, img1, img2

height = torch.tensor(24)
width  = torch.tensor(16)

rot_steps = 60

num_pixels = 5 # random pixels to randomly color


im = torch.zeros(height, width)

# randomly color a few pixels
indices = torch.randperm(width*height)[:num_pixels]
im.view(-1)[indices] = torch.rand(num_pixels)

# manually color a few pixels
im[1, 1] = 2
im[2, 2] = 1.8

im2 = im1 = im0 = im

fig, (ax0, ax1, ax2) = plt.subplots(ncols=3)

img0 = ax0.imshow(im, animated=True); ax0.set_axis_off()
img1 = ax1.imshow(im, animated=True); ax1.set_axis_off()
img2 = ax2.imshow(im, animated=True); ax2.set_axis_off()

n=3
ax1.set_title("n = {}".format(n))

ani = animation.FuncAnimation(
    fig,
    animate,
    interval=50,
    blit=True,
    cache_frame_data=False
)

plt.show()

#animate(19)
