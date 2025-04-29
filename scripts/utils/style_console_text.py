### Pimping up the console output
bold = "\033[1m"  # Bold text
dim = "\033[2m"  # Dim (faint) text
italic = "\033[3m"  # Italic text (not always supported)
underline = "\033[4m"  # Underlined text
blink = "\033[5m"  # Slow blink
reverse = "\033[7m"  # Reverse video (swap foreground and background)
hidden = "\033[8m"  # Hidden text (invisible)
strikethrough = "\033[9m"  # Strikethrough (crossed out; not always supported)

# Regular colors:
black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
# Regular background colors
bg_black = "\033[40m"
bg_red = "\033[41m"
bg_green = "\033[42m"
bg_yellow = "\033[43m"
bg_blue = "\033[44m"
bg_magenta = "\033[45m"
bg_cyan = "\033[46m"
bg_white = "\033[47m"


# High intensity (bright) versions:
bright_black = "\033[90m"
bright_red = "\033[91m"
bright_green = "\033[92m"
bright_yellow = "\033[93m"
bright_blue = "\033[94m"
bright_magenta = "\033[95m"
bright_cyan = "\033[96m"
bright_white = "\033[97m"
# Bright background colors
bg_bright_black = "\033[100m"
bg_bright_red = "\033[101m"
bg_bright_green = "\033[102m"
bg_bright_yellow = "\033[103m"
bg_bright_blue = "\033[104m"
bg_bright_magenta = "\033[105m"
bg_bright_cyan = "\033[106m"
bg_bright_white = "\033[107m"


# Resetting styles
reset = "\033[0m"  # Reset all styles to default
reset_bold = "\033[21m"  # Reset bold or increased intensity
reset_dim = "\033[22m"  # Reset dim
reset_italic = "\033[23m"  # Reset italic
reset_underline = "\033[24m"  # Reset underline
reset_blink = "\033[25m"  # Reset blink
reset_reverse = "\033[27m"  # Reset reverse video
reset_hidden = "\033[28m"  # Reset hidden
reset_strikethrough = "\033[29m"  # Reset strikethrough