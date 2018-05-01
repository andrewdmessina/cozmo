#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Main Function for Cozmo Smelling Game
# Jonathan Kirner, Matt Bernardini, Michael Lee, Andrew Messina ---- 2018
# University of Missouri- Saint Louis

# ------------------------ THE SMELLING GAME ------------------------ #
'''   Cozmo cannot smell... he doesn't have the right equipment. So the purpose of
 this exercise is to fool the human participants (HPs) into thinking Cozmo can.
 What we're actually doing is having Cozmo visually recognize the lids of the
 smelling jars.

   The game proceeds in the following way:
       After the .py file is opened the program displays a simple welcome
 message and a menu. When the Smelling Game is selected, the user follows
 a series of onscreen prompts while the program waits. The user will have the
 option of proceeding to the next checkpoint or restarting at any time.
'''


# Necessary imports
import cozmo
import pprint
import sys
import asyncio
from cozmo.lights import Light, Color
from random import choice
from label_image import label_cozmo_image
from time import sleep
orange = (Color(name="orange", int_color=0xffab41ff))
orange_light = Light(on_color=orange, off_color=orange)  # Internal bug, the two must match
yellow = (Color(name="yellow", int_color=0xfdff00ff))
yellow_light = Light(on_color=yellow, off_color=yellow)  # Internal bug, the two must match
purple = (Color(name="purple", int_color=0xb000ffff))
purple_light = Light(on_color=purple, off_color=purple)  # Internal bug, the two must match
smells = {
    "Coffee": cozmo.lights.red_light, # changed to red
    "Baby Powder": cozmo.lights.blue_light,
    "Citrus": cozmo.lights.green_light,
    "Vanilla": cozmo.lights.white_light, # changed to white
    "Mint": cozmo.lights.green_light
}
players = {  # Decided at runtime, but it may look something like:
    # "Cozmo": LightCube3
    # "PlayerOne": LightCube1
    # "PlayerTwo": LightCube2
}


# Save message strings (used by both smell_demo and play_game
pause = "\n\nPress any key to continue..."

#smell_demo def -- defines smell demonstration, without engaging the game
async def smell_demo(robot: cozmo.robot.Robot):

    '''
    Label_images should already be called and Cozmo should already be able to detect and
    respond to recognized IR patches. This module merely wraps that behavior in a set of user
    prompts.
    '''
    
    print("Welcome to the Smell Demonstration! Please select a scent container and position it "
          "label-side towards Cozmo. \nWhen he's finished smelling that container, you will be "
          "returned to the main menu. \nTo smell again, please select the Smell Demonstration "
          "option.")

    print(pause)

# play_game def -- defines smell game operation and is called by cozmo_program
async def play_game(robot: cozmo.robot.Robot):
    # Create variables to hold player score
    cozmo_score, player1_score, player2_score = 0, 0, 0


    # Saved Message Strings
    choose_prompt = "Please select a smell container from the bin. Check its smell id number and " \
                    "compare it to the list below. \n"

    # Smell Table - a dictionary of dictionaries of dictionaries
    smell_table = {
        1:{ 'Smell' : "Coffee",
            'Color' : "Red"},
        2:{ 'Smell' : "Baby Powder",
            'Color' : "Blue"},
        3:{ 'Smell' : "Citrus", 
            'Color' : "Yellow"},
        4:{ 'Smell' : "Vanilla",
            'Color' : "White"},
        5:{ 'Smell' : "Mint",
            'Color' : "Green"}
    }

    smell_accepted = "Excellent!"

    smell_prompt = "Now take that same container and allow the players to smell it. Let the " \
                   "humans go first! \nWhen they've both had a smell, point the jar's lid at " \
                   "Cozmo and wait until you hear him make a sniffing noise."

    game_prompt = "Is everyone ready to play?"

    cube_rules = "Okay! If everyone has had a chance to smell, then place the Cozmo Cubes " \
                 "in front of each player and tell them that the cubes will start to change " \
                 "colors. \n\nWhen the right color for the smell appears, they need to tap their " \
                 "cube as fast as possible!"

    game_over = "Woohoo! Great game! You'll be returning to the main menu."

    # main greeting
    print("Excellent choice! Starting the Smelling Game...."\
                "\nThe rules are simple. Up to two humans can compete with Cozmo in this game."\
                 "\n\nYou will choose a smell from the container and enter it's smell id number"\
                 " when prompted. \n\nWhen ready, you'll pass around the smell jar to both " \
                 "human players and Cozmo. Wait till you hear him make a sniffing noise, " \
                 "then follow the onscreen prompts again. \n\nWhen prompted, place the  Cozmo " \
                 "blocks in front of all the players (including Cozmo!). When you " \
                 "trigger the game, the Cozmo Cubes will start to change color. When " \
                 "the right color appears, then the players should hit their " \
                 "cube!\n\nWhoever hits their cube on the right color first wins!\n\nThat's it!")
    input(pause)

    print(choose_prompt)
    print(smell_table)

    smell, color = "", ""
    marker = 1

    # validate smell id number loop
    while marker == 1:

        # smell prompt, smell menu
        marker = 1  # controls loop

        # grab user input
        smell_id = int(input("Enter the appropriate id number here: "))

        # if the string (hopefully a number) input by the user is a member of the smell_table
        # dictionary, then it stores the smell name and its associated color for printing
        try:
            smell = smell_table[smell_id]
            #success! so break out of loop
            marker = -1

        # else it throws an error
        except ValueError:
            print("Sorry! That's not a valid entry! Please enter the number associated with the "
                "appropriate smell. ")

            # failure, proceeds to while loop start

    # smell validated, display prompts, then pause before start of game
    print(smell_accepted)
    print(smell_prompt)
    input(pause)


    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    try:
        players["cozmo"] = await robot.world.wait_for_observed_light_cube(timeout=60.0)
    except asyncio.TimeoutError:
        robot.say_text("SOILED IT")
    finally:
        look_around.stop()
        #robot.say_text("I'M READY").wait_for_completed()
    
    #  Set the players with their cubes.
    players["one"] = choice([x for x in list(robot.world.light_cubes.values()) if x not in list(players.values())])
    players["two"] = choice([x for x in list(robot.world.light_cubes.values()) if x not in list(players.values())])
    #labels, results = labe_cozmo_image(robot)
    #print(labels)
    #print(results)




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


# ---------------------- Main Cozmo API definition ---------------------- #
async def smell_game(robot: cozmo.robot.Robot):
    await label_cozmo_image(robot)

    robot.world.auto_disconnect_from_cubes_at_end(False)  # Takes a while to connect
    await robot.world.connect_to_cubes()  # Will be skipped if Cozmo is connected already.
    # robot.say_text("Hello World").wait_for_completed()

    # Welcome user
    print("Welcome to the Cozmo Smelling App! Please select an option below:")

    # Declare flag
    flag = 1

    # Starts menu loop
    while flag == 1:
        # Main Menu display
        print("Main Menu:")
        print("1\tSmell Game")
        print("2\tSmell Demonstration")
        print("Q\tQuit")

        # Get user input
        select = input("Please enter a number or Q:")

        # Start user input validation loop
        if select == "1":
            await play_game(robot)
        elif select == 2:
            await smell_demo(robot)
        elif select == "Q" or select == "q":
            flag = -1
        else:
            print("That is not a valid option. Please enter either 1 or Q.")

    print("Thanks for playing! Closing App...")
    input("\n\nPress any key to exit. You can always reload from the desktop!")
    sys.exit()


# Main Cozmo API program call
cozmo.run_program(smell_game)