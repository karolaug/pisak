import sys
import os
from pisak import unit, buttons
from gi.repository import Clutter
import random
from concept.edu.panels import RewardPanel, ResultInfoPanel, PisakEduStage, PisakEduApp

class PracticePanel(Clutter.Actor):
    def __init__(self, container):
        super().__init__()
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
        self.set_reactive(True)
        self.connect('button_release_event', lambda x, y: self.on_click_event())
        self._init_params()
        self._init_elements()
        self._init_timer()

    def _init_params(self):
        self.previous_buttons = []
        self.font_name = 'Sans 60'
        self.time_interval = 700
        self.row_count = 5
        self.col_count = 8
        self.row = 0
        self.col = 0
        self.direction = 'rows'
        self.two_col_cycles = 0
        self.added_letters_indices = []
        self.gap_count = 2
        self.gap_indices = []
        while len(self.gap_indices) < self.gap_count:
            idx = random.randint(0, len(self.word) - 1)
            if idx not in self.gap_indices:
                self.gap_indices.append(idx)
        self.gap_indices.sort()
        self.on_color = Clutter.Color.new(80, 100, 220, 255)
        self.off_color = Clutter.Color.new(200, 200, 180, 255)
        self.selection_color = Clutter.Color.new(250, 12, 250, 255)
        self.background_color = Clutter.Color.new(100, 170, 190, 255)
        self.white_color = Clutter.Color.new(255, 255, 255, 255)

    def _init_elements(self):
        self._init_buttons()
        self._init_text_field()

    def _init_buttons(self):
        self._init_letter_buttons()
        self._init_action_buttons()

    def _init_letter_buttons(self):
        letters = ['a', 'i', 'e', 'r', 'c', 'p', 'l', 'ę', 'o', 'z', 'w',
                   'y', 'm', 'ł', 'h', 'ż', 'n', 's', 'k', 'u', 'b', 'ą',
                   'ś', 'f', 't', 'd', 'j', 'g', 'ó', 'ć', 'ń', 'ź']
        self.letter_buttons = [self.set_letter_button(i, letter)
                               for i, letter in enumerate(letters)]

    def _init_action_buttons(self):
        button_names = ['sprawdź', 'skasuj', 'czytaj',
                        'literuj', 'wyczyść', 'wróć']
        self.action_buttons = [self.set_action_button(index, action)
                               for index, action in enumerate(button_names)]

    def _init_text_field(self):
        self.text_field = buttons.TextField()
        self.text_field.set_font(self.font_name)
        self.layout.attach(self.text_field, 0, 0, self.col_count, 1)
        self.text_field.set_background_color(self.white_color)
        self.user_word = [letter if index not in self.gap_indices else '_'
                          for index, letter in enumerate(self.word)]
        self.text_field.set_text(''.join(self.user_word))

    def _init_timer(self):
        self.timer = Clutter.Timeline.new(self.time_interval)
        self.timer.set_repeat_count(-1)
        self.timer.connect('completed', lambda _: self.on_timer_event())
        self.start_timer_cycle()

    def set_letter_button(self, index, letter):
        button = buttons.LetterButton()
        button.set_letter_label(letter)
        button.set_font(self.font_name)
        button.set_hilite_color(self.off_color)
        self.layout.attach(button, index % self.col_count,
                           index / self.col_count + 1, 1, 1)
        return button

    def set_action_button(self, index, action):
        button = buttons.ActionButton()
        button.set_label(action)
        button.set_icon_from_file(''.join(['concept/edu/icons/', action, '.png']))
        button.set_hilite_color(self.off_color)
        where = {'sprawdź' : (button, index, self.row_count + 1, 2, 1),
                 'wróć' : (button, index + 1, self.row_count + 1, 2, 1)}
        try:
            self.layout.attach(*where[action])
        except KeyError:
            self.layout.attach(button, index + 1, self.row_count + 1, 1, 1)
        return button

    def start_timer_cycle(self):
        self.timer.start()

    def stop_timer_cycle(self):
        self.timer.stop()

    def on_timer_event(self):
        if self.previous_buttons:
            for b in self.previous_buttons: b.set_hilite_color(self.off_color)
        self.previous_buttons = []
        if self.direction == 'rows':
            if self.two_col_cycles == 2:
                self.row, self.col = 0, 0
                self.two_col_cycles = 0
            if self.row == self.row_count - 1:
                for button in self.action_buttons:
                    button.set_hilite_color(self.on_color)
                    self.previous_buttons.append(button)
            else:
                for b in range(self.row * self.col_count, self.row * self.col_count + self.col_count):
                    button = self.letter_buttons[b]
                    button.set_hilite_color(self.on_color)
                    self.previous_buttons.append(button)
            self.row = (self.row + 1) % self.row_count
        elif self.direction == 'cols':
            if self.row == self.row_count-1:
                button = self.action_buttons[self.col]
                if self.col == self.col_count - 3:
                    self.two_col_cycles += 1
                self.col = (self.col + 1) % (self.col_count - 2)
            else:
                button = self.letter_buttons[self.row * self.col_count + self.col]
                if self.col == self.col_count-1:
                    self.two_col_cycles += 1
                self.col = (self.col + 1) % self.col_count
            if self.two_col_cycles == 2:
                self.direction = 'rows'
            button.set_hilite_color(self.on_color)
            self.previous_buttons.append(button)
        self.set_reactive(True)

    def on_click_event(self):
        self.set_reactive(False)
        self.stop_timer_cycle()
        if self.previous_buttons:
            for b in self.previous_buttons: b.set_hilite_color(self.selection_color)
        if self.direction == 'rows':
            self.two_col_cycles = 0
            self.direction = 'cols'
            if self.row == 0:
                self.row = self.row_count - 1
            else:
                self.row -= 1
        elif self.direction == 'cols':
            if self.row == self.row_count - 1:
                if self.col == 0:
                    self.col = self.col_count-3
                else:
                    self.col -= 1
                button = self.action_buttons[self.col]
                self.choose_action(button)
            else:
                if self.col == 0 :
                    self.col = self.col_count-1
                else:
                    self.col -= 1
                idx = self.row * self.col_count + self.col
                button = self.letter_buttons[idx]
                if len(self.added_letters_indices) < self.gap_count:
                    self.add_letter(button)
            self.col, self.row = 0, 0
            self.direction = 'rows'
        self.start_timer_cycle()

    def choose_action(self, button):
        button_label = button.get_label()
        actions = {'sprawdź' : self.check_result,
                   'skasuj' : self.delete_letter,
                   'wyczyść' : self.clear_all,
                   'czytaj' : self.read_out_loud,
                   'literuj' : self.spell,
                   'wróć' : self.back_to_main}
        actions[button_label]()

    def add_letter(self, button):
        letter = button.get_letter_label()
        pos = self.gap_indices[ len(self.added_letters_indices)]
        self.text_field.delete_text(pos, pos + 1)
        self.text_field.insert_text(letter, pos)
        self.added_letters_indices.append(pos)

    def check_result(self):
        self.user_word = self.text_field.get_text()
        self.container.user_word = self.user_word
        self.container.change_panel()

    def delete_letter(self):
        if len(self.added_letters_indices) > 0:
            pos = self.added_letters_indices[-1]
            self.text_field.delete_text(pos , pos+1)
            self.text_field.insert_text('_', pos)
            self.added_letters_indices.remove(pos)

    def clear_all(self):
        if len(self.added_letters_indices) > 0:
            for pos in self.added_letters_indices:
                self.text_field.delete_text(pos, pos+1)
                self.text_field.insert_text('_', pos)
                self.added_letters_indices = self.added_letters_indices[:-1]

    def read_out_loud(self):
        print('Reading out loud:   '+self.word)

    def spell(self):
        print('Spelling:    '+self.word)

    def back_to_main(self):
        self.container.back_to_main = True
        self.container.change_panel()


