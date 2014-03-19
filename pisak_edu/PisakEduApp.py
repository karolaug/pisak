import sys
import os
import unit
from gi.repository import Clutter
import widgets
import random

class RewardPanel(Clutter.Actor):
    def __init__(self,container):
        super(RewardPanel, self).__init__()
        self.container=container
        layout = Clutter.BinLayout()
        self.set_layout_manager(layout)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.set_reactive(True)
        self.connect('button_release_event', lambda x,y: self.exit_panel())
        self._init_elements()

    def _init_elements(self):
        self._init_reward_info()
        self._init_reward()

    def _init_reward_info(self):
        self.reward_info=widgets.TextField()
        self.add_actor(self.reward_info)

    def _init_reward(self):
        pass #self.reward = song/movie

    def run_reward(self,reward_file_path):
        pass #self.reward.play

    def set_reward_info(self,reward_info):
        self.reward_info.set_text(reward_info)

    def set_font(self,font_name):
        self.reward_info.set_font(font_name)

    def exit_panel(self):
        self.container.change_panel()

class ResultInfoPanel(Clutter.Actor):
    def __init__(self,container):
        super(ResultInfoPanel, self).__init__()
        self.container=container
        layout = Clutter.BinLayout()
        self.set_layout_manager(layout)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.set_reactive(True)
        self.connect('button_release_event', lambda x,y: self.exit_panel())
        self._init_result_info()

    def _init_result_info(self):
        self.result_info=widgets.TextField()
        self.add_actor(self.result_info)

    def set_result_info(self,result_info):
        self.result_info.set_text(result_info)

    def set_font(self,font_name):
        self.result_info.set_font(font_name)

    def exit_panel(self):
        self.container.change_panel()


