import cozmo
from random import choice
from time import sleep
import asyncio
from cozmo.lights import Light, Color
from label_image import get_opinon
orange = (Color(name="orange", int_color=0xffab41ff))
orange_light = Light(on_color=orange, off_color=orange)  # Internal bug, the two must match
yellow = (Color(name="yellow", int_color=0xfdff00ff))
yellow_light = Light(on_color=yellow, off_color=yellow)  # Internal bug, the two must match
purple = (Color(name="purple", int_color=0xb000ffff))
purple_light = Light(on_color=purple, off_color=purple)  # Internal bug, the two must match

smells = {
    "Coffee": cozmo.lights.red_light, # changed to red
    "Baby Powder": cozmo.lights.blue_light,
    "Citrus": yellow_light,
    "Vanilla": cozmo.lights.white_light, # changed to white
    "Mint": cozmo.lights.green_light
}

players = {  # Decided at runtime, but it may look something like:
    # "Cozmo": LightCube3
    # "PlayerOne": LightCube1
    # "PlayerTwo": LightCube2
}


class GameCube(cozmo.objects.LightCube):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._cycle = None

    def start_light_cycle(self):
        if self._cycle:
            raise ValueError("Light cycle already running")

        async def _cycle():
            while True:
                for color in smells.values():
                    players["cozmo"].set_lights(color)
                    players["one"].set_lights(color)
                    players["two"].set_lights(color)
                    await asyncio.sleep(0.5, loop=self._loop)
        self._cycle = asyncio.ensure_future(_cycle(), loop=self._loop)

    def stop_light_cycle(self):
        if self._cycle:
            self._cycle.cancel()
            self._cycle = None


cozmo.world.World.light_cube_factory = GameCube
# Cozmo queues responses which aren't being handled, but have been triggered.
# At the start of the game we could have Cozmo go and grab a random cube and make that one his.
# https://github.com/anki/cozmo-python-sdk/blob/master/examples/tutorials/05_async_python/01_cube_blinker_sync.py#L77


def get_opinion() -> {}:
    return choice(list(smells.values()))


async def cozmo_program(robot: cozmo.robot.Robot):
    #def player_choice(evt, **kw):
    #    return evt.obj
    #    robot.remove_event_handler(cozmo.objects.EvtObjectTapped, player_choice)
    #    robot.abort_all_actions(robot, False)

    robot.world.auto_disconnect_from_cubes_at_end(False)  # Takes a while to connect
    await robot.world.connect_to_cubes()  # Will be skipped if Cozmo is connected already.
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    try:
        players["cozmo"] = await robot.world.wait_for_observed_light_cube(timeout=60)
    except asyncio.TimeoutError:
        #robot.say_text("SOILED IT")
        return
    finally:
        look_around.stop()
        #robot.say_text("I'M READY").wait_for_completed()

    #  Set the players with their cubes.
    players["one"] = choice([x for x in list(robot.world.light_cubes.values()) if x not in list(players.values())])
    players["two"] = choice([x for x in list(robot.world.light_cubes.values()) if x not in list(players.values())])

    # def cube_tapped2(evt, **kw):
    #     print("Interest\ning")
    while True:
        try:
            print("Waiting for game start")
            await players["cozmo"].wait_for_tap(timeout=10)
            print("Game started")
        except asyncio.TimeoutError:
            print("Time out and start the game from the beginning")
            continue
        finally:
            # Need to smell
            opinons = [graph[1][graph[0].index(1)] for graph in get_opinon(robot)]
            print(opinons)
            players["cozmo"].start_light_cycle()
            players["one"].start_light_cycle()
            players["two"].start_light_cycle()

        #robot.add_event_handler(cozmo.objects.EvtObjectTapped, player_choice)

        try:
            print("Waiting for player opinion")
            players["one"].wait_for_tap(timeout=20)
            players["two"].wait_for_tap(timeout=20)
            await players["cozmo"].wait_for_tap(timeout=20)
            print("Cube tapped")
        except asyncio.TimeoutError:
            print("Players must have left, restart?")
        finally:
            players["cozmo"].stop_light_cycle()
            players["one"].stop_light_cycle()
            players["two"].stop_light_cycle()
            players["cozmo"].set_lights_off()
            players["one"].set_lights_off()
            players["two"].set_lights_off()


cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
#  While not max score
    #  If a block is hit, it's time to play
    #  Turn and check for a smell.
    #  Go back to your cube,
    #  Start cycling lights
    #  If a block is hit, allot points: have some timeout
