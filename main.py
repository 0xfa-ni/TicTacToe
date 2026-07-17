import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt, QTimer

from ai import check_winner, get_best_move

WIN_LINES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]


def get_winning_line(board):
    for line in WIN_LINES:
        a, b, c = line
        if board[a] != "" and board[a] == board[b] == board[c]:
            return line
    return None


# =====================================================
# Shared color palette (matches the original web version)
# =====================================================

BG_GRADIENT = "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #141E30, stop:1 #243B55);"
CARD_BG = "#1f2937"
INNER_CARD_BG = "#111827"
CELL_BG = "#374151"
CELL_HOVER_BG = "#4b5563"
CYAN = "#00ffff"


# =====================================================
# Mode Selection Screen
# =====================================================

class ModeSelectScreen(QWidget):

    def __init__(self, on_mode_selected):
        super().__init__()

        self.on_mode_selected = on_mode_selected
        self.setStyleSheet(BG_GRADIENT)

        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignCenter)
        outer.addWidget(self.build_card())
        self.setLayout(outer)

    def build_card(self):

        card = QFrame()
        card.setFixedWidth(360)
        card.setStyleSheet(f"""
            QFrame {{
                background: {CARD_BG};
                border-radius: 20px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 40, 30, 40)
        layout.setSpacing(18)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("AI Tic Tac Toe")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {CYAN}; font-size: 26px; font-weight: bold; background: transparent;")

        subtitle = QLabel("Choose a game mode to start")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: white; font-size: 14px; background: transparent;")

        vs_ai_btn = QPushButton("Single Player  (vs AI)")
        vs_ai_btn.setFixedHeight(52)
        vs_ai_btn.setCursor(Qt.PointingHandCursor)
        vs_ai_btn.setStyleSheet(self.button_style(CYAN, "black"))
        vs_ai_btn.clicked.connect(lambda: self.on_mode_selected("ai"))

        vs_2p_btn = QPushButton("2 Player")
        vs_2p_btn.setFixedHeight(52)
        vs_2p_btn.setCursor(Qt.PointingHandCursor)
        vs_2p_btn.setStyleSheet(self.button_style("#4CAF50", "white"))
        vs_2p_btn.clicked.connect(lambda: self.on_mode_selected("2player"))

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(vs_ai_btn)
        layout.addWidget(vs_2p_btn)

        card.setLayout(layout)
        return card

    def button_style(self, bg_color, text_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {bg_color};
            }}
            QPushButton:pressed {{
                padding-top: 2px;
            }}
        """


# =====================================================
# Game Screen
# =====================================================

class GameScreen(QWidget):

    def __init__(self, on_back):
        super().__init__()

        self.on_back = on_back
        self.setStyleSheet(BG_GRADIENT)

        self.board = [""] * 9
        self.mode = "ai"
        self.turn = "X"
        self.game_over = False

        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0

        self.build_ui()

    # -------------------------
    # UI Setup
    # -------------------------

    def build_ui(self):

        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedWidth(420)
        card.setStyleSheet(f"""
            QFrame {{
                background: {CARD_BG};
                border-radius: 20px;
            }}
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        title = QLabel("AI Tic Tac Toe")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"color: {CYAN}; font-size: 24px; font-weight: bold; background: transparent;")

        # Scoreboard
        score_layout = QHBoxLayout()
        score_layout.setSpacing(12)

        self.player_score_value = QLabel("0")
        self.ai_score_value = QLabel("0")
        self.draw_score_value = QLabel("0")

        score_layout.addWidget(self.build_score_card("Player", self.player_score_value))
        score_layout.addWidget(self.build_score_card("AI", self.ai_score_value))
        score_layout.addWidget(self.build_score_card("Draw", self.draw_score_value))

        # Status
        self.status_label = QLabel("Your Turn (X)")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: white; font-size: 17px; font-weight: bold; background: transparent;")

        # Board grid
        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent;")
        grid = QGridLayout()
        grid.setSpacing(10)

        self.cell_buttons = []
        self.default_cell_style = self.cell_style(CELL_BG)
        self.hover_cell_style = self.cell_style(CELL_HOVER_BG)
        self.highlight_cell_style = self.cell_style("#0f9b6c")

        for i in range(9):
            btn = QPushButton("")
            btn.setFixedSize(110, 110)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self.default_cell_style)
            btn.clicked.connect(lambda checked, index=i: self.handle_cell_click(index))
            grid.addWidget(btn, i // 3, i % 3)
            self.cell_buttons.append(btn)

        grid_widget.setLayout(grid)

        # Buttons row
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        restart_btn = QPushButton("New Game")
        restart_btn.setFixedHeight(46)
        restart_btn.setCursor(Qt.PointingHandCursor)
        restart_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CYAN};
                color: black;
                font-size: 15px;
                font-weight: bold;
                border-radius: 10px;
            }}
        """)
        restart_btn.clicked.connect(self.restart_game)

        back_btn = QPushButton("Back")
        back_btn.setFixedHeight(46)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {INNER_CARD_BG};
                color: white;
                font-size: 15px;
                font-weight: bold;
                border-radius: 10px;
            }}
        """)
        back_btn.clicked.connect(self.go_back)

        buttons_layout.addWidget(restart_btn)
        buttons_layout.addWidget(back_btn)

        main_layout.addWidget(title)
        main_layout.addLayout(score_layout)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(grid_widget, alignment=Qt.AlignCenter)
        main_layout.addLayout(buttons_layout)

        card.setLayout(main_layout)
        outer.addWidget(card)
        self.setLayout(outer)

    def build_score_card(self, label_text, value_label):

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {INNER_CARD_BG};
                border-radius: 14px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: white; font-size: 13px; background: transparent;")

        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(f"color: {CYAN}; font-size: 26px; font-weight: bold; background: transparent;")

        layout.addWidget(label)
        layout.addWidget(value_label)
        card.setLayout(layout)

        return card

    def cell_style(self, bg_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                font-size: 40px;
                font-weight: bold;
                border-radius: 14px;
            }}
            QPushButton:disabled {{
                color: white;
            }}
        """

    # -------------------------
    # Start / Reset for a mode
    # -------------------------

    def start_new_mode(self, mode):
        self.mode = mode
        self.reset_board()

    def reset_board(self):
        self.board = [""] * 9
        self.turn = "X"
        self.game_over = False

        for btn in self.cell_buttons:
            btn.setText("")
            btn.setStyleSheet(self.default_cell_style)
            btn.setEnabled(True)

        if self.mode == "2player":
            self.status_label.setText("Player 1's Turn (X)")
        else:
            self.status_label.setText("Your Turn (X)")

    def restart_game(self):
        self.reset_board()

    def go_back(self):

        game_in_progress = (not self.game_over) and any(cell != "" for cell in self.board)

        if game_in_progress:
            reply = QMessageBox.question(
                self,
                "Leave match?",
                "A match is currently in progress. Going back will discard it. Continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

        self.on_back()

    # -------------------------
    # Gameplay
    # -------------------------

    def handle_cell_click(self, index):

        if self.game_over or self.board[index] != "":
            return

        if self.mode == "2player":
            self.play_2player_move(index)
        else:
            self.play_ai_mode_move(index)

    def play_ai_mode_move(self, index):

        self.board[index] = "X"
        self.cell_buttons[index].setText("X")

        winner = check_winner(self.board)

        if winner:
            self.finish_game(winner)
            return

        self.status_label.setText("AI Thinking...")
        self.set_board_enabled(False)

        QTimer.singleShot(500, self.play_ai_turn)

    def play_ai_turn(self):

        ai_move = get_best_move(self.board)

        if ai_move != -1:
            self.board[ai_move] = "O"
            self.cell_buttons[ai_move].setText("O")

        winner = check_winner(self.board)

        if winner:
            self.finish_game(winner)
        else:
            self.status_label.setText("Your Turn (X)")
            self.set_board_enabled(True)

    def set_board_enabled(self, enabled):
        for i, btn in enumerate(self.cell_buttons):
            if self.board[i] == "":
                btn.setEnabled(enabled)

    def play_2player_move(self, index):

        self.board[index] = self.turn
        self.cell_buttons[index].setText(self.turn)

        winner = check_winner(self.board)

        if winner:
            self.finish_game(winner)
            return

        self.turn = "O" if self.turn == "X" else "X"

        self.status_label.setText(
            "Player 1's Turn (X)" if self.turn == "X" else "Player 2's Turn (O)"
        )

    # -------------------------
    # Finish game
    # -------------------------

    def finish_game(self, winner):

        self.game_over = True
        self.set_board_enabled(False)

        if winner in ("X", "O"):
            winning_line = get_winning_line(self.board)
            if winning_line:
                for i in winning_line:
                    self.cell_buttons[i].setStyleSheet(self.highlight_cell_style)

        if winner == "X":
            if self.mode == "2player":
                self.status_label.setText("Player 1 Wins!")
            else:
                self.status_label.setText("You Win!")
            self.player_score += 1

        elif winner == "O":
            if self.mode == "2player":
                self.status_label.setText("Player 2 Wins!")
            else:
                self.status_label.setText("AI Wins!")
            self.ai_score += 1

        else:
            self.status_label.setText("Draw!")
            self.draw_score += 1

        self.update_scoreboard()

    def update_scoreboard(self):
        self.player_score_value.setText(str(self.player_score))
        self.ai_score_value.setText(str(self.ai_score))
        self.draw_score_value.setText(str(self.draw_score))


# =====================================================
# Main Window
# =====================================================

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Tic Tac Toe")
        self.resize(480, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.mode_screen = ModeSelectScreen(self.on_mode_selected)
        self.game_screen = GameScreen(self.on_back_to_menu)

        self.stack.addWidget(self.mode_screen)
        self.stack.addWidget(self.game_screen)

        self.stack.setCurrentWidget(self.mode_screen)

    def on_mode_selected(self, mode):
        self.game_screen.start_new_mode(mode)
        self.stack.setCurrentWidget(self.game_screen)

    def on_back_to_menu(self):
        self.stack.setCurrentWidget(self.mode_screen)


# =====================================================
# Entry point
# =====================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
