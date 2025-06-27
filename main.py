import chess
import tkinter as tk
from gui import ChessGUI


if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