class PracticePanel(Clutter.Actor):
    def __init__(self,container):
        super(PracticePanel, self).__init__()
        self.container=container
        self.word=container.word
        self.layout=Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.layout.set_column_spacing(10)
        self.layout.set_row_spacing(10)
        self.set_reactive(True)
        self.connect('button_release_event', lambda x,y: self.on_click_event())
        self._init_params()
        self._init_elements()
        self._init_timer()

    def _init_params(self):
        self.idx=0
        self.active_letters_indices=[]
        self.added_letters_indices=[]
        self.font_name='Sans 60'
        self.time_interval=700
        self.word_len = len(self.word)
        self.letter_grid_row_count=5
        self.letter_grid_col_count=6
        self.letter_coords=[]
        while len(self.letter_coords)< self.word_len:
            coords=( random.randint(0, self.letter_grid_col_count-1),random.randint(1,self.letter_grid_row_count-1) )
            if coords not in self.letter_coords:
                self.letter_coords.append(coords)
        self.letter_coords=sorted(self.letter_coords)
        self.on_color=Clutter.Color.new(80,100,220,255)
        self.off_color=Clutter.Color.new(200,200,180,255)
        self.selection_color=Clutter.Color.new(250,12,250,255)
        self.background_color = Clutter.Color.new(100,170,190,255)
        self.white_color=Clutter.Color.new(255,255,255,255)

    def _init_elements(self):
        self._init_buttons()
        self._init_text_field()

    def _init_buttons(self):
        self._init_letter_buttons()
        self._init_action_buttons()

    def _init_letter_buttons(self):
        self.letter_buttons=[]
        self.shuffled_word=list(self.word)
        random.shuffle(self.shuffled_word)
        for i , letter in enumerate(self.shuffled_word ):
            one_button=widgets.LetterButton()
            one_button.set_letter_label(letter)
            one_button.set_font(self.font_name)
            one_button.set_hilite_color(self.off_color)
            self.letter_buttons.append(one_button)
            self.active_letters_indices.append(i)
            self.layout.attach(one_button,  self.letter_coords[i][0] , self.letter_coords[i][1] ,1,1)
            
    def _init_action_buttons(self):
        self.action_buttons=[]
        button_names=['sprawdź','skasuj','wyczyść','czytaj', 'literuj','wróć']
        for col , b in enumerate(button_names):
            one_button=widgets.ActionButton()
            one_button.set_label(b)
            one_button.set_icon_from_file('./icons/'+b+'.png')
            one_button.set_hilite_color(self.off_color)
            self.action_buttons.append(one_button)
            self.layout.attach(one_button,col, self.letter_grid_row_count ,1,1)

        
    def _init_text_field(self):
        self.text_field=widgets.TextField()
        self.text_field.set_font(self.font_name)
        self.layout.attach(self.text_field,0,0,self.letter_grid_col_count,1)
        self.text_field.set_background_color(self.white_color)

    def _init_timer(self):
        self.timer=Clutter.Timeline.new(self.time_interval)
        self.timer.set_repeat_count(-1)
        self.timer.connect('completed', lambda _: self.on_timer_event())
        self.start_timer_cycle()

    def start_timer_cycle(self):
        self.timer.start()

    def stop_timer_cycle(self):
        self.timer.stop()

    def on_timer_event(self):
        if hasattr(self, 'previous_button') and not self.letter_just_added:
            self.previous_button.set_hilite_color(self.off_color)
        else:
            self.letter_just_added=False
        if self.idx >= len(self.active_letters_indices):
            button=self.action_buttons[self.idx - len(self.active_letters_indices)]
        else:
            button=self.letter_buttons[self.active_letters_indices[self.idx]]
        button.set_hilite_color(self.on_color)
        self.previous_button=button
        self.idx = (self.idx +1) % (len(self.action_buttons) + len(self.active_letters_indices))
        
    def on_click_event(self):
        self.stop_timer_cycle()
        self.idx -= 1
        if self.idx >= len(self.active_letters_indices) or self.idx==-1:
            if self.idx==-1:
                button=self.action_buttons[self.idx]
            else:
                button=self.action_buttons[self.idx - len(self.active_letters_indices)]
            button.set_hilite_color(self.selection_color)
            button_label=button.get_label()
            if button_label=='sprawdź':
                self.check_result()
            elif button_label =='skasuj':
                if len(self.added_letters_indices) > 0:
                    self.delete_letter()
            elif button_label=='wyczyść':
                if len(self.added_letters_indices) > 0:
                    self.clear_all()
            elif button_label =='czytaj':
                self.read_out_loud()
            elif button_label=='literuj':
                self.spell()
            elif button_label=='wróć':
                self.back_to_main()
        else:
            self.add_letter(self.idx)
        self.idx=0
        self.start_timer_cycle()

    def add_letter(self,idx):
        self.letter_just_added=True
        button=self.letter_buttons[ self.active_letters_indices[idx] ]
        letter=button.get_letter_label()
        self.text_field.insert_text(letter, -1)
        button.set_letter_label('')
        button.set_hilite_color(self.background_color)
        self.added_letters_indices.append(self.active_letters_indices[idx])
        self.active_letters_indices.remove(self.active_letters_indices[idx])

    def check_result(self):
        user_word=self.text_field.get_text()
        self.container.user_word=user_word
        self.container.change_panel()

    def delete_letter(self):
        letter=self.text_field.get_text()[-1]
        start_pos=len(self.text_field.get_text())-1
        self.text_field.delete_text(start_pos , start_pos+1)
        idx=self.added_letters_indices[-1]
        button=self.letter_buttons[idx]
        button.set_background_color(self.off_color)
        button.set_letter_label(letter)
        self.added_letters_indices.remove(idx)
        self.active_letters_indices.append(idx)
        self.active_letters_indices.sort()

    def clear_all(self):
        for i in self.added_letters_indices:
            letter=self.shuffled_word[i]
            button=self.letter_buttons[i]
            button.set_background_color(self.off_color)
            button.set_letter_label(letter)
            self.active_letters_indices.append(i)
        self.active_letters_indices.sort()
        self.added_letters_indices=[]
        end_pos= len(self.text_field.get_text())
        self.text_field.delete_text(0 ,end_pos)

    def read_out_loud(self):
        print('Reading out loud:   '+self.word)

    def spell(self):
        print('Spelling:    '+self.word)

    def back_to_main(self):
        self.container.back_to_main= True
        self.container.change_panel()

        
