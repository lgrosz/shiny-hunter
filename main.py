from ShinyHunter import hunt_shiny


def usage():
    return 'program <path-to-wav>'

# Shaymin inputs
#   This start just after and ends just before the shiny animation
#   Tip: The shiny animation starts just after the "<pokemon> appeared!" text disappears
SHAYMIN_MACRO = """
5s
DPAD_UP 0.1s
0.1s
A 0.1s
6s
B 0.1s
PLUS 0.1s
DPAD_DOWN 2.5s
DPAD_UP 2.6s
A 0.1s
3.5s
A 0.1s
11.9s
"""

if __name__ == "__main__":
    hunt_shiny(SHAYMIN_MACRO)

