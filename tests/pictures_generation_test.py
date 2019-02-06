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


def test_it_should_initialize_origin_pool_with_enough_numbers():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1
    configuration['origin_pool_start'] = 100
    configuration['origin_pool_end'] = 500
    configuration['origin_pool_step'] = 2
    expected_length = (configuration['origin_pool_end'] - configuration['origin_pool_start']) / configuration['origin_pool_step']

    # When
    generator = PicturesGenerator(configuration)
    origin_pool = generator.origin_pool

    # Then
    assert len(origin_pool) == expected_length


def test_it_should_initialize_origin_pool_with_image_height():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1

    # When
    generator = PicturesGenerator(configuration)
    origin_pool = generator.origin_pool

    # Then
    for point in origin_pool:
        assert point[1] == configuration['image_height']


def test_it_should_initialize_end_pool_top_with_enough_numbers():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1
    configuration['end_pool_top_start'] = 100
    configuration['end_pool_top_end'] = 500
    configuration['end_pool_top_step'] = 2
    expected_length = (configuration['end_pool_top_end'] - configuration['end_pool_top_start']) / configuration['end_pool_top_step']

    # When
    generator = PicturesGenerator(configuration)
    end_pool_top = generator.end_pool_top

    # Then
    assert len(end_pool_top) == expected_length


def test_it_should_initialize_end_pool_top_with_image_height():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1

    # When
    generator = PicturesGenerator(configuration)
    end_pool_top = generator.end_pool_top

    # Then
    for point in end_pool_top:
        assert point[1] == 0


def test_it_should_initialize_end_pool_right_with_enough_numbers():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1
    configuration['end_pool_right_start'] = 100
    configuration['end_pool_right_end'] = 500
    configuration['end_pool_right_step'] = 2
    expected_length = (configuration['end_pool_right_end'] - configuration['end_pool_right_start']) / configuration['end_pool_right_step']

    # When
    generator = PicturesGenerator(configuration)
    end_pool_right = generator.end_pool_right

    # Then
    assert len(end_pool_right) == expected_length


def test_it_should_initialize_end_pool_right_with_image_height():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1

    # When
    generator = PicturesGenerator(configuration)
    end_pool_right = generator.end_pool_right

    # Then
    for point in end_pool_right:
        assert point[0] == configuration['image_height']


def test_it_should_initialize_radius_pool_with_enough_numbers():
    # Given
    configuration = json.load(open(CONFIG_PATH))
    configuration['images_curve'] = 1
    configuration['radius_pool_start'] = 100
    configuration['radius_pool_end'] = 500
    configuration['radius_pool_step'] = 2
    expected_length = (configuration['radius_pool_end'] - configuration['radius_pool_start']) / configuration['radius_pool_step']

    # When
    generator = PicturesGenerator(configuration)
    radius_pool = generator.radius_pool

    # Then
    assert len(radius_pool) == expected_length
