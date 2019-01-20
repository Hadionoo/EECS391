"""
EECS 391
Chris Hadiono, cxh473
Programming Assignment #1: 8-puzzle problem
"""
#!/usr/bin/python

import sys
import fileinput
import random

# The board that we are trying to reach
goal_board = [1, 2, 3,
              4, 5, 6,
              7, 8, 0]


# Find the index of item in the list if item has already been added to the list
def find_index(a_list, item):
    for index, puzzle in enumerate(a_list):
        if puzzle.board == item.board:
            return index
    return -1


class EightPuzzle:
    # Constructor
    def __init__(self):
        self.start_board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.board = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.h_val = 0
        self.f_val = 0
        self.depth = 0
        self.parent = None
        self.max_n = 1000000

    # Find index of a number in board
    def find(self, num):
        index = 0
        for i in range(0, len(self.board)):
            if self.board[i] == num:
                index = i
        return index

    # Check which moves are allowed from a board, and add their resulting boards to a list
    def get_valid_moves(self):
        valid_moves = []
        blank_index = self.find(0)
        # If blank tile is not on top row
        if not blank_index == 0 and not blank_index == 1 and not blank_index == 2:
            valid_moves.append(self.move_up()[:])
        # If blank tile is not on leftmost row
        if not blank_index == 0 and not blank_index == 3 and not blank_index == 6:
            valid_moves.append(self.move_left()[:])
        # If blank tile is not on rightmost row
        if not blank_index == 2 and not blank_index == 5 and not blank_index == 8:
            valid_moves.append(self.move_right()[:])
        # If blank tile is not on bottom row
        if not blank_index == 6 and not blank_index == 7 and not blank_index == 8:
            valid_moves.append(self.move_down()[:])
        return valid_moves

    # To find the move made to reach the current board
    def get_move_made(self):
        move_made = ""
        end = self.find(0)
        start = self.parent.find(0)
        if start - end == -3:
            move_made = "down"
        elif start - end == 3:
            move_made = "up"
        elif start - end == 1:
            move_made = "left"
        elif start - end == -1:
            move_made = "right"
        return move_made

    # Return a list of the moves that were made to reach the goal board
    def get_solution(self, solution):
        if self.parent == None:
            solution.append(self)
            return solution
        else:
            move_made = self.get_move_made()
            solution.append(self)
            solution.append(move_made)
            return self.parent.get_solution(solution)

    # Solve board with A* Search with input string of either 'h1' or 'h2'
    def solve_a_star(self, h):
        moves = 0
        open_list = [self]
        closed = []

        # Run while there is still a board that hasn't been closed
        while len(open_list) > 0:
            current_puzzle = open_list.pop(0)
            moves += 1
            if moves > self.max_n:
                print "This search has exceeded the max number of nodes checked. Aborting"
                return "This search has exceeded the max number of allowed moves. Aborting"

            if current_puzzle.board == goal_board:
                if len(closed) > 0:
                    solution = current_puzzle.get_solution([])
                    solution.reverse()
                    print "solve A-star", h
                    print "Solution length:", current_puzzle.depth
                    move_path = []
                    for index, item in enumerate(solution):
                        if not index % 2 == 0:
                            move_path.append(item)
                    print "Solution path:", move_path

                    for index, item in enumerate(solution):
                        if index == 0:
                            print "Starting state"
                            item.print_solution_state()
                        elif index % 2 == 0:
                            item.print_solution_state()
                        else:
                            print ("move " + str(item))
                    return solution, current_puzzle.depth
                else:
                    return current_puzzle.board, 0

            new_moves = current_puzzle.get_valid_moves()
            for move in new_moves:
                state = EightPuzzle()
                state.board = move[:]
                if h == "h1":
                    state.h_val = state.hamming_distance()
                elif h == "h2":
                    state.h_val = state.manhattan_distance()
                state.depth = current_puzzle.depth + 1
                state.f_val = state.h_val + state.depth
                state.parent = current_puzzle
                open_index = find_index(open_list, state)
                closed_index = find_index(closed, state)

                if open_index == -1 and closed_index == -1:
                    open_list.append(state)
                # If new node is on open list and existing one is as good or better
                elif open_index > -1:
                    already_seen = open_list[open_index]
                    if state.f_val < already_seen.f_val:
                        already_seen.f_val = state.f_val
                        already_seen.h_val = state.h_val
                        already_seen.parent = state.parent
                        already_seen.depth = state.depth

                elif closed_index > -1:
                    already_seen = closed[closed_index]
                    if state.f_val < already_seen.f_val:
                        state.h_val = already_seen.h_val
                        state.f_val = already_seen.f_val
                        state.depth = already_seen.depth
                        state.parent = already_seen.parent
                        closed.remove(already_seen)
                        open_list.append(state)
            closed.append(current_puzzle)
            open_list = sorted(open_list, key=lambda p: p.f_val)

    def solve_beam(self, k):
        moves = 0
        sorted_children = []
        all_children = []
        emptying = False
        best_children = []
        best_children.append(self)
        while not emptying:
            for child in best_children:
                # Check if any of best k children are the solution and if it is, print result
                if child.board == goal_board:
                    # This section is designed to print out the solution in the way asked for in project description
                    solution = child.get_solution([])
                    solution.reverse()
                    print "solve Beam k =", k
                    print "Solution length:", child.depth + 1
                    move_path = []
                    for index, item in enumerate(solution):
                        if not index % 2 == 0:
                            move_path.append(item)
                    print "Solution path:", move_path

                    for index, item in enumerate(solution):
                        if index == 0:
                            print "Starting state"
                            item.print_solution_state()
                        elif index % 2 == 0:
                            item.print_solution_state()
                        else:
                            print ("move " + str(item))
                    return solution, child.depth
                # Find children of all k best children and add them to priority queue
                else:
                    current_puzzle = child
                    new_moves = current_puzzle.get_valid_moves()
                    for move in new_moves:
                        moves += 1
                        state = EightPuzzle()
                        state.board = move[:]
                        state.h_val = state.manhattan_distance()
                        state.parent = current_puzzle
                        state.depth = current_puzzle.depth + 1
                        exists_index = find_index(all_children, state)
                        # Only add children that haven't already been seen
                        if exists_index == -1:
                            all_children.append(state)
                            sorted_children.append(state)
            # Sort children by lowest h_val
            sorted_children = sorted(sorted_children, key=lambda p: p.h_val)
            # Empty best_children list before adding new set of best k children
            best_children = []
            count = 0

            # Add best k children from PQ to best_children list, empty PQ
            if len(sorted_children) >= k:
                while count < k:
                    best_children.append(sorted_children.pop(0))
                    count += 1
                sorted_children = []
            elif len(sorted_children) < k:
                limit = len(sorted_children)
                while count < limit:
                    best_children.append(sorted_children.pop(0))
                    count += 1
                sorted_children = []
            emptying = False

    # Calculate number of misplaced tiles in board
    def hamming_distance(self):
        num_misplaced = 0
        for i in range(0, 9):
            if not self.board[i] == i:
                num_misplaced += 1
        return num_misplaced

    # Calculate sum of distances of current tile position from goal position in board
    def manhattan_distance(self):
        dist = sum(abs(b % 3 - g % 3) + abs(b // 3 - g // 3)
            for b, g in ((self.board.index(i), goal_board.index(i)) for i in range(0, 9)))
        return dist

    # Swap blank tile with tile above it
    def move_up(self):
        state = self.board[:]
        blank_index = self.find(0)
        if blank_index == 0 or blank_index == 1 or blank_index == 2:
            print "This move is not allowed"
            return
        else:
            temp_blank = state[blank_index]
            swap_index = blank_index - 3
            temp_tile = state[swap_index]
            state[swap_index] = temp_blank
            state[blank_index] = temp_tile
        return state

    # Swap blank tile with tile below it
    def move_down(self):
        state = self.board[:]
        blank_index = self.find(0)
        if blank_index == 6 or blank_index == 7 or blank_index == 8:
            print "This move is not allowed"
            return
        temp_blank = state[blank_index]
        down_swap = blank_index + 3
        temp_down = state[down_swap]
        state[down_swap] = temp_blank
        state[blank_index] = temp_down
        return state

    # Swap blank tile with tile to the right of it
    def move_right(self):
        state = self.board[:]
        blank_index = self.find(0)
        if blank_index == 2 or blank_index == 5 or blank_index == 8:
            print "This move is not allowed"
            return
        temp_blank = state[blank_index]
        right_swap = blank_index + 1
        temp_right = state[right_swap]
        state[right_swap] = temp_blank
        state[blank_index] = temp_right
        return state

    # Swap blank tile with tile to the left of it
    def move_left(self):
        state = self.board[:]
        blank_index = self.find(0)
        if blank_index == 0 or blank_index == 3 or blank_index == 6:
            print "This move is not allowed"
            return
        temp_blank = state[blank_index]
        left_swap = blank_index - 1
        temp_left = state[left_swap]
        state[left_swap] = temp_blank
        state[blank_index] = temp_left
        return state

    # Swap blank tile with the tile in the direction string inputted
    def move(self, direction):
        if direction == "up":
            self.board = self.move_up()
            print "move up"
            self.print_state()
        elif direction == "down":
            self.board = self.move_down()
            print "move down"
            self.print_state()
        elif direction == "left":
            self.board = self.move_left()
            print "move left"
            self.print_state()
        elif direction == "right":
            self.board = self.move_right()
            print "move right"
            self.print_state()

    # Print board in a 3x3 board like in the actual eight-puzzle
    def print_state(self):
        print "printState"
        for index, item in enumerate(self.board, start=1):
            print item,
            if not index % 3:
                print

    # Just removed the print "printState" part from print_state to make solution output cleaner here
    def print_solution_state(self):
        for index, item in enumerate(self.board, start=1):
            print item,
            if not index % 3:
                print

    # Set the board of puzzle to inputted string
    def set_state(self, input_state):
        print "setState", input_state
        if not len(input_state) == 9:
            print "Please enter 9 digits"
            return
        for i in range(0, 9):
            if input_state[i] == 'b':
                self.board[i] = 0
            else:
                self.board[i] = int(input_state[i])

    # Randomly make n valid moves
    def randomize_state(self, n):
        print "randomizeState", n
        for i in range(1, n+1):
            valid_moves = self.get_valid_moves()
            state = random.choice(valid_moves)
            self.board = state

    # Define max number of nodes that can be checked before program aborts finding goal
    def max_nodes(self, nodes):
        print "maxNodes " + str(nodes)
        self.max_n = nodes

def main():
    arg = "test.txt"
    for line in fileinput.input(arg):
        exec line


if __name__ == "__main__":
    main()
