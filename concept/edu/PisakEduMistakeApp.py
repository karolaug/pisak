import sys
import os
import random
from gi.repository import Clutter
import unit
import widgets
import switcher_app


class RewardPanel(Clutter.Actor):
    def __init__(self,container):
        super(RewardPanel, self).__init__()
        self.container = container
        layout = Clutter.BinLayout()
        self.set_layout_manager(layout)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self._init_elements()

    def _init_elements(self):
        self._init_reward_info()
        self._init_reward()

    def _init_reward_info(self):
        self.reward_info = widgets.TextField()
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
        new_panel_name = 'main'
        return self.container.change_panel(new_panel_name)

    def create_cycle(self):
        return _RewardPanelCycle(self)


class _RewardPanelCycle(object):
    def __init__(self, panel):
        self.panel = panel
        self.interval = sys.maxsize

    def expose_next(self):
        pass

    def stop(self):
        pass

    def select(self):
        return self.panel.exit_panel()


class ResultInfoPanel(Clutter.Actor):
    def __init__(self,container):
        super(ResultInfoPanel, self).__init__()
        self.container = container
        self.word = container.word
        self.user_word = container.user_word
        self.result = container.result
        layout = Clutter.BinLayout()
        self.set_layout_manager(layout)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self._init_result_info()

    def _init_result_info(self):
        self.result_info = widgets.TextField()
        self.add_actor(self.result_info)

    def set_result_info(self,result_info):
        self.result_info.set_text(result_info)

    def set_font(self,font_name):
        self.result_info.set_font(font_name)

    def exit_panel(self):
        if self.user_word == self.word and self.result == 0:
            new_panel_name = 'reward'
        else:
            new_panel_name = 'main'
        return self.container.change_panel(new_panel_name)

    def create_cycle(self):
        return _ResultInfoPanelCycle(self)


class _ResultInfoPanelCycle(object):
    def __init__(self, panel):
        self.panel = panel
        self.interval = sys.maxsize

    def expose_next(self):
        pass

    def stop(self):
        pass

    def select(self):
        return self.panel.exit_panel()


