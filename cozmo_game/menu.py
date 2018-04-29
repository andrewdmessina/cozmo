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
    print(greeting)
    print(rules_overview)
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