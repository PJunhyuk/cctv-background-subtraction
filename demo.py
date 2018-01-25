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
parser.add_argument('-w', '--videoWidth', help='Width of Video')
args = vars(parser.parse_args())

if args['videoFileName'] is not None:
    video_file_name = args['videoFileName']
    print('videoFileName: ' + video_file_name)
else:
    print('You have to input videoFileName')
    sys.exit(1)

if args['videoWidth'] is not None:
    video_width = args['videoWidth']
    print('videoWidth: ' + video_width)
    video = video.resize(width = int(video_width))
else:
    print('Maintain videoWidth')

## Read video
video_file_route = 'testset/' + video_file_name
print('video_file_route: ' + video_file_route)
video = VideoFileClip(video_file_route)
print('Read Complete')

video_frame_number = int(video.duration * video.fps) ## duration: second / fps: frame per second
video_bg = []

for a in range(0, video.size[0]):
    video_bg_row = []
    for b in range(0, video.size[1]):
        pixel_list = []
        print(str(a) + ', ' + str(b))
        for i in range(0, video_frame_number):
            # Save i-th frame as image
            image = video.get_frame(i/video.fps)
            pixel = (image[b][a][0], image[b][a][1], image[b][a][2])
            pixel_list.append(pixel)
        pixel_list_counter = collections.Counter(pixel_list)
        pixel_list_mode = pixel_list_counter.most_common(1)[0][0]
        video_bg_row.append(pixel_list_mode)
    video_bg.append(video_bg_row)
    print(str(a+1) + "_Time(s): " + str(time.time() - time_start))

print(video_bg)
print(len(video_bg))
print(len(video_bg[0]))
print(len(video_bg[0][0]))
print(type(video_bg))

video_bg_image = Image.fromarray(np.uint8(video_bg))

video_bg_image.save('video_bg.jpg')
print("Time(s): " + str(time.time() - time_start))
