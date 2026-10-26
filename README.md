# Camel Up 🐪

A terminal-based Python adaptation of Camel Up, developed as a CS1X course project. Two players take turns rolling dice or placing bets, with a simulation-based advisor to help evaluate betting decisions.

## Features

- Five colored camels with randomized starting stack order.
- Camel stacking: moving a camel also moves any camels above it.
- Two-player turns with betting and dice-rolling actions.
- Betting tickets worth 5, 3, or 2 coins.
- Automatic end-of-leg rankings and payouts.
- Colored terminal display using Colorama.
- Betting advice based on 10,000 random simulations of the remaining rolls.

## Requirements

- Python 3.10 or newer
- Colorama

## Getting Started

Clone the repository and enter its folder:

```bash
git clone https://github.com/jvtieu/Public-Version-Camel_Up-jvtieu.git
cd Public-Version-Camel_Up-jvtieu
```

Install Colorama:

```bash
python -m pip install colorama
```

Start the game:

```bash
python CamelUp.py
```

If your system uses `python3`, substitute that for `python`.

Keep all five Python files in the same folder.

## How to Play

The default players are **Dave** and **Sasha**, each starting with 3 coins.

On your turn, enter:

| Input | Action |
| --- | --- |
| `b` | Take an available betting ticket |
| `r` | Roll a random remaining die, move the corresponding camel, and earn 1 coin |
| `a` | View estimated probabilities and betting advice before choosing an action |

When betting, select a camel using its color letter:

- `r`: Red
- `b`: Blue
- `g`: Green
- `y`: Yellow
- `p`: Purple

The leg ends after all five dice have been rolled. Each betting ticket pays:

- **First place:** The ticket’s printed value
- **Second place:** 1 coin
- **Any other position:** Lose 1 coin

## Betting Advisor

The advisor simulates the rest of the leg 10,000 times using copies of the current board. It estimates each camel’s probability of finishing first or second, then calculates the expected value of available tickets.

It recommends betting when the best ticket’s estimated expected value exceeds the guaranteed 1 coin earned by rolling. Otherwise, it recommends rolling.

These estimates may vary between requests because the simulations use random outcomes.

## Project Files

| File | Purpose |
| --- | --- |
| `CamelUp.py` | Main game loop, player actions, and payouts |
| `Board.py` | Track, camel movement, betting tickets, and rankings |
| `Pyramid.py` | Random dice selection and roll values |
| `Player.py` | Player names, coins, and betting tickets |
| `AI.py` | Simulations, expected values, and betting recommendations |

## Current Scope

This version plays a single leg with two human players. It does not implement a complete multi-leg game or all rules from the original board game. The advisor provides recommendations rather than controlling a player.

Player names can be changed in the main section of `CamelUp.py`.

## Credits

Developed for the CS1X-2026 Camel Up assignment using course-provided starter materials.

Based on the board game Camel Up. This is an educational project and is not an official adaptation.
