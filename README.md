# 🎮 Tic Tac Toe

A desktop Tic Tac Toe game built entirely in **Python** using **PyQt5** — no HTML, CSS, JavaScript, or backend server involved. Everything is native Python GUI. Play against an AI powered by the **Minimax algorithm**, or challenge a friend in 2-player mode. 🧠✨

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ✨ Features

- 🤖 **Single Player vs AI** — powered by the Minimax algorithm (50% perfect play, 50% random, so it's beatable)
- 👥 **2 Player mode** — play locally against a friend, turns alternate automatically
- 🏆 **Winning line highlight** — the winning 3 cells light up green
- ⏱️ **AI "thinking" delay** — a short pause before the AI moves, so it feels more natural
- ⬅️ **Back navigation** — return to the mode-selection screen anytime, with a confirmation prompt if a match is in progress
- 📊 **Live scoreboard** — tracks Player, AI, and Draw counts
- 🎨 **Dark UI theme** with cyan accents

---

## 📁 Project Structure

```
tictactoe_pyqt/
├── main.py             # Full application: UI + game logic + entry point
├── ai.py                # AI logic (Minimax algorithm)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## ⚙️ Requirements

- 🐍 Python 3.8 or higher
- 🖥️ PyQt5

---

## 📥 Installation

1. **Clone the repository**
```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
python main.py
```

> On some systems you may need `python3` instead of `python`.

A window will open showing the mode-selection screen. Choose **Single Player (vs AI)** 🤖 or **2 Player** 👥 to start.

---

## 🧠 How It Works

### `ai.py`
- `check_winner(board)` — checks all 8 winning lines and returns `"X"`, `"O"`, `"Draw"`, or `None`
- `minimax(board, depth, is_maximizing)` — recursively simulates every possible future move to score outcomes
- `get_best_move(board)` — the AI's move-selection logic: 50% of the time it plays a random move, 50% of the time it plays the mathematically optimal move (via Minimax)

### `main.py`
| Class | Responsibility |
|---|---|
| 🖼️ `ModeSelectScreen` | The landing screen — choose "vs AI" or "2 Player" |
| 🎲 `GameScreen` | The board, scoreboard, status text, and all gameplay logic |
| 🪟 `MainWindow` | Uses `QStackedWidget` to switch between the two screens |

---

## 📦 Building a Standalone `.exe` (Windows)

To share the app with someone who doesn't have Python installed:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --icon="icon.ico" --add-data "icon.ico;." --name "TicTacToe" main.py
```

The finished executable will be in `dist/TicTacToe.exe` — fully self-contained, no dependencies needed on the target machine. 🚀

---

## 🔮 Possible Future Improvements

- 🎚️ Difficulty selector (Easy / Medium / Hard)
- 📝 Player name input for 2-player mode
- 🔊 Sound effects
- 💾 Persistent score storage across sessions

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
