import argparse
from monocular_calib import *

parser = argparse.ArgumentParser()

parser.add_argument("camera_type"              , help="type of camera must be \"monocular\", \"fisheye\" or \"stereo\"", choices = ["monocular", "fisheye", "stereo"])

data = parser.add_mutually_exclusive_group( required = True)
data.add_argument('-v'     , '--video'         , help = 'video_path_file')
data.add_argument('-if'    , '--images_folder' , help = 'Path of images folder')
data.add_argument('-i'     , '--images'        , help = 'Path of all images 1 .. N'     , nargs = '+')

parser.add_argument("-o"   , "--output"        , help="output YAML file path")
parser.add_argument("-d"   , "--display"       , help="output YAML file path", action="store_true")



""" configuration of the number of corners to be detected per row and per column for the calibration of the camera using a chessboard """
chessboard_config = tuple((6, 9)) 


args = parser.parse_args()
if args.camera_type == "monocular":
    if args.video:
        print("- Start calibration of \"{}\" camera with video input \"{}\"".format(args.camera_type, args.video, args.output))
        monocular_calib_from_video(args.video, args.display, args.output, chessboard_config)

    if args.images_folder:
        print("- Start calibration of \"{}\" camera from images folder \"{}\"".format(args.camera_type, args.images_folder))
        monocular_calib_from_images_folder(args.images_folder, args.display, args.output, chessboard_config)

    if args.images:
        print("Start calibration of \"{}\" camera with miltiple image {}".format(args.camera_type, args.images))
        monocular_calib_from_multiple_images(args.images, args.display, args.output, chessboard_config)


else:
    print ("Not implemented yet")