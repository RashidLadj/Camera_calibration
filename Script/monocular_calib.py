import cv2 as cv
import numpy as np
import yaml


def monocular_calib_from_video(filePathInput, display, configPathOutput, chessboard_config):

    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessboard_config[0]*chessboard_config[1],3), np.float32)
    objp[:,:2] = np.mgrid[0:chessboard_config[0],0:chessboard_config[1]].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    found = 0

    cap = cv.VideoCapture(filePathInput)                   #Input

    while(True):  # Here, 10 can be changed to whatever number you like to choose
        # Capture frame-by-frame
        for i in range (0,20):
            ret, img = cap.read()

        if ret != True:
            break

        (h, w) = img.shape[:2]

        # Our operations on the frame come here
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, chessboard_config, None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)   # Certainly, every loop objp is the same, in 3D.
            corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv.drawChessboardCorners(img, chessboard_config, corners2, ret)
            found += 1
            if display:
                width = 900.
                scale = width/w;
                cv.imshow("Image", cv.resize(img, None, (0, 0), scale, scale))


    print("Number of images used for calibration: ", found)

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # transform the matrix and distortion coefficients to writable lists
    data = {'resolution_image_wh': np.asarray([w, h]).tolist(),
            'intrinsic_camera_params': np.asarray(mtx).tolist(),
            'dist_coeff': np.asarray(dist).tolist()}

    # and save it to a file
    if configPathOutput == None:
        configPathOutput = "camera_params.yaml"
    elif not (configPathOutput.split(".")[-1] == "yaml"):
        configPathOutput += ".yaml"

    with open(configPathOutput, "w") as f:
        yaml.dump(data, f)



def monocular_calib_from_multiple_images(images_list, display, configPathOutput, chessboard_config):

    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros( (chessboard_config[0] * chessboard_config[1], 3), np.float32)
    objp[:, : 2] = np.mgrid[0:chessboard_config[0], 0:chessboard_config[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.

    found = 0

    resolution = None
    print("images number == ", len(images_list))

    for img_name in images_list: 
        print (img_name)
        img = cv.imread(img_name)
        
        if (img is None):
            print ("le chemin {} n'existe pas, ou bien il ne représente pas une image".format(img_name))
            break

        (h, w) = img.shape[:2]
        if resolution == None:
            resolution = (h, w)
        assert resolution == (h, w),"All images need have same resolution"

        # Our operations on the frame come here
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        # Find the chess board corners
        ret, corners = cv.findChessboardCorners(gray, chessboard_config, None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)   # Certainly, every loop objp is the same, in 3D.
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv.drawChessboardCorners(img, chessboard_config, corners2, ret)
            found += 1
            if display:
                width = 900.
                scale = width/w;
                cv.imshow("Image", cv.resize(img, None, (0, 0), scale, scale))
                cv.imwrite("images/calibrated/"+img_name, cv.resize(img, None, (0, 0), scale, scale))


    print("Number of images used for calibration: ", found)

    # When everything done
    cv.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # transform the matrix and distortion coefficients to writable lists
    data = {'resolution_image_wh': np.asarray([w, h]).tolist(),
            'intrinsic_camera_params': np.asarray(mtx).tolist(),
            'dist_coeff': np.asarray(dist).tolist()}

    # and save it to a file
    if configPathOutput == None:
        configPathOutput = "camera_params.yaml"
    elif not (configPathOutput.split(".")[-1] == "yaml"):
        configPathOutput += ".yaml"

    with open(configPathOutput, "w") as f:
        yaml.dump(data, f)



def monocular_calib_from_images_folder(folderPathInput, display, configPathOutput, chessboard_config):
    
    import os 
    """ load and sort files """
    images_list = [folderPathInput+"/"+file for file in os.listdir(folderPathInput) if (file.endswith('.png') or file.endswith('.PNG') or file.endswith('.jpg') or file.endswith('.JPG'))]
    images_list = sorted(images_list)

    monocular_calib_from_multiple_images(images_list, display, configPathOutput, chessboard_config)

    