class SecondPracticePanel(Clutter.Actor):
    def __init__(self,container):
        super(SecondPracticePanel, self).__init__()
        self.container = container
        self.word = container.word
        self.mistake_index = container.mistake_index
        self.points_limit = container.points_limit
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.layout.set_column_spacing(10)
        self.layout.set_row_spacing(10)
        self._init_params()
        self._init_elements()

    def _init_params(self):
        self.font_name = 'Sans 60'
        self.row_count = 5
        self.col_count = 8
        self.on_color = Clutter.Color.new(80,100,220,255)
        self.off_color = Clutter.Color.new(200,200,180,255)
        self.selection_color = Clutter.Color.new(250,12,250,255)
        self.background_color = Clutter.Color.new(100,170,190,255)
        self.white_color = Clutter.Color.new(255,255,255,255)

    def _init_elements(self):
        self._init_buttons()
        self._init_text_field()

    def _init_buttons(self):
        self.buttons = []
        self._init_letter_buttons()
        self._init_action_buttons()

    def _init_letter_buttons(self):
        letters = ['a' ,'i','e', 'r', 'c', 'p','l', 'ę', 'o', 'z', 'w',
                   'y' ,'m', 'ł', 'h', 'ż' , 'n', 's', 'k', 'u' , 'b',
                   'ą', 'ś', 'f', 't', 'd', 'j', 'g', 'ó', 'ć' , 'ń', 'ź']
        for i, letter in enumerate(letters):
            if i % self.col_count == 0:
                if i != 0:
                    self.buttons.append(one_row)
                one_row = []
            button = widgets.LetterButton()
            button.set_letter_label(letter)
            button.set_font(self.font_name)
            button.set_hilite_color(self.off_color)
            one_row.append(button)
            self.layout.attach(button, i % self.col_count, i / self.col_count + 1, 1, 1)
        self.buttons.append(one_row)

    def _init_action_buttons(self):
        one_row = []
        button_names = ['powrót','sprawdź','skasuj','czytaj', 'literuj','wróć']
        for col, b in enumerate(button_names):
            button = widgets.ActionButton()
            button.set_label(b)
            button.set_icon_from_file('./icons/'+b+'.png')
            button.set_hilite_color(self.off_color)
            one_row.append(button)
            if b == 'powrót':
                self.layout.attach(button, col, self.row_count + 1, 2, 1)
            elif b == 'wróć':
                self.layout.attach(button, col + 1, self.row_count + 1, 2, 1)
            else:
                self.layout.attach(button, col + 1, self.row_count + 1, 1, 1)
        self.buttons.append(one_row)

    def _init_text_field(self):
        self.text_field = widgets.TextField()
        self.text_field.set_font(self.font_name)
        self.layout.attach(self.text_field, 0, 0, self.col_count, 1)
        self.text_field.set_background_color(self.white_color)
        self.user_word = list(self.word)
        self.user_word[self.mistake_index] = '_'
        self.text_field.set_text(''.join(self.user_word))

    def select_action(self, button):
        try:
            button_label = button.get_label()
            if button_label == 'powrót':
                return self.back_to_first_practice()
            if button_label == 'sprawdź':
                return self.check_result()
            elif button_label == 'skasuj':
                self.user_word = self.text_field.get_text()
                if list(self.user_word)[self.mistake_index] != '_':
                    self.delete_letter()
            elif button_label == 'czytaj':
                self.read_out_loud()
            elif button_label == 'literuj':
                self.spell()
            elif button_label == 'wróć':
                return self.back_to_main()
        except AttributeError:
            self.user_word = self.text_field.get_text()
            if list(self.user_word)[self.mistake_index] == '_':
                self.select_letter(button)

    def back_to_first_practice(self):
        new_panel_name = 'first_practice'
        return self.container.change_panel(new_panel_name)

    def select_letter(self, button):
        letter = button.get_letter_label()
        pos = self.mistake_index
        self.text_field.delete_text(pos, pos+1)
        self.text_field.insert_text(letter, pos)

    def check_result(self):
        self.container.user_word = self.text_field.get_text()
        new_panel_name = 'result_info'
        return self.container.change_panel(new_panel_name)

    def delete_letter(self):
        pos = self.mistake_index
        self.text_field.delete_text(pos, pos+1)
        self.text_field.insert_text('_', pos)

    def read_out_loud(self):
        print('Reading out loud:   ' + self.word)

    def spell(self):
        print('Spelling:    ' + self.word)

    def back_to_main(self):
        new_panel_name = 'main'
        return self.container.change_panel(new_panel_name)

    def create_cycle(self):
        return _SecondPracticePanelCycle(self)


class _SecondPracticePanelCycle(object):
    def __init__(self, panel):
        self.panel = panel
        self.interval = 800
        self.direction = 'y'
        self.previous = None
        self.x_index, self.y_index = None, None
        self.on_color = Clutter.Color.new(80,100,220,255)
        self.off_color = Clutter.Color.new(200,200,180,255)
        self.selection_color = Clutter.Color.new(250,12,250,255)

    def expose_next(self):
        if (self.x_index and self.y_index) != None:
            if self.direction == 'y':
                if self.previous == 'x':
                    button = self.panel.buttons[self.y_index][self.x_index]
                    button.set_background_color(self.off_color)
                    self.x_index, self.y_index = -1, -1
                    self.previous = 'y'
                else:
                    for button in self.panel.buttons[self.y_index]:
                        button.set_background_color(self.off_color)
                self.y_index = (self.y_index + 1) % len(self.panel.buttons)
            elif self.direction == 'x':
                if self.previous == 'y':
                    for button in self.panel.buttons[self.y_index]:
                        button.set_background_color(self.off_color)
                else:
                    button = self.panel.buttons[self.y_index][self.x_index]
                    button.set_background_color(self.off_color)
                self.x_index = (self.x_index + 1) % len(self.panel.buttons[self.y_index])
        else:
            self.x_index, self.y_index = -1, 0
        if self.direction == 'y':
            for button in self.panel.buttons[self.y_index]:
                button.set_background_color(self.on_color)
        elif self.direction == 'x':
            button = self.panel.buttons[self.y_index][self.x_index]
            button.set_background_color(self.on_color)

    def stop(self):
        if (self.x_index and self.y_index) != None:
            if self.direction == 'y':
                for button in self.panel.buttons[self.y_index]:
                    button.set_background_color(self.off_color)
            elif self.direction == 'x':
                button = self.panel.buttons[self.y_index][self.x_index]
                button.set_background_color(self.off_color)
            self.x_index, self.y_index = None, None

    def select(self):
        if self.direction == 'y':
            for button in self.panel.buttons[self.y_index]:
                button.set_background_color(self.selection_color)
            self.direction = 'x'
            self.previous = 'y'
        elif self.direction == 'x':
            button = self.panel.buttons[self.y_index][self.x_index]
            button.set_background_color(self.selection_color)
            self.direction = 'y'
            self.previous = 'x'
            return self.panel.select_action(button)


