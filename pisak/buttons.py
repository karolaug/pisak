from gi.repository import Clutter, Mx, GObject
from pisak.res import dims

class MenuButton(Mx.Button):
    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    
    def __init__(self):
        super().__init__()
        self.connect("clicked", self.click_activate)
        self.set_width(dims.MENU_BUTTON_W_PX)
        self.set_height(dims.MENU_BUTTON_H_PX)
        #self.set_background_color(colors.BUTTON_BG)
        
    
    def set_model(self, model):
        self.model = model
        self.set_label(self.model["label"])
    
    def click_activate(self):
        self.emit("activated")


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
