import json
import os
import subprocess

import cv2
import matplotlib.pyplot as plt
import numpy as np

from definitions import CONFIG_PATH, GROUND_PATH, PHOTOS_PATH
from simulator.image_creation import compute_command_arc, \
    draw_central_dashed_arc_on_ground, draw_lateral_complete_arcs_on_ground
from simulator.utils import Point

CONFIGURATION = json.load(open(CONFIG_PATH))


class PictureGeneration:

    def __init__(self, configuration):
        # Configuration
        self.origin_pool = np.arange(configuration['origin_pool_start'],
                                     configuration['origin_pool_end'],
                                     configuration['origin_pool_step'])
        self.origin_pool = [(x, configuration['image_height']) for x in self.origin_pool]

        self.end_pool_top = np.arange(configuration['end_pool_top_start'],
                                      configuration['end_pool_top_end'],
                                      configuration['end_pool_top_step'])
        self.end_pool_top = [(x, 0) for x in self.end_pool_top]

        self.end_pool_right = range(configuration['end_pool_right_start'],
                                    configuration['end_pool_right_end'],
                                    configuration['end_pool_right_step'])
        self.end_pool_right = [(configuration['image_width'], x) for x in self.end_pool_right]

        self.end_pool = self.end_pool_top + self.end_pool_right

        self.radius_pool = range(configuration['radius_pool_start'],
                                 configuration['radius_pool_end'],
                                 configuration['radius_pool_step'])

        # Handling ground images
        ground_images = [x for x in os.listdir(GROUND_PATH) if 'JPG' in x]
        self.grounds = [cv2.imread(GROUND_PATH + '/' + img) for img in ground_images]
        self.grounds = [cv2.resize(x, (configuration['image_width'],
                                       configuration['image_height'])) for x in self.grounds]

        self.image_to_generate = configuration['images_curve']

    def right_direction(self):
        image_number = 0
        while True:
            radius, origin, end = self.generate_coordinates()

            command_angle = int(compute_command_arc(origin, end, radius))
            if command_angle <= 36:
                background_texture = self.grounds[np.random.choice(range(1))]

                img_complete = draw_image_arcs(background_texture, end, origin, radius)
                crop_image_for_povray(background_texture, img_complete)
                filename = '{}_cmd_{}'.format(command_angle, image_number)
                generate_povray_projection(filename)

                # Mirroring the image
                img_complete = cv2.flip(img_complete, 1)
                crop_image_for_povray(background_texture, img_complete)
                filename = '{}_cmd_{}'.format(180 - command_angle, image_number)
                generate_povray_projection(filename)

                image_number += 1
                if image_number == self.image_to_generate:
                    break

    def generate_coordinates(self):
        origin_pt = self.origin_pool[np.random.choice(len(self.origin_pool))]
        end_pt = self.end_pool[np.random.choice(len(self.end_pool))]

        radius = self.radius_pool[np.random.choice(len(self.radius_pool))]
        origin = Point(origin_pt[0], origin_pt[1])
        end = Point(end_pt[0], end_pt[1])

        return radius, origin, end


def crop_image_for_povray(background_texture, img_complete):
    img_final = 255 * np.ones((3 * background_texture.shape[0], 4 * background_texture.shape[1], 3), dtype='uint8')
    img_final[2 * background_texture.shape[0]:, background_texture.shape[1]:2 * background_texture.shape[1],
    :] = img_complete
    plt.imsave('/tmp/test.jpg', img_final)


def draw_image_arcs(background_texture, end, origin, radius):
    img_drawn = draw_central_dashed_arc_on_ground(background_texture, origin, end, radius, (148, 252, 9))
    img_complete = draw_lateral_complete_arcs_on_ground(img_drawn, origin, end, radius, (255, 255, 255))
    return img_complete


def generate_povray_projection(filename):
    command = 'povray -Ipovray_test_cob.pov.j2 Height=176 Width=240 Output_File_Name={}'.format(filename)
    with open(os.devnull, 'w') as devnull:
        subprocess.run(command, shell=True, cwd=PHOTOS_PATH, stdout=devnull)
