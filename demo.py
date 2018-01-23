## check time required
import time
time_start = time.time()

## for ArgParse
import argparse as ap

## moviepy
from moviepy.editor import *

## default
import sys

## ArgParse
parser = ap.ArgumentParser()
parser.add_argument('-f', '--videoFileName', help='Name of Video File')
args = vars(parser.parse_args())

if args['videoFileName'] is not None:
    video_file_name = args['videoFileName']
    print('videoFileName: ' + video_file_name)
else:
    print('You have to input videoFileName')
    sys.exit(1)

video_file_route = 'testset/' + video_file_name
print('video_file_route: ' + video_file_route)
video = VideoFileClip(video_file_route)
print('Read Complete')

frame_index = 0

while(1):
    ret, frame = video.read()
    if ret == False:
        break

    print('frame_index: ' + str(frame_index))
    frame_index = frame_index + 1

    break
