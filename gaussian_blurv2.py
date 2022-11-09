#  cv 2 for test display
import cv2 
import numpy as np


def gkernel(l=3, sig=2):
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    xx, yy = np.meshgrid(ax, ax)

    kernel = np.exp(-0.5 * (np.square(xx) + np.square(yy)) / np.square(sig))

    return kernel / np.sum(kernel)

def convolve2d(image, kernel):
    # Flip the kernel
    kernel = np.flipud(np.fliplr(kernel))
    # convolution output
    # print(image.shape)
    output = np.zeros_like(image)

    # Add zero padding to the input image
    image_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))
    image_padded[1:-1, 1:-1] = image

    # Loop over every pixel of the image
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            # element-wise multiplication of the kernel and the image
            output[y, x]=(kernel * image_padded[y: y+3, x: x+3]).sum()

    return output

def gaussian_blurv2(img, k_size, sigma):
    # if len(img.shape) == 3:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g_kernel = gkernel(k_size, sigma)
    # blurred_img = cv2.filter2D(gray, -1,  g_kernel)
    blurred_img = convolve2d(gray, g_kernel)

    return blurred_img


def test():
    img = cv2.imread('images/shapes4.png') # Reading Image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converting Image to grayscale
    g_kernel = gkernel(3,2) # Create gaussian kernel with 3x3(odd) size and sigma equals to 2
    # print("Gaussian Filter: ",g_kernel) # show the kernel array
    # dst = cv2.filter2D(gray,-1,g_kernel) #convolve kernel with image
    dst = convolve2d(gray,g_kernel)
    # dst = convolution(gray,g_kernel)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # convert BGR(opencv format) to RGB format
    cv2.imshow('image',dst)
    cv2.waitKey(0)
    # dst = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) # convert BGR(opencv format) to RGB format

    # plt.figure(figsize=(18, 18))
    # plt.subplot(131),plt.imshow(img),plt.title('Original Image') # visualize and give title
    # plt.subplot(132),plt.imshow(gray),plt.title('GrayScaled Image')
    # plt.subplot(133),plt.imshow(dst),plt.title('Smoothed Image with  Gaussian Filter (sigma=2,3x3 Kernel)')
    # plt.show()

# test()
