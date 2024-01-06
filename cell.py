from tkinter import Button, Label
import random
import settings
import ctypes
import sys


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the cell object to Cell.all
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width = 12,
            height = 4
        )
        btn.bind('<Button-1>', self.left_click_actions) # Left click
        btn.bind('<Button-3>', self.right_click_actions) # Right click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location, 
            text = f"Cells left: {Cell.cell_count}",
            bg = 'black',
            fg = 'white',
            font = ("", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
        # If Mines count is equal to the cells left count, player won
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(
                    0,
                    'Congratulations! You won the Game.', 
                    'Game Over',
                     0)
                sys.exit()

    def get_cell_by_axis(self, x, y):
        # Return a cell object based on the value of x, y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self): 
        cells = [ 
            self.get_cell_by_axis(self.x - 1, self.y - 1), 
            self.get_cell_by_axis(self.x - 1, self.y), 
            self.get_cell_by_axis(self.x - 1, self.y + 1), 
            self.get_cell_by_axis(self.x, self.y - 1), 
            self.get_cell_by_axis(self.x + 1, self.y - 1), 
            self.get_cell_by_axis(self.x + 1, self.y), 
            self.get_cell_by_axis(self.x + 1, self.y + 1), 
            self.get_cell_by_axis(self.x, self.y + 1), 
        ]
        cells = [ 
            cell for cell in cells if cell is not None]
        return cells
    
    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(
                text = f'{self.surrounded_cells_mines_length}'
                )
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text = f'Cells Left: {Cell.cell_count}')
                
        # For safety change the background color to SystemButtonFace 
        # in the case the cell was marked as a candidate
        self.cell_btn_object.configure(
            bg = 'SystemButtonFace'
        )

        # Set is_opened to true    
        self.is_opened = True

        # Unbind the events from the cell if it is opened.
        # For example to prevent making a opened cell orange
        self.cell_btn_object.unbind('<Button-1>') # Left click
        self.cell_btn_object.unbind('<Button-3>') # Right click

    def show_mine(self):
        self.cell_btn_object.config(bg = 'red')
        ctypes.windll.user32.MessageBoxW(
            0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit()

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg = 'orange')
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(bg = 'SystemButtonFace')
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all,
            settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"