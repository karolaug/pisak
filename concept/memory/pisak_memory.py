#coding:utf-8

import memory
import sys
import time
from gi.repository import Clutter, Mx

class TimerCycle(object):
	def __init__(self,contents):
		super(TimerCycle, self).__init__()
		self.tiles_table=contents.tiles_table
		self.tiles_table.set_reactive(True)
		self.tiles_table.connect('button_release_event',lambda x,y:self.when_clicked() )
		self._init_params()
		self._init_timer()
	
	def _init_params(self):
		self.time_interval=1000
		self.row_count=self.tiles_table.row_count
		self.col_count=self.tiles_table.col_count
		self.row=0
		self.col=0
		self.direction='rows'
		self.previous_tiles=[]
		
	def _init_timer(self):
		self.timer=Clutter.Timeline.new(self.time_interval)
		self.timer.set_repeat_count(-1)
		self.timer.connect('completed', lambda _: self.on_timer_event())

	def start_cycle(self):
		self.timer.start()

	def stop_cycle(self):
		self.timer.stop()
		
	def on_timer_event(self):
		if self.previous_tiles:
			self.tiles_table.update_tiles(self.previous_tiles,'off')			
		if self.direction=='rows':
			tiles=range(self.row*self.col_count , self.row*self.col_count + self.col_count )
			self.row=(self.row+1) %self.row_count
		elif self.direction=='cols':
			tiles=[self.row*self.col_count + self.col]
			self.col=(self.col+1) %self.col_count
		self.tiles_table.update_tiles(tiles,'on')
		self.previous_tiles=tiles

	def when_clicked(self):
		self.stop_cycle()
		self.tiles_table.update_tiles(self.previous_tiles,'select')
		if self.direction=='rows':
			self.row-=1
			self.direction='cols'
		elif self.direction=='cols':
			self.col-=1
			if self.col== -1:
				self.col=self.col_count-1
			tile= self.row*self.col_count + self.col
			self.tiles_table.action_on_tile(tile)
			self.direction='rows'
			self.row=0
			self.col=0
		self.start_cycle()

class MemoryGame(object):
	def __init__(self):
		self.game = memory.Memory_game((4,6))
		self.game.create_infofield()

class LetterTile(Clutter.Actor):
	def __init__(self):
		super(LetterTile,self).__init__()
		self.layout = Clutter.BinLayout()
		self.set_layout_manager(self.layout)
		self._init_letter_label()

	def _init_letter_label(self):
		self.letter_label=Mx.Label()
		self.add_actor(self.letter_label)
		
	def set_letter_label(self,letter):
		self.letter_label.set_text(letter)
	
class ActionTile(Clutter.Actor):
	def __init__(self):
		super(ActionTile,self).__init__()
		self.layout = Clutter.BoxLayout()
		self.set_layout_manager(self.layout)
		self.layout.set_vertical(True)
		self._init_elements()

	def _init_elements(self):
		self._init_icon()
		self._init_label()

	def _init_icon(self):
		self.icon=Mx.Image()
		self.add_actor(self.icon)

	def _init_label(self):		
		self.label=Mx.Label()
		self.add_actor(self.label)

	def set_label(self,text):
		self.label.set_text(text)

	def set_icon_from_file(self,path):
		self.icon.set_from_file(path)

class PictureTile(Clutter.Actor):
	def __init__(self):
		super(ActionTile,self).__init__()
		self.layout = Clutter.BoxLayout()
		self.set_layout_manager(self.layout)
		self.layout.set_vertical(True)

		self._init_elements()

	def _init_elements(self):
		self._init_icon()
		self._init_label()

	def _init_icon(self):
		self.icon=Mx.Image()
		self.add_actor(self.icon)

	def _init_label(self):		
		self.label=Mx.Label()
		self.add_actor(self.label)

	def set_label(self,text):
		self.label.set_text(text)

	def set_icon_from_file(self,path):
		self.icon.set_from_file(path)

		

