import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

        self.safes = set()
        self.mines = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.safes.add(cell)



class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        # All possible cells in the board
        self.board_available_cells = {(i,j) for i in range(0, height) for j in range(0, width)}

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def shape_sentence_from(self, cell, count):

        # set cell coordinates in the board and list for sorrounding cells
        i, j = cell
        unknown_nearby_cells = []

        # loop through possible steps combination that result in the (maximum) 8 sorrounding cells
        for row_step in [-1, 0, 1]:
            for col_step in [-1, 0, 1]:

                # nearby cell coordinates
                surr_i, surr_j = i + row_step, j + col_step
                nearby_cell = surr_i, surr_j

                # check if tentative nearby cell is in bounds
                if 0 <= surr_i < self.height and 0 <= surr_j < self.width:
                    not_a_mine = nearby_cell not in self.mines
                    not_a_safe = nearby_cell not in self.safes

                    # add only UNKNOWN cells (not mines, not safes) to new sentence
                    if not_a_mine and not_a_safe and nearby_cell != cell:
                        unknown_nearby_cells.append(nearby_cell)

                    # if we KNOW to have a mine nearby, the cell is excluded but the mine counts reduced for
                    # the remaining sentence
                    elif nearby_cell in self.mines:
                        count -= 1

        # create new sentence for filtered SO FAR UNKNOWN cells
        new_sentence = Sentence(unknown_nearby_cells, count)

        # check if any conclusion can be made on the current sentence (i.e., if all are safes or all are mines)
        if count == 0:
            # mark all sentence's cells as safe
            for n_cell in unknown_nearby_cells:
                new_sentence.mark_safe(n_cell)
        elif count == len(unknown_nearby_cells):
            # mark all sentence's cells as safe
            for n_cell in unknown_nearby_cells:
                new_sentence.mark_mine(n_cell)

        print(f'.... Move: {cell} - New sentence: {new_sentence} - New safes: {new_sentence.known_safes()} - New mines: {new_sentence.known_mines()}')
        return new_sentence, new_sentence.known_safes(), new_sentence.known_mines()

    def knowledge_due_diligence(self, sentence)
    # TODO - clean and rewrite this function
        # review sequences combination to see if there's additional inferences
        for idx1, sentence1 in enumerate(self.knowledge):
            unknown_set1 = sentence1.cells - sentence1.known_safes() - sentence1.known_mines()
            count1 = sentence1.count - len(sentence1.known_mines())
            # print(f';;;; {idx1} - {sentence.cells} - Unknown: {unknown_set1}, {count1}')
            for idx2, sentence2 in enumerate(self.knowledge):
                unknown_set2 = sentence2.cells - sentence2.known_safes() - sentence2.known_mines()
                count2 = sentence2.count - len(sentence2.known_mines())
                # print(f'.... {idx2} - {sentence.cells} - Unknown: {unknown_set2}, {count2}')
                # if subset -> difference cells have difference count
                if unknown_set1 < unknown_set2 and len(unknown_set1) > 0:
                    inferred_set = unknown_set2 - unknown_set1
                    count_difference = count2 - count1
                    knowledge_bit = Sentence(inferred_set, count_difference)
                    if knowledge_bit not in self.knowledge:
                        self.knowledge.append(knowledge_bit)

        # review if newly marked mines / safes allow to draw additional conclusions on the content of the remaining cells in the sequences
        all_conclusions_checked = False
        while not all_conclusions_checked:
            all_conclusions_checked = True
            for idx, sentence in enumerate(self.knowledge):
                unknown_set = sentence.cells - sentence.known_safes() - sentence.known_mines()
                unknown_mines_count = sentence.count - len(sentence.known_mines())
                # print(f'**** {idx} - {sentence.cells} - Unknown: {unknown_set}, {unknown_mines_count}')
                if len(unknown_set) > 0:
                    if len(unknown_set) == unknown_mines_count:
                        for cell in unknown_set:
                            self.mark_mine(cell)
                        all_conclusions_checked = False
                    elif unknown_mines_count == 0:
                        for cell in unknown_set:
                            self.mark_safe(cell)
                        all_conclusions_checked = False

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # if move already made or a mine, then nothing to be done
        if cell in self.moves_made:
            return

        if cell in self.mines:
            return

        # otherwise add move to history and mark it as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # create a sentence out of relevant surrounding cells with due checks
        new_sentence, new_safes, new_mines = self.shape_sentence_from(cell, count)

        # update knowledge base (knowledge, safes, mines) based on new_sentence
        self.knowledge.append(new_sentence)
        self.safes = self.safes | new_safes
        self.mines = self.mines | new_mines

        # find conclusions from new knowledge base
        # self.knowledge_due_diligence(new_sentence)

        print(f'.... KSafe - {self.safes}')
        print(f'.... KMine - {self.mines}')

        return


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_possible_moves = self.safes - self.moves_made
        print(f'Safe options: {safe_possible_moves}')
        if len(safe_possible_moves):
            return safe_possible_moves.pop()
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = self.board_available_cells - self.mines - self.moves_made
        if len(possible_moves):
            return possible_moves.pop()
        return None

