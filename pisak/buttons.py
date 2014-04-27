from gi.repository import Clutter, Mx, GObject, Cogl, Pango
from PIL import Image as PILImage
import os
from pisak import unit, res
from pisak.res import dims, colors

class MenuButton(Clutter.Actor):
    """
    No-framed menu button widget with label and icon.
    """
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
        self.label.set_background_color(colors.TRANSPARENT)
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
            self.background_color = colors.BLACK
            self.foreground_color = colors.WHITE
        elif self.hilite < 1.5:
            self.background_color = colors.HILITE_1
            self.foreground_color = colors.BLACK
        else:
            self.background_color = colors.WHITE
            self.foreground_color = colors.BLACK
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


class FramedButton(Clutter.Actor):
    """
    Base class for different types of framed button widgets.
    """
    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        super().__init__()
        self.connect("button-release-event", self.click_activate)
        self.connect("enter-event", lambda *_: self.hilite_on())
        self.connect("leave-event", lambda *_: self.hilite_off())
        self.set_reactive(True)
        self.selection_time = 1000

    def set_up_with_size(self, width, height):
        self.set_size(width, height)
        self._init_canvas()
        self._init_elements()

    def _init_elements(self):
        raise NotImplementedError()

    def _resize_canvas(self):
        self.canvas.set_size(self.get_width(), self.get_height())

    def _init_canvas(self):
        self.canvas = Clutter.Canvas()
        self.canvas.connect("draw", self.update_canvas)
        self.set_content(self.canvas)

    def get_color_vals(self, color):
        hexdec = color.to_string()
        r = int(hexdec[1:3], 16)
        g = int(hexdec[3:5], 16)
        b = int(hexdec[5:7], 16)
        a = int(hexdec[7:9], 16)
        return r, g, b, a

    def update_canvas(self, canvas, context, width, height):
        if self.frame_on:
            context.scale(width, height)
            line_width = 0.05
            y = line_width/2  # initial vertical offset
            x = y * height/width  # compensate for button being rectangle-shaped
            context.set_line_width(line_width)
            context.move_to(x, y)
            context.line_to(1-x, y)
            context.line_to(1-x, 1-y)
            context.line_to(x, 1-y)
            context.close_path()
            r, g, b, a = self.get_color_vals(self.background_color)
            context.set_source_rgba(r, g, b, a)
            context.fill_preserve()
            r, g, b, a = self.get_color_vals(colors.BLACK)
            context.set_source_rgba(r, g, b, a)
            context.stroke()
        else:
            context.scale(width, height)
            context.rectangle(0, 0, 1, 1)
            r, g, b, a = self.get_color_vals(self.background_color)
            context.set_source_rgba(r, g, b, a)
            context.fill()
        return True

    def hilite_off(self):
        self.frame_on = True
        self.set_hilite(0.0)
    
    def hilite_on(self):
        self.frame_on = False
        self.set_hilite(1.0)

    def select_on(self):
        self.frame_on = False
        self.set_hilite(1.5)

    def set_hilite(self, hilite):
        self.hilite = hilite
        if self.hilite < 0.5:
            self.background_color = colors.WHITE
            self.foreground_color = colors.BLACK
        elif self.hilite < 1.5:
            self.background_color = colors.BLACK
            self.foreground_color = colors.WHITE
        else:
            self.background_color = colors.HILITE_2
            self.foreground_color = colors.WHITE
        self.update_button()

    def update_button(self):
        raise NotImplementedError()

    def click_activate(self, source, event):
        self.select_on()
        Clutter.threads_add_timeout(0, self.selection_time, lambda _: self.hilite_off(), None)
        self.emit("activate")


class FramedButtonType1(FramedButton):
    """
    Framed button widget with nothing but a label.
    """
    
    def __init__(self):
        super().__init__()
        
    def _init_elements(self):
        self._init_layout()
        self._init_label()
        self.hilite_off()
        self._resize_canvas()
        
    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

    def _init_label(self):
        self.label = Clutter.Text()
        self.label.set_line_alignment(Pango.Alignment.CENTER)
        self.label.set_line_wrap(True)
        self.label.set_font_name('normal italic 16')
        self.label.set_background_color(colors.TRANSPARENT)
        self.add_child(self.label)

    def set_label(self, label):
        self.label.set_text(label)

    def update_button(self):
        self.canvas.invalidate()
        self.label.set_color(self.foreground_color)

    def set_model(self, model):
        self.set_label(model["label"])


class FramedButtonType2(FramedButton):
    """
    Framed button widget with nothing but an icon.
    """
    MODEL = {
        "icon_path": os.path.join(res.PATH, "icon.png")
    }
    
    def __init__(self):
        super().__init__()

    def _init_elements(self):
        self._init_layout()
        self._init_icon()
        self.hilite_off()
        self._resize_canvas()

    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

    def _init_icon(self):
        self.icon = Mx.Image()
        self.icon.set_scale_mode(Mx.ImageScaleMode.FIT)
        width, height = 0.9*self.get_width(), 0.9*self.get_height()
        self.icon.set_size(width, height)
        self.add_child(self.icon)

    def set_icon(self, icon_path):
        self.icon.set_from_file(icon_path)

    def update_button(self):
        icon_color = Clutter.ColorizeEffect.new(self.foreground_color)
        self.icon.clear_effects()
        self.icon.add_effect(icon_color)
        self.canvas.invalidate()

    def set_model(self, model):
        self.set_icon(self.MODEL["icon_path"])
        

class FramedButtonType3(FramedButton):
    """
    Framed button widget with label and icon.
    """
    MODEL = {
        "icon_path": os.path.join(res.PATH, "icon.png")
    }

    def __init__(self):
        super().__init__()

    def _init_elements(self):
        self._init_layout()
        self._init_label()
        self._init_icon()
        self.hilite_off()
        self._resize_canvas()

    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation.HORIZONTAL)
        spacing = 0.02 * self.get_width()
        self.layout.set_spacing(spacing)
        self.set_layout_manager(self.layout)

    def _init_label(self):
        self.label = Clutter.Text()
        self.label.set_line_alignment(Pango.Alignment.CENTER)
        self.label.set_line_wrap(True)
        self.label.set_font_name('normal italic 18')
        self.label.set_background_color(colors.TRANSPARENT)
        width = 0.65 * self.get_width()
        self.label.set_width(width)
        self.add_child(self.label)

    def _init_icon(self):
        self.icon = Mx.Image()
        self.icon.set_scale_mode(Mx.ImageScaleMode.FIT)
        width = 0.20 * self.get_width()
        self.icon.set_width(width)
        self.add_child(self.icon)
            
    def set_label(self, label):
        self.label.set_text(label)

    def set_icon(self, icon_path):
        self.icon.set_from_file(icon_path)

    def update_button(self):
        self.label.set_color(self.foreground_color)
        icon_color = Clutter.ColorizeEffect.new(self.foreground_color)
        self.icon.clear_effects()
        self.icon.add_effect(icon_color)
        self.canvas.invalidate()

    def set_model(self, model):
        self.set_label(model["label"])
        self.set_icon(self.MODEL["icon_path"])
        

class DefaultButton(Mx.Button):
    HEIGHT = unit.mm(16)
    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    
    def __init__(self):
        super().__init__()
        self.connect("clicked", self.click_activate)
        self.set_height(MenuButton.HEIGHT)
        self.set_x_expand(True)
        self.set_y_expand(False)
      
    def set_model(self, model):
        self.model = model
        self.set_label(self.model["label"])
     
    def click_activate(self):
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