class ExecuteAction(object):
	def __init__(self,action_tile,contents):
		super(ExecuteAction, self).__init__()
		self.tile_label=action_tile.label.get_text()
		self.row,self.collumn = None,None
		if self.tile_label != 'zamknij' and self.tile_label != 'reset': 
			self.row,self.collumn = int(self.tile_label.split()[0]),int(self.tile_label.split()[1])
		#else:
		#	self.row,self.collumn = 5,0
		self.contents=contents

			#self.text_field=contents.text_field
		self.tiles=contents.tiles
		self.action_chosen()

	def action_chosen(self):

		if self.tile_label=='reset':
			self.reset_game()
		elif self.tile_label=='zamknij':
			self.exit_app()
		elif self.tile_label[1] == ' ' and self.contents.game.game.displayfield[self.row,self.collumn] == -1:
			self.flip_picture()
		else:
			self.other()

	def insert_space(self):
		space=' '
		cursor_position = len(self.text_buffer.get_text())
		self.text_buffer.insert_text(cursor_position ,space, 1)

	def delete_character(self):
		cursor_position = len(self.text_buffer.get_text())-1
		if cursor_position>=0:
			self.text_buffer.delete_text(cursor_position, 1)

	def clear_all(self):
		text_len=len(self.text_buffer.get_text())
		self.text_buffer.delete_text(0, text_len)

	def exit_app(self):
		self.contents.exit_app()

	def flip_picture(self):
		self.move_info = self.contents.game.game.check_field(self.collumn,self.row)
		self.tiles[6*self.row + self.collumn].set_icon_from_file('./'+str(int(self.contents.game.game.infofield[self.row,self.collumn]))+'.png')	

		if self.move_info == 'second-miss':
				self.contents.revert = 3
				self.contents.row, self.contents.col = self.row, self.collumn
				#self.contents.game.game.revert()
				#self.tiles[6*self.row + self.collumn].set_icon_from_file('./empty.png')
				#self.tiles[6*self.contents.old_row + self.contents.old_col].set_icon_from_file('./empty.png')

		if self.move_info == 'first':
				
				self.contents.old_row, self.contents.old_col = self.row, self.collumn
	
	def reset_game(self):
		self.contents.revert = 0
		self.contents.game = MemoryGame()

		self.row_count=5
		self.col_count=6

		for i in range(len(self.contents.tiles)-6):
			tile = self.contents.tiles[i]
			tile.set_icon_from_file('./empty.png')		

	def other(self):
		print('Executing action: '+self.tile_label)

		

class ToggleHilite(object):
	def __init__(self,tile,toggle):
		super(ToggleHilite, self).__init__()
		if toggle=='off':
			color=Clutter.Color.new(200,150,150,100)
		elif toggle=='on':
			color=Clutter.Color.new(90,100,180,255)
		elif toggle=='select':
			color=Clutter.Color.new(150,40,50,100)
		tile.set_background_color(color)


class TilesTable(Clutter.Actor):
	def __init__(self,contents):
		super(TilesTable,self).__init__()
		letters=['a' ,'i','e', 'r', 'c', 'p','l', 'ę', 'o', 'z', 'w', 'y' ,'m', 'ł', 'h', 'ż' , 'n', 's', 'k', 'u' , 'b', 'ą', 'ś', 'f', 't', 'd', 'j', 'g', 'ó', 'ć' , 'ń', 'ź' ]
		actions=['reset' , 'zamknij']
		self.contents=contents
		self.tiles=[]
		layout=Clutter.GridLayout()
		self.set_layout_manager(layout)
		layout.set_row_spacing(10)
		layout.set_column_spacing(10)
		layout.set_column_homogeneous(True)
		layout.set_row_homogeneous(True)
		self.row_count=5
		self.col_count=6
		for i in range(self.row_count):
			for j in range(self.col_count):
				if i==self.row_count-1:
					if j%3 ==0:
						tile=ActionTile()
						tile.set_icon_from_file('./'+actions[j%2]+'.png')
						tile.set_label(actions[j%2])
						layout.attach(tile,j,i,3,1)
				else:
					tile=ActionTile()
					tile.set_icon_from_file('./empty.png')
					tile.set_label(str(i) + ' ' + str(j))
					layout.attach(tile,j,i,1,1)

				self.tiles.append(tile)

		self.update_tiles(range(len(self.tiles)),'off')

	def update_tiles(self,indices,toggle):
		if self.contents.revert:
			if self.contents.revert == 1:
				self.contents.game.game.revert()
				self.tiles[6*self.contents.row + self.contents.col].set_icon_from_file('./empty.png')
				self.tiles[6*self.contents.old_row + self.contents.old_col].set_icon_from_file('./empty.png')
		
			self.contents.revert -= 1
		
		for i in indices:
			ToggleHilite(self.tiles[i],toggle)

	def action_on_tile(self,index):
		try:
			letter =self.tiles[index].letter_label.get_text()
			cursor_position = len(self.text_buffer.get_text())
			self.text_buffer.insert_text(cursor_position ,letter, 1)
		except AttributeError:
			ExecuteAction(self.tiles[index],self.contents)
			
		#current_txt_coord =self.text_field.text_field.position_to_coords(len(self.text_buffer.get_text()))[3]		   
		#if current_txt_coord >= self.text_field.get_height():
		#	self.text_field.scroll_field()


