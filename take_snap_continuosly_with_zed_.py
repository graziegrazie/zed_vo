import cv2
import os
import datetime
import pyzed.camera  as zcam
import pyzed.types   as tp
import pyzed.core    as core
import pyzed.defines as sl

camera_setting_     = sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_BRIGHTNESS
str_camera_setting  = "BRIGHTNESS"
step_camera_setting = 1

def main():
    init = zcam.PyInitParameters()
    cam  = zcam.PyZEDCamera()
    if cam.is_opened():
        pass
    else:
        print("Opening ZED Camera...")

    init.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_HD1080
    status = cam.open(init)
    cam.set_camera_settings(sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_AUTO_WHITEBALANCE, 1, False)
    if status == tp.PyERROR_CODE.PySUCCESS:
        pass
    else:
        print(repr(status))
        exit()

    runtime = zcam.PyRuntimeParameters()
    mat = core.PyMat()

    # make save directory of images
    cwd      = os.getcwd()
    dir_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    dir_path = cwd + "/" + dir_name

    if os.path.exists(dir_path):
        pass
    else:
        os.makedirs(dir_path)

    key = ''
    count = 0
    while key != 113:
        err = cam.grab(runtime)
        if err == tp.PyERROR_CODE.PySUCCESS:
            cam.retrieve_image(mat, sl.PyVIEW.PyVIEW_LEFT)
            
            img = mat.get_data()
            cv2.imshow("ZED", img)

            file_name = ("image_{0:08d}.jpg".format(count))
            cv2.imwrite(dir_path + "/" + file_name, img)
            count = count + 1
                        
            key = cv2.waitKey(10)
        else:
            key = cv2.waitKey(10)
    cv2.destroyAllWindows()

    cam.close()
    print("\nFINISH")

if __name__ == '__main__':
    main()
