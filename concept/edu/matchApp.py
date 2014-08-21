import sys
import os
from pisak import unit, buttons
from gi.repository import Clutter
import random
from concept.edu.panels import RewardPanel, ResultInfoPanel, PisakEduStage, PisakEduApp

class PracticePanel(Clutter.Actor):
    def __init__(self,container):
        super(PracticePanel, self).__init__()
        self.container = container
        self.word = container.word
        self.words_list = container.words_list
        self.word_idx = container.word_idx
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

    def _init_params(self):
        self.result_font = 'Sans 40'
        self.word_font = 'Sans 70'
        self.time_interval = 800
        self.word_count = 3
        self.idx = 0
        self.on_color = Clutter.Color.new(80, 100, 220, 255)
        self.off_color = Clutter.Color.new(200, 200, 180, 255)
        self.selection_color = Clutter.Color.new(250, 12, 250, 255)
        self.scanning_on = False

    def _init_elements(self):
        self._init_result_field()
        self._init_image()
        self._init_buttons()

    def _init_buttons(self):
        self._init_word_buttons()
        self._init_action_buttons()

    def _init_result_field(self):
        self.result_field = buttons.TextField()
        self.layout.attach(self.result_field, 0, 0, 4 ,1)
        self.result_field.set_x_expand(True)

    def _init_word_buttons(self):
        words = []
        while len(words) < self.word_count - 1:
            idx = random.randint(0, len(self.container.words_list) - 1)
            word = self.container.words_list[idx]
            if word not in words and word != self.container.word:
                words.append(word)
        words.insert(random.randint(0, self.word_count - 2), self.container.word)
        self.word_buttons = []
        for i, b in enumerate(words):
            one_button = buttons.TextField()
            one_button.set_text(b)
            one_button.set_background_color(self.off_color)
            one_button.set_font(self.word_font)
            self.word_buttons.append(one_button)
            self.layout.attach(one_button, 0, i + 1, 2, 1)
            one_button.set_x_expand(True)
            one_button.set_y_expand(True)

    def _init_image(self):
        self.image = buttons.Image()
        self.image.set_image_from_file('concept/edu/words/pictures/' + self.word + '.jpg')
        self.layout.attach(self.image, 2, 1, 2, self.word_count)
        self.image.set_x_expand(True)
        self.image.set_y_expand(True)

    def _init_action_buttons(self):
        self.action_buttons = []
        action_button_names = ['czytaj',
                               'literuj','następny','zamknij']
        for col, b in enumerate(action_button_names):
            one_button = buttons.ActionButton()
            one_button.set_label(b)
            one_button.set_icon_from_file('concept/edu/icons/'+b+'.png')
            one_button.set_hilite_color(self.off_color)
            self.action_buttons.append(one_button)
            self.layout.attach(one_button, col, self.word_count + 1, 1, 1)
        self.action_buttons_count = len(self.action_buttons)

    def update_elements(self,current_word_buttons = None):
        self.update_result_field()
        self.update_image()
        self.update_word_buttons(current_word_buttons)

    def update_result_field(self):
        text = 'twój wynik: ' + str(self.container.result) + ' / ' + str(self.container.points_limit) + ' pkt'
        self.result_field.set_text(text)
        self.result_field.set_font(self.result_font)

    def update_word_buttons(self,current_word_buttons=None):
        if not current_word_buttons:
            words = []
            while len(words) < self.word_count - 1:
                idx = random.randint(0, len(self.container.words_list) - 1)
                word = self.container.words_list[idx]
                if word not in words and word != self.container.word:
                    words.append(word)
            words.insert(random.randint(0, self.word_count - 2),self.container.word)
            for i, b in enumerate(self.word_buttons):
                b.set_text(words[i])
        else:
            for i in range(self.word_count):
                self.word_buttons[i].set_text(current_word_buttons[i].get_text())

    def update_image(self):
        self.image.set_image_from_file('concept/edu/words/pictures/' + self.word + '.jpg')

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
            try:
                self.previous_button.set_hilite_color(self.off_color)
            except AttributeError:
                self.previous_button.set_background_color(self.off_color)
        if self.idx >= self.word_count:
            button = self.action_buttons[self.idx - self.word_count]
        else:
            button = self.word_buttons[self.idx]
        try:
            button.set_hilite_color(self.on_color)
        except AttributeError:
            button.set_background_color(self.on_color)
        self.previous_button = button
        self.idx = (self.idx + 1) % (self.word_count + self.action_buttons_count)
        self.scanning_on = True
        self.set_reactive(True)

    def on_click_event(self):
        self.set_reactive(False)
        if self.scanning_on:
            self.stop_timer_cycle()
            if self.idx > self.word_count:
                button = self.action_buttons[self.idx - self.word_count - 1]
            elif self.idx == self.word_count:
                button = self.word_buttons[-1]
            elif self.idx == 0:
                button = self.action_buttons[-1]
            else:
                button = self.word_buttons[self.idx-1]
            self.idx = 0
            self.choose_action(button)
            self.start_timer_cycle()

    def choose_action(self,button):
        if button in self.word_buttons:
            word = button.get_text()
            self.container.word = self.word
            self.container.user_word = word
            self.container.current_word_buttons = self.word_buttons
            self.container.change_panel()
        else:
            try:
                button.set_hilite_color(self.selection_color)
            except AttributeError:
                button.set_background_color(self.selection_color)
            button_label = button.get_label()
            if button_label == 'zamknij':
                self.exit_app()
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

    def spell(self):
        print('Spelling: ' + self.container.word)

    def change_word(self):
        self.word_idx = (self.word_idx + 1) % self.word_count
        self.word = self.words_list[self.word_idx]
        self.update_word_buttons(None)
        self.update_image()

    def slide_in(self,widget):
        widget.set_opacity(0)
        widget.animatev(Clutter.AnimationMode.LINEAR, self.widget_transition_time, ["opacity"], [255])

    def slide_out(self,widget):
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
        self.words_list = [i[:i.index('.')] for i in self.word_pictures_list]
        random.shuffle(self.words_list)

    def _init_params(self):
        self.panel_transition_time = 1000
        self.word_idx = 0
        self.word_count = len(self.words_list)
        self.result = 0
        self.points_limit = 2

    def _init_panel(self):
        self.word = self.words_list[self.word_idx]
        self.panel = PracticePanel(self)
        self.current_panel_name = 'practice'
        self.add_actor(self.panel)
        self.panel.update_elements()

    def slide_in(self,panel):
        panel.set_opacity(0)
        panel.animatev(Clutter.AnimationMode.LINEAR, self.panel_transition_time, ["opacity"], [255])

    def slide_out(self,panel):
        panel.animatev(Clutter.AnimationMode.LINEAR, self.panel_transition_time, ["opacity"], [0])
        panel.set_reactive(False)

    def change_panel(self):
        new_panel = self.choose_panel()
        self.add_actor(new_panel)
        self.slide_in(new_panel)
        self.slide_out(self.panel)
        self.panel = new_panel

    def choose_panel(self):
        if self.current_panel_name == 'practice':
            new_panel = ResultInfoPanel(self)
            self.current_panel_name = 'result_info'
            if self.user_word == self.word:
                self.result += 1
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
            elif self.result < self.points_limit:
                self.current_panel_name = 'practice'
                if self.user_word != self.word:
                    new_panel = PracticePanel(self)
                    new_panel.update_elements(self.current_word_buttons)
                else:
                    self.word_idx = (self.word_idx + 1) % self.word_count
                    self.word = self.words_list[self.word_idx]
                    new_panel = PracticePanel(self)
                    new_panel.update_elements()
        elif self.current_panel_name == 'reward':
            self.result = 0
            self.word_idx = (self.word_idx + 1)%self.word_count
            self.word = self.words_list[self.word_idx]
            new_panel = PracticePanel(self)
            self.current_panel_name = 'practice'
            new_panel.update_elements()
        return new_panel

    def exit_app(self):
        self.destroy()

PisakEduApp(PisakEduContainer, sys.argv).main()
