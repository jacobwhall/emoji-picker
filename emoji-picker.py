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

    # Get dimensions of terminal
    rows, cols = stdscr.getmaxyx()

    # Create a curses window for user input
    inputWin = curses.newwin(1, cols, 0, 2)

    # Make that curses window into a Textbox
    inputLine = Textbox(inputWin)

    # Create a curses window for the autocompleted emojis
    acWin = curses.newwin(rows, cols, 3, 2)

    stdscr.refresh()
    inputWin.refresh()


    # Width between emojis
    width = 5

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
            if currentLoc == len(currentEmojis):
                currentLoc = 0
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
            startWithEmojis = []
            includeEmojis = []
            currentEmojis = []

	    # Search emojis dict for input
            query = inputLine.gather().strip()
            currentLoc = 0
            for emoji, keywords in emojis.items():
                startsWith = False
                includes = False
                for keyword in keywords:
                    subwords = keyword.split("_")
                    for subword in subwords:
                        if subword.startswith(query):
                            startsWith = True
                            break
                        elif query in subword:
                            includes = True
                    if startsWith: break
                if startsWith:
                    startWithEmojis.append(emoji)
                elif includes:
                    includeEmojis.append(emoji)
            currentEmojis = startWithEmojis + includeEmojis
            acWin.addstr(rows - 5, 0, str(len(currentEmojis)) + " ^ matches, " + str(len(includeEmojis)) + " * matches")
        currentXCoord = 1
        locCount = 0
        emojirows = (rows - 6) // 2
        emojicols = (cols - 1) // width
        for emoji in currentEmojis:
            yCoord = (locCount // emojicols) * 2
            if locCount == (emojirows * emojicols):
                break
            xCoord = (locCount % emojicols) * width
            if locCount == currentLoc:
                acWin.addstr(yCoord, xCoord, emoji, curses.A_STANDOUT)
            else:
                acWin.addstr(yCoord, xCoord, emoji)
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
