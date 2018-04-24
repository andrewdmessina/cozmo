import cozmo
from cozmo.util import degrees
import time
import sys
import os

def on_new_camera_image(evt, **kwargs):
    global rtValue
    pilImage = kwargs['image'].raw_image
    pilImage.save("images/" + directory + "/" + directory + "-%d.jpg" % kwargs['image'].image_number, "JPEG")
    rtValue = "images/" + directory + "/" + directory + "-%d.jpg" % kwargs['image'].image_number


def cozmo_program(robot: cozmo.robot.Robot):
    robot.set_head_angle(degrees(10.0)).wait_for_completed()
    robot.set_lift_height(0.0).wait_for_completed()
    global directory
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('images/' + directory):
        os.makedirs('images/' + directory)
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)
    time.sleep(10)
    print("Done: Taking images")

def tf_cozmo_program(robot: cozmo.robot.Robot):
    #robot.set_head_angle(degrees(10.0)).wait_for_completed()
    #robot.set_lift_height(0.0).wait_for_completed()
    global directory
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('images/' + directory):
        os.makedirs('images/' + directory)
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)

def take_pictures():
    global directory
    directory = input("Please enter object name:\n")
    print("Cozmo will take pictures for 10 seconds, please rotate him around the object in order to get the best predictions")
    input("Press enter to continue when you are ready")
    cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)

def tf_picture_taker():
    global directory, rtValue
    cozmo.run_program(tf_cozmo_program, use_viewer=False, force_viewer_on_top=False)
    return rtValue