class MainPanel(Clutter.Actor):
    def __init__(self,container):
        super(MainPanel, self).__init__()
        self.container=container
        self.layout=Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.layout.set_column_spacing(10)
        self.layout.set_row_spacing(10)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.set_size(1400, 1300)
        self.set_reactive(True)
        self.connect('button_release_event', lambda x,y: self.on_click_event())
        self._init_params()
        self._init_elements()
        self._init_timer()

    def _init_elements(self):
        self._init_result_field()
        self._init_word_field()
        self._init_image()
        self._init_buttons()

    def _init_result_field(self):
        self.result_field=widgets.TextField()
        self.layout.attach(self.result_field , 0, 0, 5 ,1)
        self.result_field.set_x_expand(True)
        
    def _init_word_field(self):
        self.word_field=widgets.TextField()
        self.layout.attach(self.word_field , 0, 1,2,4)
        self.word_field.set_x_expand(True)
        self.word_field.set_y_expand(True)
        
    def _init_image(self):
        self.image=widgets.Image()
        self.layout.attach(self.image , 2, 1,3,4)
        self.image.set_x_expand(True)
        self.image.set_y_expand(True)
        
    def _init_buttons(self):
        self.buttons=[]
        button_names=['ćwicz','czytaj',
                               'literuj','następny','zamknij']
        for col , b in enumerate(button_names):
            one_button=widgets.ActionButton()
            one_button.set_label(b)
            one_button.set_icon_from_file('./icons/'+b+'.png')
            one_button.set_hilite_color(self.off_color)
            self.buttons.append(one_button)
            self.layout.attach(one_button,col,5,1,1)
        self.idx_count=len(self.buttons)

    def update_elements(self,result,word):
        self.update_result_field(result)
        self.update_word_field(word)
        self.update_image(word)

    def update_result_field(self,result):
        text='twój wynik: '+str(result)+' / '+str(self.container.points_limit)+ ' pkt'
        self.result_field.set_text(text)
        self.result_field.set_font(self.result_font)

    def update_word_field(self,word):
        self.word_field.set_text(word)
        self.word_field.set_font(self.word_font)

    def update_image(self,word):
        self.image.set_image_from_file('./words/pictures/' + word + '.png')

    def _init_params(self):
        self.result_font='Sans 40'
        self.word_font='Sans 70'
        self.time_interval=800
	#self.widget_transition_time = 500
        self.idx=0
        self.on_color=Clutter.Color.new(80,100,220,255)
        self.off_color=Clutter.Color.new(200,200,180,255)
        self.selection_color=Clutter.Color.new(250,12,250,255)
        self.scanning_on=False

    def _init_timer(self):
        self.timer=Clutter.Timeline.new(self.time_interval)
        self.timer.set_repeat_count(-1)
        self.timer.connect('completed', lambda _: self.on_timer_event())
        self.start_timer_cycle()
        
    def start_timer_cycle(self):
        self.timer.start()

    def stop_timer_cycle(self):
        self.timer.stop()

    def on_timer_event(self,*args):
        if hasattr(self,'previous_button'):
            self.previous_button.set_hilite_color(self.off_color)
        button=self.buttons[self.idx]
        button.set_hilite_color(self.on_color)
        self.previous_button=button
        self.idx = (self.idx +1) % self.idx_count
        self.scanning_on = True

    def on_click_event(self):
        if self.scanning_on:
            self.stop_timer_cycle()
            button=self.buttons[self.idx -1]
            button.set_hilite_color(self.selection_color)
            self.idx=0
            self.choose_action(button)
            self.start_timer_cycle()

    def choose_action(self,button):
        button_label=button.get_label()
        if button_label=='zamknij':
            self.exit_app()
        elif button_label=='ćwicz':
            self.go_practice()
        elif button_label=='czytaj':
            self.read_out_loud()
        elif button_label=='literuj':
            self.spell()
        elif button_label == 'następny':
            self.change_word()

    def exit_app(self):
        self.container.exit_app()

    def read_out_loud(self):
        print('Reading: ' + self.container.word)

    def go_practice(self):
        self.container.change_panel()

    def spell(self):
        print('Spelling: ' + self.container.word)

    def change_word(self):
        self.container.word_idx = (self.container.word_idx +1) % self.container.word_count
        self.container.word=self.container.words_list[self.container.word_idx]
        self.update_word_field( word= self.container.word)
        self.update_image( word=self.container.word)

    #def slide_in(self,widget):
        #widget.set_opacity(0)
        #widget.animatev(Clutter.AnimationMode.LINEAR, self.widget_transition_time, ["opacity"], [255])

    #def slide_out(self,widget):
        #widget.animatev(Clutter.AnimationMode.LINEAR, self.widget_transition_time, ["opacity"], [0])

