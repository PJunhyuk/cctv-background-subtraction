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
parser.add_argument('-b', '--videoBackground', help='Background Image of Video')
args = vars(parser.parse_args())

if args['videoFileName'] is not None:
    video_file_name = args['videoFileName']
    print('videoFileName: ' + video_file_name)
else:
    print('You have to input videoFileName')
    sys.exit(1)
video_output_name = video_file_name.split('.')[0]

## Read video
video_file_route = 'testset/' + video_file_name
print('video_file_route: ' + video_file_route)
video = VideoFileClip(video_file_route)
print('Read Complete')

if args['videoWidth'] is not None:
    video_width = args['videoWidth']
    print('videoWidth: ' + video_width)
    video = video.resize(width = int(video_width))
else:
    print('Maintain videoWidth')

video_frame_number = int(video.duration * video.fps) ## duration: second / fps: frame per second

if args['videoBackground'] is not None:
    video_bg_image = Image.open(args['videoBackground'])
    video_bg = np.asarray(video_bg_image)
else:
    print('No background image input!')
    print('Subtracting background from input video...')
    video_bg = []
    skip_const = 1
    for a in range(0, video.size[1]):
        video_bg_row = []
        for b in range(0, video.size[0]):
            pixel_list = []
            print(str(b) + ', ' + str(a))
            video_step = int(video_frame_number / video.fps) * skip_const
            for i in range(0, video_frame_number, video_step):
                # Save i-th frame as image
                image = video.get_frame(i/video.fps)
                pixel = (image[a][b][0], image[a][b][1], image[a][b][2])
                pixel_list.append(pixel)
            pixel_list_counter = collections.Counter(pixel_list)
            pixel_list_mode = pixel_list_counter.most_common(1)[0][0]
            video_bg_row.append(pixel_list_mode)
        video_bg.append(video_bg_row)
        print(str(a+1) + "_Time(s): " + str(time.time() - time_start))
    video_bg_image = Image.fromarray(np.uint8(video_bg))
    video_bg_image.save('testset/' + video_output_name + '_bg.jpg')

image_new_list = []
pixel_diff_thres = 10 ## For specific pixel, if difference of each R, G, B is less than pixel_diff_thres, we decide that is background

for i in range(0, video_frame_number):
    image = video.get_frame(i/video.fps)
    image = np.asarray(image)
    image_new = image
    for a in range(0, video.size[1]):
        for b in range(0, video.size[0]):
            if (abs(image[a][b][0] - video_bg[a][b][0]) <= pixel_diff_thres) and (abs(image[a][b][1] - video_bg[a][b][1]) <= pixel_diff_thres) and (abs(image[a][b][2] - video_bg[a][b][2]) <= pixel_diff_thres):
                image_new[a][b][0] = 0
                image_new[a][b][1] = 0
                image_new[a][b][2] = 0
    image_new_list.append(image_new)

video_rmbg = ImageSequenceClip(image_new_list, fps=video.fps)
video_rmbg.write_videofile("testset/" + video_output_name + "_bgrm.mp4", fps=video.fps, progress_bar=False)

print("Time(s): " + str(time.time() - time_start))