class FirstPracticePanel(Clutter.Actor):
    def __init__(self,container):
        super(FirstPracticePanel, self).__init__()
        self.container = container
        self.word = container.word
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.layout.set_column_spacing(10)
        self.layout.set_row_spacing(10)
        self._init_params()
        self._init_elements()

    def _init_params(self):
        self.font_name = 'Sans 60'
        self.mistake_index = random.randint(0, len(self.word) - 1)
        self.off_color = Clutter.Color.new(200,200,180,255)
        self.white_color = Clutter.Color.new(255,255,255,255)
        self.green_color = Clutter.Color.new(20,220,20,255)

    def _init_elements(self):
        self._init_buttons()
        self._init_text_field()

    def _init_buttons(self):
        for i in [1, 2, 3, 5, 6, 7]:
            a = Clutter.Actor()
            self.layout.attach(a, 0, i, 1, 1) #filling
        self.buttons = []
        self._init_number_buttons()
        self._init_action_buttons()

    def _init_number_buttons(self):
        for i in range(len(self.word)):
            button = widgets.TextField()
            button.set_text(str(i+1))
            button.set_font(self.font_name)
            button.set_background_color(self.off_color)
            self.buttons.append(button)
            self.layout.attach(button, i, 4, 1, 2)

    def _init_action_buttons(self):
        button_names = ['czytaj', 'literuj','wróć']
        for col, b in enumerate(button_names):
            button = widgets.ActionButton()
            button.set_label(b)
            button.set_icon_from_file('./icons/'+b+'.png')
            button.set_hilite_color(self.off_color)
            self.buttons.append(button)
            self.layout.attach(button, col*4, 7, 4, 2)

    def _init_text_field(self):
        letters = ['a' ,'i','e', 'r', 'c', 'p','l', 'ę', 'o', 'z', 'w',
                   'y' ,'m', 'ł', 'h', 'ż' , 'n', 's', 'k', 'u' , 'b',
                   'ą', 'ś', 'f', 't', 'd', 'j', 'g', 'ó', 'ć' , 'ń', 'ź']
        index = random.randint(0, len(letters) - 1)
        while letters[index] == list(self.word)[self.mistake_index]:
            index = random.randint(0, len(letters) - 1)
        user_word = list(self.word)
        user_word[self.mistake_index] = letters[index]
        self.user_word = ''.join(user_word)
        self.text_field = widgets.TextField()
        self.text_field.set_text(self.user_word)
        self.text_field.set_font(self.font_name)
        self.layout.attach(self.text_field, 0, 0, 12, 2)
        self.text_field.set_background_color(self.white_color)

    def read_out_loud(self):
        print('Reading out loud:   ' + self.word)

    def spell(self):
        print('Spelling:    ' + self.word)

    def back_to_main(self):
        new_panel_name = 'main'
        return self.container.change_panel(new_panel_name)

    def select_letter(self, button):
        index = int(button.get_text())
        user_word = self.text_field.get_text()
        if user_word[index - 1] == self.word[index - 1]:
            button.set_background_color(self.green_color)
        else:
            new_panel_name = 'second_practice'
            self.container.user_word = user_word
            self.container.mistake_index = self.mistake_index
            return self.container.change_panel(new_panel_name)

    def select_action(self, button):
        try:
            button_label = button.get_label()
            if button_label == 'czytaj':
                self.read_out_loud()
            elif button_label == 'literuj':
                self.spell()
            elif button_label == 'wróć':
                return self.back_to_main()
        except AttributeError:
            return self.select_letter(button)

    def create_cycle(self):
        return _FirstPracticePanelCycle(self)


