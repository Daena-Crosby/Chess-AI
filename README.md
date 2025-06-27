<<<<<<< HEAD
# Chess AI (Pink Theme)

A simple chess game with a pink-themed GUI, built using Python, Tkinter, and the `python-chess` library. Play as White or Black against an AI powered by the minimax algorithm with selectable difficulty levels.

---

## Features

- Play as White or Black; your pieces are always at the bottom.
- Three AI difficulty levels: Beginner, Intermediate, Advanced.
- Pawn promotion options (Queen, Rook, Bishop, Knight).
- Fully resizable, pink-themed chessboard with graphical pieces.

---

## Requirements

- Python 3.8+
- [python-chess](https://pypi.org/project/python-chess/)
- [Pillow](https://pypi.org/project/Pillow/)

---

## Setup

1. **Clone or download this repository.**

2. **Install dependencies** (preferably in a virtual environment):

    ```sh
    pip install python-chess pillow
    ```

3. **Add chess piece images:**

    - Place 12 PNG images in an `images/` folder inside the project directory.
    - Filenames should be:
      - `wK.png`, `wQ.png`, `wR.png`, `wB.png`, `wN.png`, `wP.png`
      - `bK.png`, `bQ.png`, `bR.png`, `bB.png`, `bN.png`, `bP.png`

---

## Running the Game

From the project directory, run:

```sh
python main.py
```

- The homepage will appear. Choose your color and difficulty, then click **Play**.
- The chessboard will appear. Make moves by clicking squares.
- If you play as Black, the board will flip so your pieces are at the bottom.
- When a pawn reaches the last rank, you will be prompted for promotion.

---

## File Structure

- `main.py` — Entry point; launches the GUI.
- `gui.py` — Handles the GUI, user interaction, and game logic.
- `agent.py` — Contains the AI logic (minimax, evaluation).
- `images/` — Folder containing chess piece images.

---

## Notes

- Make sure your `images/` folder and all image filenames are correct.
- If you encounter errors about missing modules, ensure you installed all dependencies in the correct environment.

---

Enjoy
=======
# Chess-AI
>>>>>>> 715294685bedfe032bce55913b85e6f32b307cd9
