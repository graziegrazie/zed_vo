import sys
import copy
import math

import cv2
import numpy as np

import pyzed.camera  as zcam
import pyzed.types   as tp
import pyzed.core    as core
import pyzed.defines as sl

from matplotlib import pyplot as plt

zed = ""
orb = ""
runtime_parameters = ""

def init_zed():
    global zed
    global runtime_parameters
    
    zed = zcam.PyZEDCamera()

    init_params                   = zcam.PyInitParameters()
    init_params.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_HD1080
    init_params.depth_mode        = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE
    init_params.coordinate_units  = sl.PyUNIT.PyUNIT_MILLIMETER

    err = zed.open(init_params)
    if err == tp.PyERROR_CODE.PySUCCESS:
        print("ZED Opened")
        pass
    else:
        print("init_zed failed!! ERROR_CODE:%d" % err)
        exit(1)

    runtime_parameters              = zcam.PyRuntimeParameters()
    runtime_parameters.sensing_mode = sl.PySENSING_MODE.PySENSING_MODE_STANDARD

# this function detects match point between t-1 and t
def detect_matching_from_images(prev_img, curr_img):
    global orb
    
    prev_kp, prev_des = orb.detectAndCompute(prev_img, None)
    curr_kp, curr_des = orb.detectAndCompute(curr_img, None)
    
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(prev_des, curr_des)
    matches = sorted(matches, key=lambda x:x.distance)
    
    match_img = cv2.drawMatches(prev_img, prev_kp, curr_img, curr_kp, matches[:10], None, flags=0)
    cv2.imshow("match", match_img)
    plt.pause(0.1)

    
def cap_and_show_depth_image():
    global zed
    global runtime_parameters
 
    i   = 0
    key = ''

    left_img = core.PyMat()
    right_img = core.PyMat()
    prev_img = core.PyMat()
    curr_img = core.PyMat()
    match_img = ""
    depth    = core.PyMat()

    while key != 113: # means 'q'
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            zed.retrieve_image(left_img, sl.PyVIEW.PyVIEW_LEFT_GRAY)
            zed.retrieve_measure(depth,  sl.PyMEASURE.PyMEASURE_DEPTH)

            curr_img = left_img.get_data()

            if i == 0:
                # skip this operation
                pass
            else:
                detect_matching_from_images(prev_img, curr_img)

            key = cv2.waitKey(10)
            
            i = i + 1
            prev_img = copy.deepcopy(curr_img)

    zed.close()

def main():
    global orb
    orb = cv2.ORB_create()
    init_zed()
    cap_and_show_depth_image()
        
if __name__ == '__main__':
    main()