class _FirstPracticePanelCycle(object):
    def __init__(self, panel):
        self.panel = panel
        self.interval = 800
        self.index = None
        self.on_color = Clutter.Color.new(80,100,220,255)
        self.off_color = Clutter.Color.new(200,200,180,255)
        self.selection_color = Clutter.Color.new(250,12,250,255)

    def expose_next(self):
        if self.index != None:
            self.panel.buttons[self.index].set_background_color(self.off_color)
            self.index = (self.index + 1) % len(self.panel.buttons)
        else:
            self.index = 0
        self.panel.buttons[self.index].set_background_color(self.on_color)

    def stop(self):
        if self.index != None:
            self.panel.buttons[self.index].set_background_color(self.off_color)
            self.index = None

    def select(self):
        button = self.panel.buttons[self.index]
        button.set_background_color(self.selection_color)
        return self.panel.select_action(button)


class MainPanel(Clutter.Actor):
    def __init__(self,container):
        super(MainPanel, self).__init__()
        self.container = container
        self.word = container.word
        self.result = container.result
        self.word_index = container.word_index
        self.words_list = container.words_list
        self.points_limit = container.points_limit
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.layout.set_column_spacing(10)
        self.layout.set_row_spacing(10)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self._init_params()
        self._init_elements()

    def _init_elements(self):
        self._init_result_field()
        self._init_word_field()
        self._init_image()
        self._init_buttons()
        self.update_elements()

    def _init_result_field(self):
        self.result_field = widgets.TextField()
        self.layout.attach(self.result_field, 0, 0, 5, 1)
        self.result_field.set_x_expand(True)

    def _init_word_field(self):
        self.word_field = widgets.TextField()
        self.layout.attach(self.word_field, 0, 1, 2, 4)
        self.word_field.set_x_expand(True)
        self.word_field.set_y_expand(True)

    def _init_image(self):
        self.image = widgets.Image()
        self.layout.attach(self.image, 2, 1, 3, 4)
        self.image.set_x_expand(True)
        self.image.set_y_expand(True)

    def _init_buttons(self):
        self.buttons = []
        button_names = ['ćwicz', 'czytaj',
                        'literuj', 'następny', 'zamknij']
        for col, b in enumerate(button_names):
            button = widgets.ActionButton()
            button.set_label(b)
            button.set_icon_from_file('./icons/'+b+'.png')
            button.set_hilite_color(self.off_color)
            self.buttons.append(button)
            self.layout.attach(button, col, 5, 1, 1)

    def _init_params(self):
        self.result_font = 'Sans 40'
        self.word_font = 'Sans 70'
        self.off_color = Clutter.Color.new(200,200,180,255)

    def update_elements(self):
        self.update_result_field()
        self.update_word_field()
        self.update_image()

    def update_result_field(self):
        text = 'twój wynik: '+str(self.result)+' / '+str(self.points_limit)+' pkt'
        self.result_field.set_text(text)
        self.result_field.set_font(self.result_font)

    def update_word_field(self):
        self.word_field.set_text(self.word)
        self.word_field.set_font(self.word_font)

    def update_image(self):
        self.image.set_image_from_file('./words/pictures/' + self.word + '.jpg')

    def select_action(self,button):
        button_label = button.get_label()
        if button_label == 'zamknij':
            self.exit_app()
        elif button_label == 'ćwicz':
            return self.go_practice()
        elif button_label == 'czytaj':
            self.read_out_loud()
        elif button_label == 'literuj':
            self.spell()
        elif button_label == 'następny':
            self.change_word()

    def go_practice(self):
        self.container.word = self.word
        self.container.word_index = self.word_index
        new_panel_name = 'first_practice'
        return self.container.change_panel(new_panel_name)

    def read_out_loud(self):
        print('Reading: ' + self.word)

    def spell(self):
        print('Spelling: ' + self.word)

    def change_word(self):
        self.word_index = (self.word_index + 1) % len(self.words_list)
        self.word = self.words_list[self.word_index]
        self.update_word_field()
        self.update_image()

    def exit_app(self):
        self.container.exit_app()

    def create_cycle(self):
        return _MainPanelCycle(self)


