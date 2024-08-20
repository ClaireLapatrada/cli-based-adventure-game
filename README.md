# Shared Docs for puye & claire
https://docs.google.com/document/d/1Ez3APubmwXywDIuRtNh3vRW7N-BtwqWG4T7MbZHPJq4/edit?usp=sharing
# 🏫 UofT Great Exam Heist Adventure Game 🕵️‍♂️

Welcome to the University of Toronto's St. George campus, where your wit is tested beyond the exams! In this text-based adventure, you play as a student who's mysteriously lost their essential exam items. Are you ready to embark on a quest filled with humor, puzzles, and a touch of campus lore? 📜✨

## Authors 🖊️

- **[Lapatrada (Claire) Jaroonjetjumnong](https://github.com/help)**  - Buys the caffeine and actually codes.
- **[Sataphon (Puyefang) Obra](https://github.com/puyepuye)** - Github Master and actually codes more.

## Acknowledgments 🙌

- Hat tip to the UofT squirrels for inspiration 🐿️
- Special thanks to the UofT for providing the ambiance and the labyrinthine layout necessary for a real adventure.

## TODO

- clean up pyTA

## Game Rules

### Game Objective
It's the morning of a big test, and you realize you've lost your three essential items:
1. Your Lucky pen
2. Cheat Sheet
3. TCard

Your mission is to navigate the world and 'acquire' these items in your inventory before the test begins.

### General Commands
- **[quit]:** Exit the game
- **[go [direction]]:** Move player in the specified direction
- **[inventory]:** Show player's inventory
- **[look]:** Print the brief description for player's current location
- **[hint]:** Provide game hints for each location
- **[help]:** Show all available commands in player's current location
- **[interaction]:** Show the number of interactions left before the exam starts
- **[item]:** Show all obtainable items in player's current location
- **[score]:** Show player's current amount of Tbucks (score)

Notes: Some commands are not available while solving specific puzzles.

### Interaction Limit
You have exactly 42 interactions.
Each valid command you enter except the General Commands, some event interactions,
and input to the Final Challenge counts as one interaction. Choose wisely to avoid a premature game over!
You can type 'help' to see the valid commands in each location.

### Scoring
Throughout your quest, you'll earn Tbucks by completing side quests. Your prowess in acquiring
Tbucks will determine your final rank: GOLD, SILVER, or BRONZE.
To earn Tbucks, you must engage with the RANDOMLY SPAWNING LIBRARIANS,
either by trading items or by bargaining for extra Tbucks.

### Final Challenge
In the last room, you are tasked with sorting critical information correctly.
CAREFUL: You only get six attempts to place everything in its right place.
Fail, and it's game over.

## Getting Started 🚀

Clone the repository and dare to face the ultimate academic trial:

```bash
git clone https://github.com/puyepuye/project1.git
cd project1
python adventure.py

git add .
git commit -m "message"
git push
# cli-based-adventure-game
