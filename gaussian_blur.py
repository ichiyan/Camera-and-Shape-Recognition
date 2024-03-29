import numpy as np
import cv2
import matplotlib.pyplot as plt
import math
import argparse


def dnorm(x, mu, sd):
    # density using the univariate normal distribution formula
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)

def gaussian_kernel(size, sigma=1, verbose=False):

    kernel_1D = np.linspace(-(size // 2), size // 2, size )
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)
    kernel_2D *= 1.0 / kernel_2D.max()

    if verbose:
        plt.imshow(kernel_2D, interpolation='none', cmap='gray')
        plt.title(f"Kernel ( {size}x{size} )")
        plt.show()

    return kernel_2D


def convolution(image, kernel, average=False, verbose=False):
    
    if len(image.shape) == 3:
        if verbose: print(f"Found 3 channels : {image.shape}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if verbose: print(f"Converted to gray channel. Size : {image.shape}")
    
    else:
        if verbose: print(f"Image Shape : {image.shape}")

    if verbose:
        print(f"Kernel Shape : {kernel.shape}")
        plt.imshow(image, cmap="gray")
        plt.title("Image")
        plt.show()

    image_row, image_col = image.shape
    kernel_row, kernel_col = kernel.shape

    output = np.zeros(image.shape)

    pad_height = int((kernel_row - 1) / 2 )
    pad_width = int((kernel_col - 1) / 2)

    padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))
    padded_image[ pad_height: padded_image.shape[0] - pad_height, pad_width: padded_image.shape[1] - pad_width ] = image  

    if verbose:
        plt.imshow(padded_image, cmap="gray")
        plt.title("Padded Image")
        plt.show()
    
    
    for row in range(image_row):
        for col in range(image_col):
            output[row, col] = np.sum(kernel * padded_image[row: row + kernel_row, col: col + kernel_col])

    if average:
        output[row, col] /= kernel.shape[0] * kernel.shape[1]

    if verbose:
        print(f"Output image size : {output.shape}")
        plt.imshow(output, cmap="gray")
        plt.title(f"Output Image Using {kernel_row}x{kernel_col} Kernel")
        plt.show()

        print(type(output))

    return output

def gaussian_blur(image, kernel_size, verbose=False):
    kernel = gaussian_kernel(kernel_size, sigma=math.sqrt(kernel_size), verbose=verbose)
    return convolution(image, kernel, average=True, verbose=verbose)


if __name__  == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="Path to the image.")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])

    test = gaussian_blur(image, 15, verbose=True)
    # print(type(test))
    # print(test)