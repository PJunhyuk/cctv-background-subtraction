## check time required
import time
time_start = time.time()

## for ArgParse
import argparse as ap

## moviepy
from moviepy.editor import *

## default
import sys

## counter
import collections

import numpy as np

from PIL import Image

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

## Read video
video_file_route = 'testset/' + video_file_name
print('video_file_route: ' + video_file_route)
video = VideoFileClip(video_file_route)
print('Read Complete')

video = video.resize(width = 32)

video_frame_number = int(video.duration * video.fps) ## duration: second / fps: frame per second
video_bg_row = []
video_bg = []

for a in range(0, video.size[1]):
    for b in range(0, video.size[0]):
        pixel_list = []
        print(a)
        print(b)
        for i in range(0, video_frame_number):
            # Save i-th frame as image
            image = video.get_frame(i/video.fps)
            pixel = (image[a][b][0], image[a][b][1], image[a][b][2])
            pixel_list.append(pixel)
        pixel_list_counter = collections.Counter(pixel_list)
        pixel_list_mode = pixel_list_counter.most_common(1)[0][0]
        video_bg_row.append(pixel_list_mode)
    video_bg.append(video_bg_row)
    print(str(a+1) + "_Time(s): " + str(time.time() - time_start))

print(video_bg)
print(size(video_bg))
video_bg.save('video_bg.jpg')
# video_bg_image = Image.fromarray(video_bg)
# video_bg_image.save('video_bg.jpg')
print("Time(s): " + str(time.time() - time_start))
