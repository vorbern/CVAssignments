import math
import sys

import cv2
import numpy as np
import sklearn


class ImageInfo:
    def __init__(self, name, img, position):
        self.name = name
        self.img = img
        self.position = position


def imageBoundingBox(img, M):
    """
       This is a useful helper function that you might choose to implement
       that takes an image, and a transform, and computes the bounding box
       of the transformed image.

       INPUT:
         img: image to get the bounding box of
         M: the transformation to apply to the img
       OUTPUT:
         minX: int for the minimum X value of a corner
         minY: int for the minimum Y value of a corner
         maxX: int for the maximum X value of a corner
         maxY: int for the maximum Y value of a corner
    """
    #TODO 8
    #TODO-BLOCK-BEGIN
    # C B
    # O A
    height,width = img.shape[:2]
    O = np.array([0,0,1])
    A = np.array([0,height-1,1])
    B = np.array([width-1,height-1,1])
    C = np.array([width-1,0,1])

    O = np.dot(M,O)
    A = np.dot(M,A)
    B = np.dot(M,B)
    C = np.dot(M,C)

    def up(x):
        if x<0.0:
            x = math.floor(x)
        else:
            x = math.ceil(x)
        return x

    minX = up(min(O[0]/O[2], A[0]/A[2], B[0]/B[2], C[0]/C[2]))
    minY = up(min(O[1]/O[2], A[1]/A[2], B[1]/B[2], C[1]/C[2]))
    maxX = up(max(O[0]/O[2], A[0]/A[2], B[0]/B[2], C[0]/C[2]))
    maxY = up(max(O[1]/O[2], A[1]/A[2], B[1]/B[2], C[1]/C[2]))
    raise Exception("TODO in blend.py not implemented")
    #TODO-BLOCK-END
    return int(minX), int(minY), int(maxX), int(maxY)


def accumulateBlend(img, acc, M, blendWidth):
    """
       INPUT:
         img: image to add to the accumulator
         acc: portion of the accumulated image where img should be added
         M: the transformation mapping the input image to the accumulator
         blendWidth: width of blending function. horizontal hat function
       OUTPUT:
         modify acc with weighted copy of img added where the first
         three channels of acc record the weighted sum of the pixel colors
         and the fourth channel of acc records a sum of the weights
    """
    # BEGIN TODO 10
    # Fill in this routine
    #TODO-BLOCK-BEGIN
    h = img.shape[0]
    w = img.shape[1]

    h_acc = acc.shape[0]
    w_acc = acc.shape[1]

    ## get the bounding box of img in acc
    minX, minY, maxX, maxY = imageBoundingBox(img, M)

    for i in range(minX, maxX, 1):
        for j in range(minY, maxY, 1):
            # don't want to include black pixels when inverse warping
            ## whether current pixel black or white
            p = np.array([i, j, 1.])
            p = np.dot(inv(M), p)
            newx = min(p[0] / p[2], w - 1)
            newy = min(p[1] / p[2], h - 1)

            if newx < 0 or newx >= w or newy < 0 or newy >= h:
                continue
            if img[newy, newx, 0] == 0 and img[newy, newx, 1] == 0 and img[newy, newx, 2] == 0:
                continue
            if newx >= 0 and newx < w - 1 and newy >= 0 and newy < h - 1:
                weight = 1.0
                if newx >= minX and newx < minX + blendWidth:
                    weight = 1. * (newx - minX) / blendWidth
                if newx <= maxX and newx > maxX - blendWidth:
                    weight = 1. * (maxX - newx) / blendWidth
                acc[j, i, 3] += weight

                for k in range(3):
                    acc[j, i, k] += img[int(newy), int(newx), k] * weight

    #*******Try1
    # acc[:,:,0:2] = cv2.remap(img,)
    raise Exception("TODO in blend.py not implemented")
    #TODO-BLOCK-END
    # END TODO


def normalizeBlend(acc):
    """
       INPUT:
         acc: input image whose alpha channel (4th channel) contains
         normalizing weight values
       OUTPUT:
         img: image with r,g,b values of acc normalized
    """
    # BEGIN TODO 11
    # fill in this routine..
    #TODO-BLOCK-BEGIN
    h,w = acc.shape[0:1]
    img = np.zeros((h,w,3))
#****Try1
    # temp1 = acc[:,:,3]
    # temp1.apply(lambda x:0 if x<0 else 1)
    # temp = acc[:,:,0:2]
    # temp = temp*temp1
    # img = temp / acc[:,:,3]
    # img = np.uint8(img)
    for i in range(0, w_acc, 1):
        for j in range(0, h_acc, 1):
            if acc[j,i,3]>0:
                img[j,i,0] = int (acc[j,i,0] / acc[j,i,3])
                img[j,i,1] = int (acc[j,i,1] / acc[j,i,3])
                img[j,i,2] = int (acc[j,i,2] / acc[j,i,3])
            else:
                img[j,i,0] = 0
                img[j,i,1] = 0
                img[j,i,2] = 0
    img = np.uint8(img)
    raise Exception("TODO in blend.py not implemented")
    #TODO-BLOCK-END
    # END TODO
    return img


