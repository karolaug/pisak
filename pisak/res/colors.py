'''
Globally defined colors
'''
from gi.repository import Clutter

BLACK = Clutter.Color.new(0, 0, 0, 255)
WHITE = Clutter.Color.new(255, 255, 255, 255)
TRANSPARENT = Clutter.Color.new(255, 255, 255, 0)

HILITE_1 = Clutter.Color.new(0, 228, 195, 255)
HILITE_2 = Clutter.Color.new(136, 0, 224, 255)
BUTTON_BG = BLACK

onBACK = BLACK
onFORE = WHITE

offBACK = WHITE
offFORE = BLACK

selBACK = HILITE_1
selFORE = WHITE
