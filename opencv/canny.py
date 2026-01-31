import numpy as np
from scipy import signal
import cv2
import matplotlib.pyplot as plt
import matplotlib
from ipywidgets import interact, fixed, widgets
from mpl_toolkits.mplot3d import Axes3D
import os

matplotlib.rcParams['figure.figsize'] = (15.0, 15.0)

# Implement a function that blurres an input image using a Gaussian filter and then normalizes it.
def gaussian_smoothing(image, sigma, w_kernel):
    """ Blur and normalize input image.   
    
        Args:
            image: Input image to be binarized
            sigma: Standard deviation of the Gaussian distribution
            w_kernel: Kernel aperture size
                    
        Returns: 
            smoothed_norm: Blurred image
    """   
    # Write your code here!
    
    # Define 1D kernel
    s=sigma
    w=w_kernel
    # Create 1D Gaussian filter
    kernel_1D = np.array([(1/(np.sqrt(2*np.pi)*s))*np.exp(-(1/2)*(z*z/(s*s))) for z in range(-w,w+1)])
    
    # Apply distributive property of convolution
    vertical_kernel = kernel_1D.reshape(2*w+1,1)
    horizontal_kernel = kernel_1D.reshape(1,2*w+1)   
    gaussian_kernel_2D = signal.convolve2d(vertical_kernel, horizontal_kernel)   
    
    # Blur image
    smoothed_img = cv2.filter2D(image, cv2.CV_8U, gaussian_kernel_2D)
    
    # Normalize to [0 254] values
    smoothed_norm = np.array(image.shape)
    # cv.normalize(src, dst, alpha (=norm value to normalize), beta (=upper range boundary in case of the range normalization), norm_type) 
    smoothed_norm = cv2.normalize(smoothed_img, None, 0, 255, cv2.NORM_MINMAX) # Leave the second argument as None
    
    return smoothed_norm


# CANNY
lower_threshold = 60
upper_threshold = 100
sigma = 2
w_gaussian = 3
# Resize
r,c = 200,200
# Locations
images_path = './images/'
directory = './train/'



for card in range(2):
    for num in range (10):
        carta = cv2.imread(images_path + 'image' + str(card) + '_' + str(num) + '.jpg')
        carta = cv2.resize(carta, (r,c))
        # Smooth image
        blurred_img = gaussian_smoothing(carta, sigma, w_gaussian)      
        # Apply Canny to blurred image
        canny_blurred = cv2.Canny(blurred_img, lower_threshold, upper_threshold)
        
        # Save in train folder
        cv2.imwrite(directory + 'image' + str(card) + '_' + str(num) + '.png', canny_blurred)