def getAccSize(ipv):
    """
       This function takes a list of ImageInfo objects consisting of images and
       corresponding transforms and Returns useful information about the accumulated
       image.

       INPUT:
         ipv: list of ImageInfo objects consisting of image (ImageInfo.img) and transform(image (ImageInfo.position))
       OUTPUT:
         accWidth: Width of accumulator image(minimum width such that all tranformed images lie within acc)
         accHeight: Height of accumulator image(minimum height such that all tranformed images lie within acc)

         channels: Number of channels in the accumulator image
         width: Width of each image(assumption: all input images have same width)
         translation: transformation matrix so that top-left corner of accumulator image is origin
    """

    # Compute bounding box for the mosaic
    minX = sys.maxint
    minY = sys.maxint
    maxX = 0
    maxY = 0
    channels = -1
    width = -1  # Assumes all images are the same width
    M = np.identity(3)
    for i in ipv:
        M = i.position
        img = i.img
        h, w, c = img.shape
        if channels == -1:
            channels = c
            width = w

        # BEGIN TODO 9
        # add some code here to update minX, ..., maxY
        #TODO-BLOCK-BEGIN
        minx,miny,maxx,maxy = imageBoundingBox(img,M)
        minX = min(minX,minx)
        minY = min(minY,miny)
        maxX = max(maxX,maxx)
        maxY = max(maxY,maxy)
        raise Exception("TODO in blend.py not implemented")
        #TODO-BLOCK-END
        # END TODO

    # Create an accumulator image
    accWidth = int(math.ceil(maxX) - math.floor(minX))
    accHeight = int(math.ceil(maxY) - math.floor(minY))
    print('accWidth, accHeight:', (accWidth, accHeight))
    translation = np.array([[1, 0, -minX], [0, 1, -minY], [0, 0, 1]])

    return accWidth, accHeight, channels, width, translation


def pasteImages(ipv, translation, blendWidth, accWidth, accHeight, channels):
    acc = np.zeros((accHeight, accWidth, channels + 1))
    # Add in all the images
    M = np.identity(3)
    for count, i in enumerate(ipv):
        M = i.position
        img = i.img

        M_trans = translation.dot(M)
        accumulateBlend(img, acc, M_trans, blendWidth)

    return acc


def getDriftParams(ipv, translation, width):
    # Add in all the images
    M = np.identity(3)
    for count, i in enumerate(ipv):
        if count != 0 and count != (len(ipv) - 1):
            continue

        M = i.position

        M_trans = translation.dot(M)

        p = np.array([0.5 * width, 0, 1])
        p = M_trans.dot(p)

        # First image
        if count == 0:
            x_init, y_init = p[:2] / p[2]
        # Last image
        if count == (len(ipv) - 1):
            x_final, y_final = p[:2] / p[2]

    return x_init, y_init, x_final, y_final


def computeDrift(x_init, y_init, x_final, y_final, width):
    A = np.identity(3)
    drift = (float)(y_final - y_init)
    # We implicitly multiply by -1 if the order of the images is swapped...
    length = (float)(x_final - x_init)
    A[0, 2] = -0.5 * width
    # Negative because positive y points downwards
    A[1, 0] = -drift / length

    return A


def blendImages(ipv, blendWidth, is360=False, A_out=None):
    """
       INPUT:
         ipv: list of input images and their relative positions in the mosaic
         blendWidth: width of the blending function
       OUTPUT:
         croppedImage: final mosaic created by blending all images and
         correcting for any vertical drift
    """
    accWidth, accHeight, channels, width, translation = getAccSize(ipv)
    acc = pasteImages(
        ipv, translation, blendWidth, accWidth, accHeight, channels
    )
    compImage = normalizeBlend(acc)

    # Determine the final image width
    outputWidth = (accWidth - width) if is360 else accWidth
    x_init, y_init, x_final, y_final = getDriftParams(ipv, translation, width)
    # Compute the affine transform
    A = np.identity(3)
    # BEGIN TODO 12
    # fill in appropriate entries in A to trim the left edge and
    # to take out the vertical drift if this is a 360 panorama
    # (i.e. is360 is true)
    # Shift it left by the correct amount
    # Then handle the vertical drift
    # Note: warpPerspective does forward mapping which means A is an affine
    # transform that maps accumulator coordinates to final panorama coordinates
    #TODO-BLOCK-BEGIN
    if is360 :
        A = computeDrift(x_init, y_init, x_final, y_final, width)
    raise Exception("TODO in blend.py not implemented")
    #TODO-BLOCK-END
    # END TODO

    if A_out is not None:
        A_out[:] = A

    # Warp and crop the composite
    croppedImage = cv2.warpPerspective(
        compImage, A, (outputWidth, accHeight), flags=cv2.INTER_LINEAR
    )

    return croppedImage