class _MainPanelCycle(object):
    def __init__(self, panel):
        self.panel = panel
        self.interval = 1000
        self.index = None
        self.on_color = Clutter.Color.new(80,100,220,255)
        self.off_color = Clutter.Color.new(200,200,180,255)
        self.selection_color = Clutter.Color.new(250,12,250,255)

    def expose_next(self):
        if self.index != None:
            self.panel.buttons[self.index].set_hilite_color(self.off_color)
            self.index = (self.index + 1) % len(self.panel.buttons)
        else:
            self.index = 0
        self.panel.buttons[self.index].set_hilite_color(self.on_color)

    def stop(self):
        if self.index != None:
            self.panel.buttons[self.index].set_hilite_color(self.off_color)
            self.index = None

    def select(self):
        button = self.panel.buttons[self.index]
        button.set_hilite_color(self.selection_color)
        return self.panel.select_action(button)


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
        self._init_params()
        self._init_training_set()
        self._init_panel()

    def _init_params(self):
        self.panel_transition_time = 500
        self.word_index = 0
        self.info_font = 'Sans 50'
        self.result = 0
        self.points_limit = 2

    def _init_training_set(self):
        self.pictures_list = os.listdir('./words/pictures')
        self.words_list = [ i[ : i.index('.')] for i in self.pictures_list ]
        random.shuffle(self.words_list)
        self.word = self.words_list[self.word_index]

    def _init_panel(self):
        self.panel = MainPanel(self)
        self.add_actor(self.panel)
        self.panel.update_elements()

    def change_panel(self, new_panel_name):
        new_panel = self.choose_panel(new_panel_name)
        self.add_actor(new_panel)
        self.slide_in(new_panel)
        self.slide_out(self.panel)
        self.panel = new_panel
        return self.panel.create_cycle()

    def choose_panel(self, new_panel_name):
        if new_panel_name == 'first_practice':
            new_panel = FirstPracticePanel(self)
        elif new_panel_name == 'second_practice':
            new_panel = SecondPracticePanel(self)
        elif new_panel_name == 'main':
            new_panel = MainPanel(self)
        elif new_panel_name == 'result_info':
            if self.user_word == self.word:
                self.result = (self.result + 1) % self.points_limit
                if self.result == 0:
                    info = 'Brawo!\nZdobyłeś wszystkie punkty.\nKliknij żeby odebrać nagrodę.'
                else:
                    info = 'Gratulacje.\nWpisałeś poprawne słowo.\nZdobywasz punkt.'
            else:
                info = 'Niestety.\nSpróbuj jeszcze raz.'
            new_panel = ResultInfoPanel(self)
            new_panel.set_result_info(info)
            new_panel.set_font(self.info_font)
            if self.user_word == self.word:
                self.word_index = (self.word_index + 1) % len(self.words_list)
                self.word = self.words_list[self.word_index]
        elif new_panel_name == 'reward':
            new_panel = RewardPanel(self)
            new_panel.set_reward_info('Chcesz wyłączyć? (piosenkę / film)\nKliknij.')
            new_panel.set_font(self.info_font)
        return new_panel

    def slide_in(self,panel):
        panel.set_opacity(0)
        panel.animatev(Clutter.AnimationMode.LINEAR, self.panel_transition_time, ["opacity"], [255])

    def slide_out(self,panel):
        panel.animatev(Clutter.AnimationMode.LINEAR, self.panel_transition_time, ["opacity"], [0])

    def create_cycle(self):
        return self.panel.create_cycle()

    def exit_app(self):
        self.destroy()


class PisakEduStage(Clutter.Stage):
    def __init__(self, context):
        super(PisakEduStage, self).__init__()
        self.context = context
        color = Clutter.Color.new(100,170,190,255)
        self.set_background_color(color)
        self._init_elements()
        self.context.switcher.push_cycle(self.content.create_cycle())
        self.input = switcher_app.MouseSwitcherInput(self)
        self.context.switcher.add_input(self.input)

    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.content = PisakEduContainer()
        self.content.connect('destroy', lambda _:self.exit_app())
        self.add_actor(self.content)

    def exit_app(self):
        self.destroy()


class PisakEduApp(object):
    def __init__(self, argv):
        PisakEduApp.APP = self
        Clutter.init(argv)
        self._init_context()
        self._init_stage()

    def _init_context(self):
        self.context = switcher_app.Context(self)

    def _init_stage(self):
        self.stage = PisakEduStage(self.context)
        self.stage.connect("destroy", lambda _: Clutter.main_quit())
        self.stage.set_fullscreen(True)
        self.stage.show_all()

    def main(self):
        Clutter.main()


PisakEduApp(sys.argv).main()
