from tkinter import *
import settings
import utils

root = Tk()

# Override the setting of window
root.configure(bg='black')
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title('Minesweeper Game')
root.resizable(False, False)

# Create and configure top frame
top_frame = Frame(root,
                  bg = 'black',
                  width = settings.WIDTH, 
                  height = utils.height_prct(25)
)
top_frame.place(x=0, y=0)

# Create and configure left frame
left_frame = Frame(
    root,
    bg = 'black', 
    width = utils.width_prct(25),
    height = utils.height_prct(75)
)
left_frame.place(x = 0, y = utils.height_prct(25))

# Create and configure center frame
center_frame = Frame(
    root,
    bg = 'black', 
    width = utils.width_prct(75), 
    height = utils.height_prct(75), 
)
center_frame.place(
    x = utils.width_prct(25), 
    y = utils.height_prct(25)
)


# Run the window
root.mainloop()