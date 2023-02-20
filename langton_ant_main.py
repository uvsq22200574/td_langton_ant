from tkinter import Tk, Canvas, Label, Menu
from ctypes import windll

# Window size
user32 = windll.user32
user32.SetProcessDPIAware()
# Window size END

# Simulation parameters
height, width, posx, posy, pause = 100, 100, 10, 10, -1
# Correction
height += 2
width += 2
# END


window = Tk()
window.title("Game of Life")
window.configure(bg="#000000")
window.state('zoomed')

screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

window.geometry('%dx%d' % (screen_width - 50, screen_height - 50))
# Window def END


canevas = Canvas(window, bg="white", height=((height + 2) * (cell)), width=((width + 2) * (cell)))
canevas.grid(row=0, column=0)


window.mainloop()
