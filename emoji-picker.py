import sys
import json
import curses
from curses.textpad import Textbox

# This variable is what the script will output
currentEmojis = []

query = ""

# Current Emoji selected
currentLoc = 0

# Open emoji keywords json file
emojiFile = open("emojis.json")

# Load data from emoji keywords json file
emojis = json.load(emojiFile)


def main(stdscr):
    global currentLoc
    global currentEmojis

    # Add cute little "terminal prompt" before cursor
    stdscr.addstr("> ")
    stdscr.refresh()

    # Create a curses window for user input
    inputWin = curses.newwin(1, 30, 0, 2)

    # Make that curses window into a Textbox
    inputLine = Textbox(inputWin)

    # Create a curses window for the autocompleted emojis
    acWin = curses.newwin(1, 60, 3, 2)

    stdscr.refresh()
    inputWin.refresh()

    # Width between emojis
    width = 3

    # Maxmimum row width
    maxwidth = 50

    while True:
        ch = inputWin.getch()
        if not ch:
            continue
        if not inputLine.do_command(ch):
            break
        # If user inputs a tab or right arrow
        if ch == 9 or ch == 261:
            currentLoc += 1
        # Elif user inputs a left arrow
        elif ch == 260:
            currentLoc -= 1
        # Elif user inputs an up arrow
        # elif ch == 259:
        # TODO: move up one row
        # Elif user inputs a down arrow
        # elif ch == 258:
        # TODO: move down one row
        elif ch == 127:
            inputLine.do_command(curses.KEY_BACKSPACE)
        else:
            inputWin.refresh()
            acWin.clear()
            currentEmojis = []
            query = inputLine.gather().strip()
            for emoji, keywords in emojis.items():
                startsWith = False
                for keyword in keywords:
                    if keyword.startswith(query):
                        startsWith = True
                if startsWith:
                    currentEmojis.append(emoji)
        currentXCoord = 1
        locCount = 0
        for emoji in currentEmojis:
            if locCount == currentLoc:
                acWin.addstr(0, currentXCoord, emoji, curses.A_STANDOUT)
            else:
                acWin.addstr(0, currentXCoord, emoji)
            currentXCoord += width
            if currentXCoord > maxwidth:
                break
            locCount += 1
        acWin.refresh()


# Initialize curses for, and then run, main() function
curses.wrapper(main)

# Close emoji keywords json file
emojiFile.close()

# Output, baby.
# https://stackoverflow.com/a/18231470
sys.stdout.write(currentEmojis[currentLoc])
sys.stdout.flush()
sys.exit(0)
