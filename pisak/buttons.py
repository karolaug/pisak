from gi.repository import Clutter, Mx, GObject, Cogl
from PIL import Image as PILImage
import os
from pisak import unit, res
from pisak.res import dims

class MenuButton(Clutter.Actor):
    HEIGHT = unit.mm(15)
    WIDTH = unit.mm(65)
    MODEL = {
        "icon_path": os.path.join(res.PATH, "icon.png")
    }
    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    
    def __init__(self):
        super().__init__()
        self.connect("button-release-event", self.click_activate)
        self.connect("enter-event", lambda *_: self.hilite_on())
        self.connect("leave-event", lambda *_: self.hilite_off())
        self.set_reactive(True)
        self.set_size(dims.MENU_BUTTON_W_PX, dims.MENU_BUTTON_H_PX)
        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation.HORIZONTAL)
        self.layout.set_spacing(MenuButton.WIDTH/30.)
        self.set_layout_manager(self.layout)
        self._init_label()
        self._init_icon()
        self.hilite_off()
        self.selection_time = 1000
    
    def _init_label(self):
        self.label = Clutter.Text()
        self.label.set_width(MenuButton.WIDTH/1.5)
        self.label.set_line_wrap(True)
        self.label.set_font_name('monospace bold 20')
        self.label.set_background_color(res.colors.TRANSPARENT)
        self.add_child(self.label)

    def _init_icon(self):
        self.icon = Mx.Image()
        self.icon.set_size(MenuButton.WIDTH/4.2, MenuButton.HEIGHT/1.2)
        self.icon.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.add_child(self.icon)
            
    def set_label(self, label):
        self.label.set_text(label)

    def set_icon(self, icon_path):
        self.icon.set_from_file(icon_path)

    def hilite_off(self):
        self.set_hilite(0.0)
    
    def hilite_on(self):
        self.set_hilite(1.0)

    def select_on(self):
        self.set_hilite(1.5)

    def set_hilite(self, hilite):
        self.hilite = hilite
        if self.hilite < 0.5:
            self.background_color = res.colors.BLACK
            self.foreground_color = res.colors.WHITE
        elif self.hilite < 1.5:
            self.background_color = res.colors.HILITE_1
            self.foreground_color = res.colors.BLACK
        else:
            self.background_color = res.colors.WHITE
            self.foreground_color = res.colors.BLACK
        self.update_button()

    def update_button(self):
        self.set_background_color(self.background_color)
        self.label.set_color(self.foreground_color)
        icon_color = Clutter.ColorizeEffect.new(self.foreground_color)
        self.icon.clear_effects()
        self.icon.add_effect(icon_color)

    def set_model(self, model):
        self.set_label(model["label"])
        self.set_icon(self.MODEL["icon_path"])
    
    def click_activate(self, source, event):
        self.select_on()
        Clutter.threads_add_timeout(0, self.selection_time, lambda _: self.hilite_off(), None)
        self.emit("activate")


class LetterButton(Clutter.Actor):
    def __init__(self):
        super(LetterButton,self).__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self._init_letter_label()

    def _init_letter_label(self):
        self.letter_label=Clutter.Text() #/Mx.Label
        self.add_actor(self.letter_label)
        
    def set_letter_label(self,letter):
        self.letter_label.set_text(letter)

    def set_font(self,font_name):
        self.letter_label.set_font_name(font_name)

    def get_letter_label(self):
        return self.letter_label.get_text()

    def set_hilite_color(self,color):
        self.set_background_color(color)
        

class ActionButton(Clutter.Actor):
    def __init__(self):
        super(ActionButton,self).__init__()
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

    def get_label(self):
        return self.label.get_text()

    def set_icon_from_file(self,path):
        self.icon.set_from_file(path)

    def set_hilite_color(self,color):
        self.set_background_color(color)

class TextField(Clutter.Actor):
    def __init__(self):
        super(TextField, self).__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self._init_text_field()

    def _init_text_field(self):
        self.text_field=Clutter.Text()
        self.add_actor(self.text_field)

    def set_text(self,text):
        self.text_field.set_text(text)

    def insert_text(self,text,position):
        self.text_field.insert_text(text,position)

    def delete_text(self,start_pos,end_pos):
        self.text_field.delete_text(start_pos,end_pos)

    def set_font(self,font_name):
        self.text_field.set_font_name(font_name)

    def get_text(self):
        return self.text_field.get_text()

    
class Image(Clutter.Actor):
    def __init__(self):
        super(Image, self).__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self._init_image()

    def _init_image(self):
        self.image=Mx.Image()
        self.image.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.add_actor(self.image)

    def set_image_from_file(self,path):
        self.image.set_from_file(path)