class TextBuffer(Clutter.TextBuffer):
	def __init__(self):
		super(TextBuffer,self).__init__()

class TextField(Clutter.ScrollActor):
	def __init__(self,text_buffer):
		super(TextField,self).__init__()
		self.set_scroll_mode(Clutter.ScrollMode.VERTICALLY)
		self.text_buffer=text_buffer
		self.layout = Clutter.BinLayout()
		self.set_layout_manager(self.layout)
		white_color=Clutter.Color.new(255,255,255,255)
		self.set_background_color(white_color)
		self.font='Sans 100px'
		self._init_field()
	
	def _init_field(self):		
		self.text_field=Clutter.Text.new_with_buffer(self.text_buffer)
		self.text_field.set_line_wrap(True)
		self.text_field.set_height(1000)
		self.text_field.set_x_expand(True)
		self.text_field.set_editable(True)
		self.text_field.set_y_expand(True)
		self.text_field.set_font_name(self.font)
		self.add_actor(self.text_field)

	def scroll_field(self):
		vertical_distance=100
		animation_time=500
		point=Clutter.Point.alloc()
		Clutter.Point.init(point,0,vertical_distance)
		self.set_easing_mode(Clutter.AnimationMode.LINEAR)
		self.set_easing_duration(animation_time)
		self.scroll_to_point(point)
			

class PisakSpellerContainer(Clutter.Actor):
	def __init__(self,stage):
		super(PisakSpellerContainer, self).__init__()
		self.stage=stage
		margin = Clutter.Margin()
		margin.left = margin.right =  5
		margin.top = margin.bottom = 0
		self.set_margin(margin)
		self._init_elements()
		
	def _init_elements(self):
		
		self.revert = 0
		self.game = MemoryGame()
		self.tiles_table=TilesTable(self)
		self.tiles = self.tiles_table.tiles
		self.tiles_table.set_height(750)
		self.tiles_table.set_width(1350)
		self.tiles_table.set_x_expand(True)
		self.tiles_table.set_y_expand(False)

		self.row = None
		self.col = None	

		self.old_row = None
		self.old_col = None

		layout=Clutter.BoxLayout()
		layout.set_vertical(True)
		layout.set_spacing(20)
		self.set_layout_manager(layout)
		self.add_actor(self.tiles_table)

	def exit_app(self):
		self.stage.exit_app()

class PisakSpellerStage(Clutter.Stage):
	def __init__(self):
		super(PisakSpellerStage, self).__init__()
		color=Clutter.Color.new(180,200,230,100)
		self.set_background_color(color)
		self._init_elements()
	
	def _init_elements(self):
		self.layout = Clutter.BinLayout()
		self.set_layout_manager(self.layout)
		self.contents = PisakSpellerContainer(self)
		self.add_actor(self.contents)

	def exit_app(self):
		self.destroy()

class PisakSpellerApp(object):
	def __init__(self, argv):
		PisakSpellerApp.APP = self
		Clutter.init(argv)
		self.stage = PisakSpellerStage()
		TimerCycle(self.stage.contents).start_cycle()
		self.stage.connect("destroy", lambda _: Clutter.main_quit())
		self.stage.set_fullscreen(True)
		self.stage.show_all()

	def main(self):
		Clutter.main()


PisakSpellerApp(sys.argv).main()
			
