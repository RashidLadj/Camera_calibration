import argparse


parser = argparse.ArgumentParser()

parser.add_argument("camera_type"              , help="type of camera must be \"monocular\", \"fisheye\" or \"stereo\"", choices = ["monocular", "fisheye", "stereo"])

data = parser.add_mutually_exclusive_group( required = True)
data.add_argument('-v'     , '--video'         , help = 'video_path_file')
data.add_argument('-if'    , '--images_folder' , help = 'Path of images folder')
data.add_argument('-i'     , '--images'        , help = 'Path of all images 1 .. N'     , nargs = '+')

parser.add_argument("-o"   , "--output"        , help="output YAML file path")
parser.add_argument("-d"   , "--display"       , help="output YAML file path", action="store_true")
