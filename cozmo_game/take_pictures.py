import cozmo
from cozmo.util import degrees
import time
import sys
import os
import asyncio
import uuid
from shutil import copytree, rmtree
imageNumber = 200
def on_new_camera_image(evt, **kwargs):
    print("here", directory)
    pilImage = kwargs['image'].raw_image
    pilImage.save("images/" + directory + "/" + directory + "/" + str(uuid.uuid4()) + ".jpg", "JPEG")

def on_tf_new_camera_image(evt, **kwargs):
    print("here", directory)
    pilImage = kwargs['image'].raw_image
    pilImage.save(directory + "/" + str(uuid.uuid4()) + ".jpg", "JPEG")

def cozmo_program(robot: cozmo.robot.Robot):
    robot.set_head_light(enable=True)
    global directory
    if not os.path.exists('images/' + directory):
        copytree("images/template", "images/" + directory)
        os.makedirs('images/' + directory + '/' + directory)
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image).onceshot()
    time.sleep(1)
    robot.set_head_light(False)
    print("Done: Taking images")

def tf_cozmo_program(robot: cozmo.robot.Robot):
    global directory
    directory = "label"
    if os.path.exists(directory):
        rmtree(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_tf_new_camera_image)
    time.sleep(.1)
    robot.remove_event_handler(cozmo.world.EvtNewCameraImage, on_tf_new_camera_image)

def label_image():
    cozmo.run_program(tf_cozmo_program, use_viewer=True, force_viewer_on_top=True)

def take_pictures():
    new_images = []
    while (True):
        global directory
        directory = input("Please enter object name:\n")
        if (directory == "done"):
            return new_images
        else:
            new_images.append(directory)
        print("Cozmo will take pictures for 10 seconds, please rotate him around the object in order to get the best predictions")
        input("Press enter to continue when you are ready")
        cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
