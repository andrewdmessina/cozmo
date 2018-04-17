import cozmo
from random import choice
from time import sleep
from cozmo.lights import Light, Color

orange = (Color(name="orange", int_color=0xffab41ff))
orange_light = Light(on_color=orange, off_color=orange)  # Internal bug, the two must match
yellow = (Color(name="yellow", int_color=0xfdff00ff))
yellow_light = Light(on_color=yellow, off_color=yellow)  # Internal bug, the two must match
purple = (Color(name="purple", int_color=0xb000ffff))
purple_light = Light(on_color=purple, off_color=purple)  # Internal bug, the two must match

smells = {
    "Coffee": orange_light,
    "Baby Powder": cozmo.lights.blue_light,
    "Citrus": yellow_light,
    "Cocoa": orange_light,
    "Mint": cozmo.lights.green_light
}

# Cozmo queues responses which aren't being handled, but have been triggered.
# At the start of the game we could have Cozmo go and grab a random cube and make that one his.
# https://github.com/anki/cozmo-python-sdk/blob/master/examples/tutorials/05_async_python/01_cube_blinker_sync.py#L77


def get_opinion() -> {}:
    return choice(list(smells.values()))


def cube_tapped(evt, **kw):  # It queues actions
    evt.obj.set_lights(get_opinion())
    print(f"Object {evt.obj} was tapped.")


def cozmo_program(robot: cozmo.robot.Robot):
    robot.world.auto_disconnect_from_cubes_at_end(False)  # I'm assuming we don't want this.
    robot.world.connect_to_cubes()  # Will be skipped if Cozmo is connected already.
    # robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    robot.add_event_handler(cozmo.objects.EvtObjectTapped, cube_tapped)

    while True:
        pass


cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program)