import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import chess
import agent  # Your Minimax implementation module
import threading
import time

COLORS = {
    "light": "#ffe6f0",     # Light pink
    "dark": "#ffb6c1",      # Pink for "black" tiles
    "highlight": "#ff66b2", # Hot pink highlight
}

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess AI - Pink Theme")
        self.level_var = tk.StringVar(value="Beginner")
        self.color_var = tk.StringVar(value="White")  # Add color selection
        self.homepage_frame = tk.Frame(root, bg=COLORS["light"])
        self.game_frame = tk.Frame(root, bg=COLORS["light"])
        self.create_homepage()
        self.homepage_frame.pack(fill=tk.BOTH, expand=True)

    def create_homepage(self):
        title = tk.Label(self.homepage_frame, text="Welcome to Chess AI!", font=("Arial", 24, "bold"), bg=COLORS["light"], fg=COLORS["highlight"])
        title.pack(pady=40)
        level_label = tk.Label(self.homepage_frame, text="Choose Difficulty Level:", font=("Arial", 16), bg=COLORS["light"], fg=COLORS["dark"])
        level_label.pack(pady=10)
        level_menu = tk.OptionMenu(self.homepage_frame, self.level_var, "Beginner", "Intermediate", "Advanced")
        level_menu.config(font=("Arial", 14), bg=COLORS["dark"], fg="white", highlightbackground=COLORS["highlight"])
        level_menu.pack(pady=10)
        color_label = tk.Label(self.homepage_frame, text="Choose Your Color:", font=("Arial", 16), bg=COLORS["light"], fg=COLORS["dark"])
        color_label.pack(pady=10)
        color_menu = tk.OptionMenu(self.homepage_frame, self.color_var, "White", "Black")
        color_menu.config(font=("Arial", 14), bg=COLORS["dark"], fg="white", highlightbackground=COLORS["highlight"])
        color_menu.pack(pady=10)
        play_button = tk.Button(self.homepage_frame, text="Play", font=("Arial", 16, "bold"), bg=COLORS["highlight"], fg="white", command=self.start_game)
        play_button.pack(pady=40)

    def start_game(self):
        self.homepage_frame.pack_forget()
        self.setup_game_frame()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        # If user chose Black, let AI move first
        if self.color_var.get() == "Black":
            self.root.after(200, self.ai_move)

    def setup_game_frame(self):
        self.canvas = tk.Canvas(self.game_frame, width=480, height=480, bg=COLORS["light"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.board = chess.Board()
        self.selected_square = None
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Configure>", self.on_resize)
        self.images_raw = self.load_piece_images_raw()
        self.piece_images = {}
        self.square_size = 60  # Default, will be updated on resize
        self.draw_board()

    def load_piece_images_raw(self):
        # Load and store raw PIL images for resizing later
        pieces = ['K', 'Q', 'R', 'B', 'N', 'P']
        colors = ['w', 'b']
        images = {}
        for color in colors:
            for piece in pieces:
                filename = f"images/{color}{piece}.png"
                img = Image.open(filename)
                images[f"{color}{piece}"] = img
        return images

    def resize_piece_images(self, square_size):
        # Resize images to fit the current square size
        self.piece_images = {}
        for key, img in self.images_raw.items():
            resized = img.resize((square_size, square_size), Image.LANCZOS)
            self.piece_images[key] = ImageTk.PhotoImage(resized)

    def draw_board(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.square_size = max(1, min(width, height) // 8)
        if self.square_size < 1:
            return
        self.resize_piece_images(self.square_size)
        user_is_white = self.color_var.get() == "White"
        for rank in range(8):
            for file in range(8):
                # Flip the board if user is black
                display_rank = 7 - rank if user_is_white else rank
                display_file = file if user_is_white else 7 - file
                square_color = COLORS["light"] if (display_rank + display_file) % 2 == 0 else COLORS["dark"]
                x1 = file * self.square_size
                y1 = rank * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=square_color, outline="")
                square_index = chess.square(display_file, display_rank)
                piece = self.board.piece_at(square_index)
                if piece:
                    color = 'w' if piece.color == chess.WHITE else 'b'
                    symbol = piece.symbol().upper()
                    image_key = f"{color}{symbol}"
                    if image_key in self.piece_images:
                        self.canvas.create_image(
                            x1 + self.square_size // 2, y1 + self.square_size // 2,
                            image=self.piece_images[image_key]
                        )
        self.root.update()

    def on_resize(self, event):
        self.draw_board()

    def ask_promotion(self):
        # Simple dialog for promotion choice
        choice = simpledialog.askstring(
            "Promotion", "Promote to (q, r, b, n):", parent=self.root)
        if choice and choice.lower() in ['q', 'r', 'b', 'n']:
            return choice.lower()
        return 'q'  # Default to queen

    def on_click(self, event):
        # Only allow user to move their own color
        file = event.x // self.square_size
        rank = 7 - (event.y // self.square_size)
        square = chess.square(file, rank)

        user_is_white = self.color_var.get() == "White"
        if (user_is_white and self.board.turn != chess.WHITE) or (not user_is_white and self.board.turn != chess.BLACK):
            return  # Not user's turn

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == (chess.WHITE if user_is_white else chess.BLACK):
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            piece = self.board.piece_at(self.selected_square)
            # Only offer promotion if moving a pawn to the last rank
            if (
                piece and piece.piece_type == chess.PAWN and piece.color == (chess.WHITE if user_is_white else chess.BLACK) and
                ((user_is_white and chess.square_rank(self.selected_square) == 6 and chess.square_rank(square) == 7) or
                 (not user_is_white and chess.square_rank(self.selected_square) == 1 and chess.square_rank(square) == 0))
            ):
                promo = self.ask_promotion()
                promo_piece = {'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}[promo]
                move = chess.Move(self.selected_square, square, promotion=promo_piece)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.draw_board()
                self.root.after(200, self.ai_move)
            else:
                self.selected_square = None
            self.draw_board()

    def show_winner_animation(self, winner_text, after_animation=None):
        overlay = self.canvas.create_rectangle(
            0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(),
            fill=COLORS["highlight"], stipple="gray25", outline=""
        )
        text = self.canvas.create_text(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            text=winner_text,
            font=("Arial", 36, "bold"),
            fill="white"
        )
        self.root.update()
        def animate():
            for _ in range(6):
                self.canvas.itemconfigure(overlay, state="normal")
                self.canvas.itemconfigure(text, state="normal")
                self.root.update()
                time.sleep(0.3)
                self.canvas.itemconfigure(overlay, state="hidden")
                self.canvas.itemconfigure(text, state="hidden")
                self.root.update()
                time.sleep(0.2)
            self.canvas.delete(overlay)
            self.canvas.delete(text)
            if after_animation:
                self.root.after(0, after_animation)
        threading.Thread(target=animate, daemon=True).start()

    def ai_move(self):
        if not self.board.is_game_over():
            user_is_white = self.color_var.get() == "White"
            ai_turn = (self.board.turn == chess.BLACK and user_is_white) or (self.board.turn == chess.WHITE and not user_is_white)
            if not ai_turn:
                return
            level = self.level_var.get()
            if level == "Beginner":
                depth = 1
            elif level == "Intermediate":
                depth = 3
            else:
                depth = 5
            best_move = agent.get_best_move(self.board, depth=depth)
            if best_move:
                self.board.push(best_move)
            self.draw_board()
            if self.board.is_game_over():
                result = self.board.result()
                if result == "1-0":
                    winner = "White wins by checkmate!"
                elif result == "0-1":
                    winner = "Black wins by checkmate!"
                else:
                    winner = "Draw!"
                def after_animation():
                    messagebox.showinfo("Game Over", result)
                    self.game_frame.pack_forget()
                    self.homepage_frame.pack(fill=tk.BOTH, expand=True)
                self.show_winner_animation(winner, after_animation)


