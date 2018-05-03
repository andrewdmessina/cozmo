import cozmo
from random import choice
from time import sleep
import asyncio
from cozmo.lights import Light, Color
from label_image import get_opinon
POINTS_NEEDED_TO_WIN = 3

orange = (Color(name="orange", int_color=0xffab41ff))
orange_light = Light(on_color=orange, off_color=orange)  # Internal bug, the two must match
yellow = (Color(name="yellow", int_color=0xfdff00ff))
yellow_light = Light(on_color=yellow, off_color=yellow)  # Internal bug, the two must match
purple = (Color(name="purple", int_color=0xb000ffff))
purple_light = Light(on_color=purple, off_color=purple)  # Internal bug, the two must match

smells = {
    "coffee": cozmo.lights.red_light, # changed to red
    "baby powder": cozmo.lights.blue_light,
    "citrus": yellow_light,
    "vanilla": cozmo.lights.white_light, # changed to white
    "mint": cozmo.lights.green_light
}

players = {  # Decided at runtime, but it may look something like:
    # "cozmo": LightCube3
    # "player1": LightCube1
    # "player2": LightCube2
}

score = {
    'cozmo': 0,
    'player1': 0,
    'player2': 0
}


class GameCube(cozmo.objects.LightCube):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._cycle = None
        self.color = None

    def set_and_remember_lights(self, light_color: cozmo.lights):
        self.color = light_color
        self.set_lights(light_color)

    def start_light_cycle(self):
        if self._cycle:
            raise ValueError("Light cycle already running")

        async def _cycle():
            while True:
                for color in smells.values():
                    self.set_and_remember_lights(color)
                    await asyncio.sleep(0.5, loop=self._loop)
        self._cycle = asyncio.ensure_future(_cycle(), loop=self._loop)

    def stop_light_cycle(self):
        if self._cycle:
            self._cycle.cancel()
            self._cycle = None


cozmo.world.World.light_cube_factory = GameCube
# Cozmo queues responses which aren't being handled, but have been triggered.
# https://github.com/anki/cozmo-python-sdk/blob/master/examples/tutorials/05_async_python/01_cube_blinker_sync.py#L77


def grade_player_decision(tapped_cube: GameCube, cozmos_opinion: cozmo.lights) -> bool:
    player_who_tapped = [k for k,v in players.items() if v == tapped_cube][0]
    if tapped_cube.color == cozmos_opinion:  # If the color of that thing is correct, win
        score[player_who_tapped] += 1
        return True
    else:  # bonk
        for player_name in players.keys():
            if player_name != player_who_tapped:
                score[player_name] += 1
        return False


async def cozmo_program(robot: cozmo.robot.Robot):
    robot.set_head_light(enable=True)
    robot.world.auto_disconnect_from_cubes_at_end(False)  # Takes a while to connect
    await robot.world.connect_to_cubes()  # Will be skipped if Cozmo is connected already.
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    try:
        players["cozmo"] = await robot.world.wait_for_observed_light_cube(timeout=60)
    except asyncio.TimeoutError:
        return
    finally:
        look_around.stop()

    #  Set the players with their cubes.
    players["player1"] = choice([x for x in list(robot.world.light_cubes.values()) if x not in list(players.values())])
    players["player2"] = choice([x for x in list(robot.world.light_cubes.values()) if x not in list(players.values())])

    await robot.set_lift_height(1).wait_for_completed()
    await robot.go_to_object(players["cozmo"], distance_from_object=cozmo.util.Distance(35)).wait_for_completed()

    while max(score.values()) < POINTS_NEEDED_TO_WIN:
        await robot.drive_straight(cozmo.util.distance_mm(-10), cozmo.util.speed_mmps(50)).wait_for_completed()
        print("Waiting for cozmo to smell")
        await robot.turn_in_place(cozmo.util.degrees(90)).wait_for_completed()
        await robot.set_head_angle(cozmo.util.degrees(5)).wait_for_completed()
        have_valid_picture = False
        while not have_valid_picture:
            # Sniff sound
            opinons = [graph[1][graph[0].index(1)] for graph in await get_opinon(robot)]
            if len(set(opinons)) == 2:
                have_valid_picture = True
        await robot.turn_in_place(cozmo.util.degrees(-90)).wait_for_completed()
        await robot.drive_straight(cozmo.util.distance_mm(10), cozmo.util.speed_mmps(50)).wait_for_completed()
        await robot.say_text("Ready to play").wait_for_completed()
        #await robot.set_lift_height(.4, 50).wait_for_completed()
        #await robot.set_lift_height(1).wait_for_completed()
        print("Cozmo has an opinion")

        print(opinons)
        cozmos_guess = [x for x in set(opinons) if x != "junk"][0]
        print(f"Cozmo thinks the smell is: " + cozmos_guess)
        players["cozmo"].start_light_cycle()
        players["player1"].start_light_cycle()
        players["player2"].start_light_cycle()

        try:
            first_cube_tap = await robot.wait_for(cozmo.objects.EvtObjectTapped, timeout=30)
            first_person_to_tap = [k for k,v in players.items() if v == first_cube_tap.obj][0]
        except asyncio.TimeoutError:
            # Probably restart or teardown the game
            continue
        finally:
            first_cube_tap.obj.stop_light_cycle()
            print(f"Player: " + first_person_to_tap + f" tapped first.")
            for cube in set(players.values()) - set([first_cube_tap.obj]):
                cube.stop_light_cycle()
                cube.set_lights_off()
            player_was_correct = grade_player_decision(first_cube_tap.obj, smells[cozmos_guess])
            if player_was_correct:
                robot.say_text("Agree")
            else:
                robot.say_text("Disagree")

        print("Pausing execution until an object is moved.")
        await robot.wait_for(cozmo.objects.EvtObjectMovingStarted,  timeout=30)
        #teardown for next test iteration
        for cube in players.values():
            cube.stop_light_cycle()
            cube.set_and_remember_lights(cozmo.lights.off_light)

cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
#  While not max score
    #  If a block is hit, it's time to play
    #  Turn and check for a smell.
    #  Go back to your cube,
    #  Start cycling lights
    #  If a block is hit, allot points: have some timeout
