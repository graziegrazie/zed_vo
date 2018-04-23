import cv2
import math
import numpy as np
import sys
import pyzed.camera  as zcam
import pyzed.types   as tp
import pyzed.core    as core
import pyzed.defines as sl

zed = ""
runtime_parameters = ""

def init_zed():
    global zed
    global runtime_parameters
    
    zed = zcam.PyZEDCamera()

    init_params                  = zcam.PyInitParameters()
    init_params.depth_mode       = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE
    init_params.coordinate_units = sl.PyUNIT.PyUNIT_MILLIMETER

    err = zed.open(init_params)
    if err == tp.PyERROR_CODE.PySUCCESS:
        print("ZED Opened")
        pass
    else:
        print("init_zed failed!! ERROR_CODE:%d" % err)
        exit(1)

    runtime_parameters              = zcam.PyRuntimeParameters()
    runtime_parameters.sensing_mode = sl.PySENSING_MODE.PySENSING_MODE_STANDARD

def cap_and_show_depth_image():
    global zed
    global runtime_parameters
 
    i   = 0
    key = ''

    limage      = core.PyMat()
    rimage      = core.PyMat()
    depth       = core.PyMat()
    point_cloud = core.PyMat()

    while key != 113: # means 'q'
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            zed.retrieve_image(limage,        sl.PyVIEW.PyVIEW_LEFT)
            zed.retrieve_image(rimage,        sl.PyVIEW.PyVIEW_RIGHT)
            zed.retrieve_measure(depth,       sl.PyMEASURE.PyMEASURE_DEPTH)
            zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)

            cv2.imshow("left image", limage.get_data())
            cv2.imshow("right image", rimage.get_data())
            cv2.imshow("depth image", depth.get_data())

            key = cv2.waitKey(10)

            x = round(limage.get_width()  / 2.0)
            y = round(limage.get_height() / 2.0)
            err, point_cloud_value = point_cloud.get_value(x, y)

            distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                 point_cloud_value[1] * point_cloud_value[1] +
                                 point_cloud_value[2] * point_cloud_value[2])

            if np.isnan(distance) or np.isinf(distance):
                print("Can't estimate distance at this position, move the camera\n")
            else:
                distance = round(distance)
                print("Distance to Camera at ({0}, {1}): {2}mm\n".format(x, y, distance))
                i = i + 1
            sys.stdout.flush()

    zed.close()

def main():
    init_zed()
    cap_and_show_depth_image()
        
if __name__ == '__main__':
    main()
