'''
Module with screen dimensions of various app elements.
'''
from pisak import unit

# Proportion dimensions

'''Height of screen grid cell'''
GRID_CELL_H = 0.1

'''Height of menu button'''
MENU_BUTTON_H = GRID_CELL_H * 0.85

'''Height of space between buttons'''
H_SPACING = (GRID_CELL_H - MENU_BUTTON_H) * 10 / 11.0

'''Height of photo tile'''

TILE_H = 2 * MENU_BUTTON_H + H_SPACING

# Pixel dimensions

H_SPACING_PX = int(unit.h(H_SPACING))
W_SPACING_PX = 2 * H_SPACING_PX

MENU_BUTTON_H_PX = int(unit.h(MENU_BUTTON_H))
TILE_H_PX = 2 * MENU_BUTTON_H_PX + H_SPACING_PX
TILE_W_PX = 2 * TILE_H_PX
MENU_BUTTON_W_PX = TILE_W_PX