class MainPanel(Clutter.Actor):
    def __init__(self, container):
        super(MainPanel, self).__init__()
        self.container = container
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.layout.set_column_spacing(10)
        self.layout.set_row_spacing(10)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.set_size(1400, 1300)
        self.set_reactive(True)
        self.connect('button_release_event', lambda x, y: self.on_click_event())
        self._init_params()
        self._init_elements()
        self._init_timer()

    def _init_elements(self):
        self._init_result_field()
        self._init_word_field()
        self._init_image()
        self._init_buttons()

    def _init_result_field(self):
        self.result_field = buttons.TextField()
        self.layout.attach(self.result_field, 0, 0, 5, 1)
        self.result_field.set_x_expand(True)

    def _init_word_field(self):
        self.word_field = buttons.TextField()
        self.layout.attach(self.word_field, 0, 1, 2, 4)
        self.word_field.set_x_expand(True)
        self.word_field.set_y_expand(True)

    def _init_image(self):
        self.image = buttons.Image()
        self.layout.attach(self.image, 2, 1, 3, 4)
        self.image.set_x_expand(True)
        self.image.set_y_expand(True)

    def _init_buttons(self):
        self.buttons = []
        button_names = ['ćwicz', 'czytaj',
                        'literuj', 'następny',
                        'zamknij']
        for col, b in enumerate(button_names):
            one_button = buttons.ActionButton()
            one_button.set_label(b)
            one_button.set_icon_from_file('concept/edu/icons/' + b + '.png')
            one_button.set_hilite_color(self.off_color)
            self.buttons.append(one_button)
            self.layout.attach(one_button, col, 5, 1, 1)
        self.idx_count = len(self.buttons)

    def update_elements(self, result, word):
        self.update_result_field(result)
        self.update_word_field(word)
        self.update_image(word)

    def update_result_field(self, result):
        text = 'twój wynik: ' + str(result) + ' / ' + str(self.container.points_limit) + ' pkt'
        self.result_field.set_text(text)
        self.result_field.set_font(self.result_font)

    def update_word_field(self, word):
        self.word_field.set_text(word)
        self.word_field.set_font(self.word_font)

    def update_image(self, word):
        self.image.set_image_from_file('concept/edu/words/pictures/' + word + '.jpg')

    def _init_params(self):
        self.result_font = 'Sans 40'
        self.word_font = 'Sans 70'
        self.time_interval = 800
        self.idx = 0
        self.on_color = Clutter.Color.new(80, 100, 220, 255)
        self.off_color = Clutter.Color.new(200, 200, 180, 255)
        self.selection_color = Clutter.Color.new(250, 12, 250, 255)
        self.scanning_on = False

    def _init_timer(self):
        self.timer = Clutter.Timeline.new(self.time_interval)
        self.timer.set_repeat_count(-1)
        self.timer.connect('completed', lambda _: self.on_timer_event())
        self.start_timer_cycle()

    def start_timer_cycle(self):
        self.timer.start()

    def stop_timer_cycle(self):
        self.timer.stop()

    def on_timer_event(self, *args):
        if hasattr(self, 'previous_button'):
            self.previous_button.set_hilite_color(self.off_color)
        button = self.buttons[self.idx]
        button.set_hilite_color(self.on_color)
        self.previous_button = button
        self.idx = (self.idx + 1) % self.idx_count
        self.scanning_on = True
        self.set_reactive(True)

    def on_click_event(self):
        self.set_reactive(False)
        if self.scanning_on:
            self.stop_timer_cycle()
            button = self.buttons[self.idx - 1]
            button.set_hilite_color(self.selection_color)
            self.idx = 0
            self.choose_action(button)
            if not hasattr(self, 'back_to_main'):
                self.start_timer_cycle()

    def choose_action(self, button):
        button_label = button.get_label()
        if button_label == 'zamknij':
            self.exit_app()
        elif button_label == 'ćwicz':
            self.go_practice()
        elif button_label == 'czytaj':
            self.read_out_loud()
        elif button_label == 'literuj':
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
        self.container.word_idx = (self.container.word_idx + 1) % self.container.word_count
        self.container.word = self.container.words_list[self.container.word_idx]
        self.update_word_field(word = self.container.word)
        self.update_image(word = self.container.word)

    def slide_in(self, widget):
        widget.set_opacity(0)
        widget.animatev(Clutter.AnimationMode.LINEAR, self.widget_transition_time, ["opacity"], [255])

    def slide_out(self, widget):
        widget.animatev(Clutter.AnimationMode.LINEAR, self.widget_transition_time, ["opacity"], [0])

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
        self.word_pictures_list = os.listdir('concept/edu/words/pictures')
        self.words_list = [ i[ : i.index('.')] for i in self.word_pictures_list ]
        random.shuffle(self.words_list)

    def _init_params(self):
        self.panel_transition_time = 1000
        self.word_idx = 0
        self.word_count = len(self.words_list)
        self.result = 0
        self.points_limit = 2

    def _init_panel(self):
        self.panel = MainPanel(self)
        self.current_panel_name = 'main'
        self.add_actor(self.panel)
        self.word = self.words_list[self.word_idx]
        self.panel.update_elements(result = self.result, word = self.word)

    def slide_in(self, panel):
        panel.set_opacity(0)
        panel.animatev(Clutter.AnimationMode.LINEAR, self.panel_transition_time, ["opacity"], [255])

    def slide_out(self, panel):
        panel.animatev(Clutter.AnimationMode.LINEAR, self.panel_transition_time, ["opacity"], [0])
        panel.set_reactive(False)

    def change_panel(self):
        new_panel = self.choose_panel()
        self.add_actor(new_panel)
        self.slide_in(new_panel)
        self.slide_out(self.panel)
        self.panel = new_panel

    def choose_panel(self):
        if self.current_panel_name == 'main':
            new_panel = PracticePanel(self)
            self.current_panel_name = 'practice'
        elif self.current_panel_name == 'practice':
            if hasattr(self, 'back_to_main'):
                delattr(self, 'back_to_main')
                new_panel = MainPanel(self)
                self.current_panel_name = 'main'
                new_word = self.words_list[self.word_idx]
                new_panel.update_elements(result = self.result , word = new_word)
            else:
                new_panel = ResultInfoPanel(self)
                self.current_panel_name = 'result_info'
                if self.user_word == self.word:
                    self.result += 1
                    self.word_idx = (self.word_idx + 1) % self.word_count
                    if self.result == self.points_limit:
                        info = 'Brawo!\nZdobyłeś wszystkie punkty.\nKliknij żeby odebrać nagrodę.'
                    elif self.result < self.points_limit:
                        info = 'Gratulacje.\nWpisałeś poprawne słowo.\nZdobywasz punkt.'
                else:
                    info = 'Niestety.\nSpróbuj jeszcze raz.'
                new_panel.set_info(info)
                new_panel.set_font('Sans 60')
        elif self.current_panel_name == 'result_info':
            if self.result == self.points_limit:
                new_panel = RewardPanel(self)
                self.current_panel_name = 'reward'
                new_panel.set_info('Chcesz wyłączyć? (piosenkę / film)\nKliknij.')
                new_panel.set_font('Sans 40')
                self.result = 0
            elif self.result < self.points_limit:
                new_panel = MainPanel(self)
                self.current_panel_name = 'main'
                self.word = self.words_list[self.word_idx]
                new_panel.update_elements(result = self.result, word = self.word)
        elif self.current_panel_name == 'reward':
            new_panel = MainPanel(self)
            self.current_panel_name = 'main'
            self.word = self.words_list[self.word_idx]
            new_panel.update_elements(result = self.result, word = self.word)
        return new_panel

    def exit_app(self):
        self.destroy()

PisakEduApp(PisakEduContainer, sys.argv).main()
