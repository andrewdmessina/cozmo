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


# playGame def -- defines smell game operation and is called by cozmo_program
def play_game():
    # Create variables to hold player score
    cozmo_score, player1_score, player2_score = 0


    # Save message strings
    pause = "\n\nPress any key to continue..."

    greeting = "Excellent choice! Starting the Smelling Game...."

    rules_overview = "The rules are simple. Up to two humans can compete with Cozmo in this game."\
                 "\n\nYou will choose a smell from the container and enter it's smell id number"\
                 " when prompted. \n\nWhen ready, you'll pass around the smell jar to both " \
                 "human players and Cozmo. Wait till you hear him make a sniffing noise, " \
                 "then follow the onscreen prompts again. \n\nWhen prompted, place the  Cozmo " \
                 "blocks in front of all the players (including Cozmo!). When you " \
                 "trigger the game, the Cozmo Cubes will start to change color. When " \
                 "the right color appears, then the players should hit their " \
                 "cube!\n\nWhoever hits their cube on the right color first wins!\n\nThat's it!"

    choose_prompt = "Please select a smell container from the bin. Check its smell id number and " \
                    "compare it to the list below. \n"

    # Smell Table - a dictionary of dictionaries of dictionaries
    # To call smell, use smell_table[#]
    # To call color, use smell_table[#[smell_name]]

    smell_table = {
        1:{"Coffee" : "Red"},
        2:{"Baby Powder":"Blue"},
        3:{"Citrus" : "Yellow"},
        4:{"Vanilla" : "White"},
        5:{"Mint":"Green"}
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

    # main greeting
    print(greeting)
    print(rules_overview)
    input(pause)

    print(choose_prompt)
    pprint(smell_table)

    smell = ""
    color = ""

    # validate smell id number loop
    while marker == 1:

        # smell prompt, smell menu
        marker = 1  # controls loop

        # grab user input
        smell_id = input("Enter the appropriate id number here: ")

        # if the string (hopefully a number) input by the user is a member of the smell_table
        # dictionary, then it stores the smell name and its associated color for printing
        if smell_table.has_key(smell_id) :
            smell = smell_table[smell_id]
            color = smell_table[smell_id[smell]]

            #success! so break out of loop
            marker = -1

        # else it throws an error
        else :
            print("Sorry! That's not a valid entry! Please enter the number associated with the "
                "appropriate smell. ")

            # failure, proceeds to while loop start

    # smell validated, display prompts, then pause before start of game
    print(smell_accepted)
    print(smell_prompt)
    input(pause)

    # display cube rules and prepare to run game
    print(cube_rules)
    print(game_prompt)
    input(pause)

    # run color match cube routine
    color_match = "\nThe game has begun! The smell is: ", smell, "and the color is: ", color
    print(color_match)
    input(pause)


    # cube routine
    # cube routine
    # cube routine
    # cube routine

    # store score
    # assign results of each smell game to one of the score variables
    # cozmo_score, player1_score, player2_score (declared above)

    return

def play_again()

# ---------------------- Main Cozmo API definition ---------------------- #
def cozmo_program(robot: cozmo.robot.Robot):

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
        # print("2\tSmell Demonstration")
        print("Q\tQuit")

        # Get user input
        select = input("Please enter a number or Q:")

        # Start user input validation loop
        if select == 1:
            play_game()
            play_again()
        elif select == "Q" or select == "q":
            flag = -1
        else:
            print("That is not a valid option. Please enter either 1 or Q.")

    print("Thanks for playing! Closing App...")
    input("\n\nPress any key to exit. You can always reload from the desktop!")
    sys.exit()

# Main Cozmo API program call
cozmo.run_program(cozmo_program)