class PisakEduContainer(Clutter.Actor):
    def __init__(self):
        super(PisakEduContainer, self).__init__()
        margin = Clutter.Margin()
        margin.left = margin.right = margin.top = margin.bottom = unit.mm(10)
        self.set_margin(margin)
        layout = Clutter.BinLayout()
        self.set_layout_manager(layout)
        self.set_x_expand(True)
        self.set_y_expand(True)
        self._init_training_set()
        self._init_params()
        self._init_panel()

    def _init_training_set(self):
        self.word_pictures_list=os.listdir('./words/pictures')
        self.words_list=[ i[ : i.index('.')] for i in self.word_pictures_list ]
        random.shuffle(self.words_list)

    def _init_params(self):
        self.panel_transition_time=1000
        self.word_idx=0
        self.word_count = len(self.words_list)
        self.result=0
        self.points_limit=2

    def _init_panel(self):
        self.panel=MainPanel(self)
        self.current_panel_name='main'
        self.add_actor(self.panel)
        self.word=self.words_list[self.word_idx]
        self.panel.update_elements(result= self.result, word= self.word)

    def slide_in(self,panel):
        panel.set_opacity(0)
        panel.animatev(Clutter.AnimationMode.LINEAR, self.panel_transition_time, ["opacity"], [255])

    def slide_out(self,panel):
        panel.animatev(Clutter.AnimationMode.LINEAR, self.panel_transition_time, ["opacity"], [0])
        panel.set_reactive(False)

    def change_panel(self):
        new_panel=self.choose_panel()
        self.add_actor(new_panel)
        self.slide_in(new_panel)
        self.slide_out(self.panel)
        self.panel=new_panel

    def choose_panel(self):
        if self.current_panel_name =='main':
            new_panel=PracticePanel(self)
            self.current_panel_name='practice'
        elif self.current_panel_name=='practice':
            if hasattr(self,'back_to_main'):
                new_panel=MainPanel(self)
                self.current_panel_name='main'
                new_word=self.words_list[self.word_idx]
                new_panel.update_elements(result=self.result , word= new_word)
            else:
                new_panel=ResultInfoPanel(self)
                self.current_panel_name='result_info'
                if self.user_word == self.word:
                    self.result+=1
                    self.word_idx = (self.word_idx + 1)%self.word_count
                    if self.result==self.points_limit:
                        info='Brawo!\nZdobyłeś wszystkie punkty.\nKliknij żeby odebrać nagrodę.'
                    elif self.result < self.points_limit:
                        info='Gratulacje.\nWpisałeś poprawne słowo.\nZdobywasz punkt.'
                else:
                    info='Niestety.\nSpróbuj jeszcze raz.'
                new_panel.set_result_info(info)
                new_panel.set_font('Sans 60')
        elif self.current_panel_name =='result_info':
            if self.result==self.points_limit:
                new_panel=RewardPanel(self)
                self.current_panel_name='reward'
                new_panel.set_reward_info('Chcesz wyłączyć? (piosenkę / film)\nKliknij.')
                new_panel.set_font('Sans 40')
                self.result=0
            elif self.result < self.points_limit:
                new_panel=MainPanel(self)
                self.current_panel_name='main'
                self.word=self.words_list[self.word_idx]
                new_panel.update_elements(result=self.result , word= self.word)
        elif self.current_panel_name== 'reward':
            new_panel=MainPanel(self)
            self.current_panel_name='main'
            self.word=self.words_list[self.word_idx]
            new_panel.update_elements(result=self.result , word= self.word)
        return new_panel

    def exit_app(self):
        self.destroy()

class PisakEduStage(Clutter.Stage):
    def __init__(self):
        super(PisakEduStage, self).__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        color = Clutter.Color.new(100,170,190,255)
        self.set_background_color(color)
        self._init_elements()

    def _init_elements(self):
        self.contents = PisakEduContainer()
        self.contents.connect('destroy', lambda _:self.exit_app())
        self.add_actor(self.contents)

    def exit_app(self):
        self.destroy()


class PisakEduApp(object):
    def __init__(self, argv):
        PisakEduApp.APP = self
        Clutter.init(argv)
        self.stage = PisakEduStage()
        self.stage.connect("destroy", lambda _: Clutter.main_quit())
        self.stage.set_fullscreen(True)
        self.stage.show_all()
    
    def main(self):
        Clutter.main()

PisakEduApp(sys.argv).main()
