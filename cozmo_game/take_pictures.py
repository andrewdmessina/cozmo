import cozmo
from cozmo.util import degrees
import time
import sys
import os
imageNumber = 200
def on_new_camera_image(evt, **kwargs):
    print("here", directory)
    pilImage = kwargs['image'].raw_image
    pilImage.save("images/" + directory + "/" + directory + "-11%d.jpg" % kwargs['image'].image_number, "JPEG")


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
    robot.set_head_angle(degrees(10.0)).wait_for_completed()
    robot.set_lift_height(0.0).wait_for_completed()
    global directory
    directory = "label"
    if not os.path.exists('images'):
        os.makedirs('images')
    if not os.path.exists('images/' + directory):
        os.makedirs('images/' + directory)
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)
    time.sleep(.1)

def take_pictures():
    while (True):
        global directory
        directory = input("Please enter object name:\n")
        if (directory == "done"):
            return
        print("Cozmo will take pictures for 10 seconds, please rotate him around the object in order to get the best predictions")
        input("Press enter to continue when you are ready")
        cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
