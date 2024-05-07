import random


table = {
    1: "", 2: "", 3: "",
    4: "", 5: "", 6: "",
    7: "", 8: "", 9: "",
}

combinations = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  # Rows
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  # Columns
        [1, 5, 9], [3, 5, 7]              # Diagonals
    ]


middles = [2, 4, 6, 8 ]
random_numbers = random.choice(middles)
corners = [1, 3, 7, 9]
opposite_corners = {1: 9, 3: 7, 7: 3, 9: 1}
return_corner = random.choice(corners)
player2_score = 0
player1_score = 0


def board():
    for key, value in table.items():
        print(f"{key}: {value}", end="\n" if key % 3 == 0 else ", ")
    print()


def fork_progr(x:int):
    global table, combinations
    count_all_x = set()
    if x == 1:
        table = {i: "" for i in range(1, 10)}
# I separate all combinations which have one X and two empty spots.
# Then I put them into set

    for comb in combinations:
        for position in comb:
            countx = sum(1 for position in comb if table[position] == "X")
            if countx == 1:
                count_all_x.add(tuple(comb))

# I find in which squares these combinations connect and put them into set
# Example (1, 2, 3) and (3, 6, 9) connects at 3

    intersectionX = {num for s in count_all_x for num in s if
            sum([1 for other_s in count_all_x if num in other_s]) > 1}

# Eliminating all numbers containing X's

    intersection2X = []
    for number in intersectionX:
        if table[number] == "":
            intersection2X.append(number)

# If more than one connection is found means that opponent has opposite corners.
# If that happened bot is holding middle
# Only move left is to force opponent to not fork.(achieved by any non corner square

    if len(intersection2X) > 1 and table[random_numbers] == "":
        return random_numbers

# Only one intersection found. Need to check if it's empty.
# if its empty it's the best move to stop fork or start fork attack.
    else:
        for numb in intersection2X:
            if numb != "X" and table[numb] == "":
                print(intersection2X)
                return numb

# Same process repeated for O.

    count_all_O = set()
    for comb in combinations:
        for position in comb:
            countO = sum(1 for position in comb if table[position] == "O")
            if countO == 1:
                count_all_O.add(tuple(comb))

    intersectionO = {num for s in count_all_O for num in s if
            sum([1 for other_s in count_all_O if num in other_s]) > 1}

    intersection2O = []
    for number in intersectionO:
        if table[number] == "":
            intersection2O.append(number)

    if len(intersection2O) >1 and table[random_numbers] == "":
        return random_numbers

    for numb in intersection2O:
        if numb != "O" and table[numb] == "":
            return numb

    return None

board()





def bot():
    global sign, table, combinations


#1. Win : If the player has two in a row, they can place a third to get three in a row.
#2. Block: If the opponent has two in a row, the player must play the third themselves to block the opponent.
    while True:
        for comb in combinations:
            CountX = sum(1 for position in comb if table[position] == "X")
            CountO = sum(1 for position in comb if table[position] == "O")
            if CountO == 2 or CountX == 2:
                for position in comb:
                    if table[position] == "":
                        return position

    #4.Try to detect possible forks, atacking or defending.
    # Find two intersecting lines with one X or O. X or O cant be intersection point.
    # Situation example horizontal: [1 : "", 2 : X, 3 : ""]
    # vertical [3 : "", 6 : "", 9 : X].
    # Point 4 empty connection must be captured.
        if fork_progr(0) is not None:
            return fork_progr(0)


    #5.If center is still empty take center

        if table[5] != "X" and table[5] != "O":
            return 5


    #6. Taking opposite corner

        for corner in corners:
            if table[corner] == "X":
                opposite_corner_position = opposite_corners.get(corner)
                if table[opposite_corner_position] == "":
                    return opposite_corner_position



        for corner in corners:
            if table[corner] == "O":
                opposite_corner_position = opposite_corners.get(corner)
                if table[opposite_corner_position] == "":
                    return opposite_corner_position



    #7. Empty corner: The player plays in a corner square.
    # Corners defined in the beginning of def bot()

        for x in corners:
            if table[return_corner] == "":
                return return_corner




    #8.Empty side: The player plays in a middle square on any of the four sides.
    # Just finishing empty squares

        for position in table:
            if table[position] == "":
                return position



        # Player part with user interferace.



def player(sign: str, is_bot=True):
    global player2_score, player1_score, table, combinations

    while True:
        try:
            if is_bot:
                player_input = int(bot())
                if table[player_input] == "":
                    table[player_input] = sign
                    board()
                    break
            else:
                player_input = input(f'Player {sign} please choose place for {sign} (between 1 and 9)'
                                  '\n if you wish to exit game write 10'
                                  '\n if you wish to see score write 11'
                                  '\n if you wish to restart game write 12'
                                  '\n if you wish to play against bot write 13'
                                  '\n your choice: ')

            if int(player_input) == 10:
                exit()

            if int(player_input) == 11:
                print(f"playerX {player1_score} : playerO {player2_score} ")

            if int(player_input) == 12:
                table = {i: "" for i in range(1, 10)}
                board()
                continue

            if int(player_input) == 13:
                player(sign="O", is_bot= True)
                continue

            if table[int(player_input)] == "X" or table[int(player_input)] == "O":
                print(f"this place is already occupied ")
                continue

            table[int(player_input)] = sign
            board()
            break

        except ValueError:
            print(f"Player {sign} must input number between 1 and 12 instead this : {player_input}")

        except KeyError:
            print(f"Player {sign} must input number between 1 and 12")

        finally:

            if all(value == "X" or value == "O" for value in table.values()):
                print("Game over, no one wins")

                while True:
                    input_game_end = input("Do you wish to play another game Y/N")

                    if input_game_end.upper() == "N":
                        exit()

                    elif input_game_end.upper() == "Y":
                        table = {i: "" for i in range(1, 10)}
                        board()
                        break


                    else:
                        print("wrong input. Write Y to play again or N to end game")

            if (table[1] == table[2] == table[3] == sign
                    or table[4] == table[5] == table[6] == sign
                    or table[7] == table[8] == table[9] == sign
                    or table[1] == table[4] == table[7] == sign
                    or table[2] == table[8] == table[5] == sign
                    or table[3] == table[6] == table[9] == sign
                    or table[1] == table[5] == table[9] == sign
                    or table[7] == table[5] == table[3] == sign):
                print(f"Player {sign} WINS")

                if sign == "X":
                    player1_score += 1

                else:
                    player2_score += 1

                while True:
                    input_game_end = input("Do you wish to play another game Y/N")

                    if input_game_end.upper() == "N":
                        exit()

                    elif input_game_end.upper() == "Y":
                        table = {i: "" for i in range(1, 10)}
                        board()
                        break


                    else:
                        print("wrong input. Write Y to play again or N to end game")





while True:
    player(sign= "X", is_bot=False)
    player(sign="O", is_bot= True)

    # player.player(sign="X", is_bot=True)