import json
import os
from unittest.mock import patch

from definitions import CONFIG_PATH
from simulator.pictures_generation import PicturesGenerator


def test_it_should_generate_new_images():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1
    PHOTOS_PATH = '../photos/'
    images_produced_by_povray = [x for x in os.listdir(PHOTOS_PATH) if x.endswith('.png')]
    image_number_init = len(images_produced_by_povray)

    # Where
    generator = PicturesGenerator(configuration)
    generator.run()
    images_produced_by_povray = [x for x in os.listdir(PHOTOS_PATH) if x.endswith('.png')]
    image_number_end = len(images_produced_by_povray)

    # Then
    image_number = image_number_end - image_number_init
    assert image_number == 2 * configuration['images_curve']


@patch('subprocess.run')
def test_it_should_call_subprocess(subprocess_mock):
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1

    # When
    generator = PicturesGenerator(configuration)
    generator.run()

    # Then
    assert subprocess_mock.call_count == 2


@patch('subprocess.run')
def test_it_should_call_povray(subprocess_mock):
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1

    # When
    generator = PicturesGenerator(configuration)
    generator.run()
    subprocess_args, kwargs = subprocess_mock.call_args

    # Then
    povray_is_called = 'povray' in subprocess_args[0]
    assert povray_is_called
