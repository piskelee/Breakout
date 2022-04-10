TITLE = "Breakout"
WIN_WIDTH = 1280
WIN_HEIGHT = 720

BLOCK_MAP = [
    "777777777777",
    "666666666666",
    "555555555555",
    "444444444444",
    "333333333333",
    "222222222222",
    "111111111111",
    "            ",
    "            "]

COLOR_LEGEND = {
    "1": "red",
    "2": "green",
    "3": "blue",
    "4": "orange",
    "5": "purple",
    "6": "bronce",
    "7": "grey"
}

GAP_SIZE = 2
BLOCK_HEIGHT = WIN_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = WIN_WIDTH / len(BLOCK_MAP[0]) - GAP_SIZE
