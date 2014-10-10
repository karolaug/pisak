import collections
import os.path

from gi.repository import Clutter, Mx, GObject, Rsvg, Cogl, GdkPixbuf
import cairo

from pisak import switcher_app, unit, res, properties, scanning
from pisak.layout import Box, Bin
from pisak.res import colors


class HiliteTool(Clutter.Actor):
    """
    Classes implementing HiliteTool interface can be used to add highlight to
    widgets which need to implement Scannable interface, but are not
    Stylable. Scannable widget should add HiliteTool instance as a descendant
    and call its methods to change highlight state.

    :see: :class:`pisak.widgets.Aperture`
    """
    def turn_on(self):
        """
        Enable highlight.
        """
        raise NotImplementedError()

    def turn_off(self):
        """
        Disable highlight.
        """
        raise NotImplementedError()


class Aperture(HiliteTool, properties.PropertyAdapter):
    """
    This actor draws a semi transparent cover with rectangular aperture in
    the center. It can be used to highlight another widget.
    """
    __gtype_name__ = "PisakAperture"
    __gproperties__ = {
        'cover': (GObject.TYPE_FLOAT, None, None,
                  0, 1, 0, GObject.PARAM_READWRITE)
    }

    COVER_OFF = 0.0

    COVER_ON = 0.4

    def __init__(self):
        super().__init__()
        self.set_x_expand(True)
        self.set_y_expand(True)
        self.color = colors.CYAN
        self._init_content()
        self.connect("notify::cover", lambda *_: self.canvas.invalidate())
        self.cover_transition = Clutter.PropertyTransition.new("cover")
        self.set_property("cover", 0)

    @property
    def cover(self):
        """
        Specifies what portion of the actor should be covered. The value
        should range from 0 to 1. Covered area doesn't change linearly.
        """
        return self._cover

    @cover.setter
    def cover(self, value):
        self._cover = value

    def set_cover(self, value):
        self.remove_transition("cover")
        self.cover_transition.set_from(self.get_property("cover"))
        self.cover_transition.set_to(value)
        self.cover_transition.set_duration(166)
        self.add_transition("cover", self.cover_transition)

    def _draw(self, canvas, context, w, h):
        context.set_operator(cairo.OPERATOR_CLEAR)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)
        context.rectangle(0, 0, w, h)
        context.set_source_rgba(0, 0.894, 0.765, 0.66)
        context.fill()
        context.set_operator(cairo.OPERATOR_CLEAR)
        a = 1 - self.get_property("cover")
        x, y = (0.5 - a / 2) * w, (0.5 - a / 2) * h
        rw, rh = a * w, a * h
        context.rectangle(x, y, rw, rh)
        context.fill()
        return True

    def _init_content(self):
        self.canvas = Clutter.Canvas()
        self.canvas.set_size(140, 140)
        self.canvas.connect("draw", self._draw)
        self.set_content(self.canvas)

    def turn_on(self):
        self.set_cover(self.COVER_ON)

    def turn_off(self):
        self.set_cover(self.COVER_OFF)


class PhotoTile(Bin, properties.PropertyAdapter, scanning.Scannable):
    """
    Tile containing image and label that can be styled by CSS.
    This widget display a preview of a photo along with label. It can be
    used to display a grid of photo tiles.

    The style of PhotoTile elements be adjusted in CSS. The label is a
    "MxButton" element with "PisakPhotoTileLabel" class. The photo is
    "MxImage" element with no class set.
    """
    __gtype_name__ = "PisakPhotoTile"

    GTYPE_NAME = __gtype_name__
    """GType name"""

    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    __gproperties__ = {
        "preview_path": (
            GObject.TYPE_STRING,
            "path to preview photo",
            "path to preview photo displayed on a tile",
            "noop",
            GObject.PARAM_READWRITE),
        "preview_ratio_width": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "preview_ratio_height": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "scale_mode": (
            Mx.ImageScaleMode.__gtype__,
            "image scale mode", "scale mode", "crop",
            GObject.PARAM_READWRITE),
        "label_text": (
            GObject.TYPE_STRING,
            "label under the tile",
            "tile label text",
            "noop",
            GObject.PARAM_READWRITE),
        "hilite_tool": (
            HiliteTool.__gtype__,
            "actor to hilite", "hiliting tool",
            GObject.PARAM_READWRITE),
        "ratio_spacing": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self._init_box()
        self._init_elements()
        self.preview_loading_width = 300
        self.preview_loading_height = 300
        self.hilite_tool = None
        self.scale_mode = Mx.ImageScaleMode.CROP

    @property
    def label_text(self):
        """
        Text on the photo label
        """
        return self.label.get_text()

    @label_text.setter
    def label_text(self, value):
        self.label.set_text(value)

    @property
    def preview_path(self):
        """
        Path to the preview photo
        """
        return self._preview_path

    @preview_path.setter
    def preview_path(self, value):
        self._preview_path = value
        width, height = self.preview.get_size()
        if width <= 1 or height <= 1:  # 1 x 1 as unrenderable picture size
            width, height = self.get_size()
        if width <= 1 or height <= 1:
            width = self.preview_loading_width
            height = self.preview_loading_height
        self.preview.set_from_file_at_size(value, width, height)
        
    @property
    def preview_ratio_width(self):
        """
        Screen-relative width
        """
        return self._preview_ratio_width

    @preview_ratio_width.setter
    def preview_ratio_width(self, value):
        self._preview_ratio_width = value
        self.preview.set_width(unit.w(value))

    @property
    def preview_ratio_height(self):
        """
        Screen-relative height
        """
        return self._preview_ratio_height

    @preview_ratio_height.setter
    def preview_ratio_height(self, value):
        self._preview_ratio_height = value
        self.preview.set_height(unit.h(value))

    @property
    def ratio_spacing(self):
        """
        Screen-relative spacing between photo and label
        """
        return self.box.ratio_spacing

    @ratio_spacing.setter
    def ratio_spacing(self, value):
        self.box.ratio_spacing = value

    @property
    def scale_mode(self):
        """
        Preview photo scale mode
        
        :see: :class:`gi.repository.Mx.Image`
        """
        return self.preview.get_scale_mode()

    @scale_mode.setter
    def scale_mode(self, value):
        self.preview.set_scale_mode(value)

    @property
    def hilite_tool(self):
        """
        Highlighting object.
        """
        return self._hilite_tool

    @hilite_tool.setter
    def hilite_tool(self, value):
        self._hilite_tool = value
        if value is not None:
            self.add_child(value)

    def _init_box(self):
        self.box = Box()
        self.box.orientation = Clutter.Orientation.VERTICAL
        self.add_child(self.box)

    def _init_elements(self):
        self.preview = Mx.Image()
        self.preview.set_allow_upscale(True)
        self.box.add_child(self.preview)
        self.label = Mx.Label()
        self.label.set_style_class("PisakPhotoTileLabel")
        self.box.add_child(self.label)

    def activate(self):
        self.emit("activate")

    def enable_hilite(self):
        if self.hilite_tool is not None:
            self.hilite_tool.turn_on()

    def disable_hilite(self):
        if self.hilite_tool is not None:
            self.hilite_tool.turn_off()

    def enable_scanned(self):
        # TODO: add scanned highlight
        pass

    def disable_scanned(self):
        # TODO: add scanned highlight
        pass

    def is_disabled(self):
        return False


class Slider(Mx.Slider, properties.PropertyAdapter):
    """
    Widget indicating a range of content being displayed, consists of bar with
    handle moving back and forth on top of it.
    """
    __gtype_name__ = "PisakSlider"
    __gproperties__ = {
        "value-transition-duration": (
            GObject.TYPE_INT64, "transition duration",
            "duration of value transition in msc", 0,
            GObject.G_MAXUINT, 1000, GObject.PARAM_READWRITE),
        "followed-object": (
            Clutter.Actor.__gtype__,
            "", "", GObject.PARAM_READWRITE)
    }
    def __init__(self):
        self.value_transition = Clutter.PropertyTransition.new("value")
        self.value_transition_duration = 1000
        self.followed_object = None

    @property
    def followed_object(self):
        return self._followed_object

    @followed_object.setter
    def followed_object(self, value):
        self._followed_object = value
        if value is not None:
            value.connect("progressed", self._set_value)

    @property
    def value_transition_duration(self):
        return self.value_transition.get_duration()

    @value_transition_duration.setter
    def value_transition_duration(self, value):
        self.value_transition.set_duration(value)

    def _set_value(self, source, value, custom_step):
        self.value_transition.set_from(self.get_value())
        self.value_transition.set_to(value)
        self.remove_transition("value")
        self.add_transition("value", self.value_transition)


class ProgressBar(Bin, properties.PropertyAdapter):
    """
    Custom-drawn progress indicator. Progress bar can observe one object for
    progress. Observed object emits two types of signal: "limit-declared" and
    "progressed". The former signal is emitted to set maximal progress value,
    the latter one is emitted to set current progress.
    
    This widget is composed from MxProgressBar an MxLabel and can be styled
    in CSS.
    """
    __gtype_name__ = "PisakProgressBar"
    __gproperties__ = {
        "label": (
            Mx.Label.__gtype__,
            "", "", GObject.PARAM_READWRITE),
        "progress": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "progress_transition_duration": (
            GObject.TYPE_INT64, "transition duration",
            "duration of progress transition in msc", 0,
            GObject.G_MAXUINT, 1000, GObject.PARAM_READWRITE),
        "label_ratio_x_offset": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "counter_limit": (
            GObject.TYPE_INT64, "counter limit",
            "max counter value", 0, GObject.G_MAXUINT,
            10, GObject.PARAM_READWRITE),
        "followed-object": (
            Clutter.Actor.__gtype__,
            "", "", GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self._init_bar()
        self.label = None
        self.step = None
        self.label_ratio_x_offset = None
        self.counter_limit = None
        self.progress_transition = Clutter.PropertyTransition.new("progress")
        self.progress_transition_duration = 1000
        self.progress_transition.connect("stopped", self._update_label)
        self.connect("notify::width", self._allocate_label)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        if value is not None:
            value.set_y_expand(True)
            value.set_y_align(Clutter.ActorAlign.CENTER)
            self.insert_child_above(value, None)

    @property
    def followed_object(self):
        """
        Object observed by the progressbar.
        """
        return self._related_object

    @followed_object.setter
    def followed_object(self, value):
        self._followed_object = value
        value.connect("limit-declared", self._set_counter_limit)
        value.connect("progressed", self._set_progress)

    @property
    def counter_limit(self):
        """
        Maximal progress value.
        """
        return self._counter_limit

    @counter_limit.setter
    def counter_limit(self, value):
        self._counter_limit = value
        if value is not None:
            self.step = int(self.progress*value)
        self._update_label()

    @property
    def progress(self):
        """
        Progressbar value.
        """
        return self.bar.get_progress()

    @progress.setter
    def progress(self, value):
        self.progress_transition.set_from(self.progress)
        self.progress_transition.set_to(value)
        self.bar.remove_transition("progress")
        self.bar.add_transition("progress", self.progress_transition)
        if self.counter_limit is not None:
            self.step = int(value*self.counter_limit)

    @property
    def progress_transition_duration(self):
        """
        Duration of animation in milliseconds.
        """
        return self.progress_transition.get_duration()

    @progress_transition_duration.setter
    def progress_transition_duration(self, value):
        self.progress_transition.set_duration(value)

    @property
    def label_ratio_x_offset(self):
        """
        Horizontal offset of label relative to progressbar width 
        """
        return self._label_ratio_x_offset

    @label_ratio_x_offset.setter
    def label_ratio_x_offset(self, value):
        self._label_ratio_x_offset = value
        self._allocate_label()

    def _init_bar(self):
        self.bar = Mx.ProgressBar()
        self.bar.set_x_expand(True)
        self.bar.set_y_expand(True)
        self.insert_child_below(self.bar, None)

    def _allocate_label(self, *args):
        if self.label is not None:
            if self.get_width() and self.label_ratio_x_offset is not None:
                px_x_offset = self.label_ratio_x_offset * self.get_width()
                self.label.set_x(px_x_offset)

    def _set_counter_limit(self, source, limit):
        self.counter_limit = limit

    def _set_progress(self, source, progress, custom_step):
        self.progress = progress
        self.step = custom_step

    def _update_label(self, *args):
        if self.label is not None:
            new_text = " / ".join([str(self.step),
                                str(self.counter_limit)])
            self.label.set_text(new_text)


class Header(Mx.Image, properties.PropertyAdapter):
    __gtype_name__ = "PisakMenuHeader"
    __gproperties__ = {
        "name": (
            GObject.TYPE_STRING, None, None, "funkcjenapis",
            GObject.PARAM_READWRITE),
        "ratio_width": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_height": (
            GObject.TYPE_FLOAT, None, None, 0,
            1., 0, GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.handle = Rsvg.Handle()

    @property
    def ratio_width(self):
        return self._ratio_width

    @ratio_width.setter
    def ratio_width(self, value):
        self._ratio_width = value
        self.set_width(unit.w(value))

    @property
    def ratio_height(self):
        return self._ratio_height

    @ratio_height.setter
    def ratio_height(self, value):
        self._ratio_height = value
        self.set_height(unit.h(value))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        svg_path = os.path.join(res.PATH, 'icons',
                                ''.join([self.name, ".svg"]))
        self.svg = self.handle.new_from_file(svg_path)
        pixbuf = self.svg.get_pixbuf()
        self.set_from_data(pixbuf.get_pixels(),
                           Cogl.PixelFormat.RGBA_8888,
                           pixbuf.get_width(),
                           pixbuf.get_height(),
                           pixbuf.get_rowstride())


class Button(Mx.Button, properties.PropertyAdapter, scanning.StylableScannable):
    """
    Generic Pisak button widget with label and icon.
    """
    __gtype_name__ = "PisakButton"
    
    # removing these signals due to functionality duplication
    #__gsignals__ = {
    #    "activate": (GObject.SIGNAL_RUN_FIRST, None, ()),
    #    "inactivate": (GObject.SIGNAL_RUN_FIRST, None, ())
    #}
    
    __gproperties__ = {
        #"disabled": (GObject.TYPE_BOOLEAN, "State of button",
        #             "If state of button is disabled.", False, 
        #             GObject.PARAM_READWRITE),
        "ratio_width": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_height": (
            GObject.TYPE_FLOAT, None, None, 0,
            1., 0, GObject.PARAM_READWRITE),
        "text": (
            GObject.TYPE_STRING, "label default text",
            "text displayed on the button", "noop",
            GObject.PARAM_READWRITE),
        "alternative_text": (
            GObject.TYPE_STRING,
            "alternative label text",
            "alternative text displayed on the button",
            "?", GObject.PARAM_READWRITE),
        "icon_name": (
            GObject.TYPE_STRING, "blank",
            "name of the icon displayed on the button",
            "blank", GObject.PARAM_READWRITE),
        "alternative_icon_name": (
            GObject.TYPE_STRING, "blank",
            "name of the aternative icon displayed on the button",
            "blank", GObject.PARAM_READWRITE),
        "spacing": (
            GObject.TYPE_INT64, "space between icon and text",
            "space between icon and text", 0, 1000, 100,
            GObject.PARAM_READWRITE),
        "on_select_hilite_duration": (
            GObject.TYPE_UINT, "hilite duration",
            "duration of hilite in msc",
            0, GObject.G_MAXUINT, 1000,
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.properties = {}
        self.on_select_hilite_duration = None
        self.current_icon = None
        self.box = None
        self.disabled = False
        self._connect_signals()

    def _connect_signals(self):
        self.connect("notify::text", self._set_initial_label)
        self.connect("clicked", self.on_click_activate)
        #self.connect("enter-event", lambda *_: self.hilite_on())
        #self.connect("leave-event", lambda *_: self.hilite_off())
        #self.connect("inactivate", lambda *_: self.inactivate())
        self.connect("notify::style-pseudo-class", self._change_icon_style)
        self.connect("notify::mapped", self.set_space)
        self.set_reactive(True)

    @property
    def ratio_width(self):
        return self._ratio_width

    @ratio_width.setter
    def ratio_width(self, value):
        self._ratio_width = value
        self.set_width(unit.w(value))

    @property
    def ratio_height(self):
        return self._ratio_height

    @ratio_height.setter
    def ratio_height(self, value):
        self._ratio_height = value
        self.set_height(unit.h(value))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)

    @property
    def alternative_text(self):
        return self._alternative_text

    @alternative_text.setter
    def alternative_text(self, value):
        self._alternative_text = str(value)

    @property
    def icon_name(self):
        return self._icon_name

    @icon_name.setter
    def icon_name(self, value):
        self._icon_name = value
        #if not Mx.IconTheme.get_default().has_icon(value):
        self.set_icon()

    @property
    def alternative_icon_name(self):
        return self._alternative_icon_name

    @alternative_icon_name.setter
    def alternative_icon_name(self, value):
        self._alternative_icon_name = value

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self._spacing = value
        #self.box.set_spacing(value)

    @property
    def on_select_hilite_duration(self):
        return self._on_select_hilite_duration

    @on_select_hilite_duration.setter
    def on_select_hilite_duration(self, value):
        self._on_select_hilite_duration = value

    def _set_initial_label(self, source, spec):
        self.set_default_label()
        self.disconnect_by_func(self._set_initial_label)

    def set_default_label(self):
        self.set_label(self.text)

    def set_space(self, *args):
        try:
            img_width = self.image.get_width()
            text_width = self.get_children()[0].get_children()[1].get_width()
            butt_width = self.get_width()
            self.space.set_width(butt_width - img_width - text_width - 26)
        except AttributeError:
            pass  # should write a new PisakButtonMenu

    def set_alternative_label(self):
        self.set_label(self.alternative_text)

    def switch_label(self):
        current_label = self.get_label()
        if current_label in (self.alternative_text, None):
            self.set_default_label()
        elif current_label == self.text:
            self.set_alternative_label()

    def switch_icon(self):
        raise NotImplementedError

    def _change_icon_style(self, *args):
        self.change_icon_white()

    def set_icon(self):
        if not self.box:
            self.custom_content()
        if self.icon_name:
            self.load_image()
            self.box.show()
        else:
            self.box.hide()

    def custom_content(self):
        self.set_icon_visible(False)
        self.box = Box()
        original_box = self.get_children()[0]
        self.clutter_text = original_box.get_children()[1]
        self.clutter_text.set_property("ellipsize", 0)
        text_content = self.clutter_text.get_text()
        if text_content.strip() == '':
            original_box.set_layout_manager(Clutter.BinLayout())
            original_box.add_actor(self.box, 1)
        else:
            original_box.add_actor(self.box, 1)
            self.space = Clutter.Actor()
            self.box.add_child(self.space)
        self.image = Mx.Image()
        self.box.add_child(self.image)

    def load_image(self):
        self.read_svg()
        self.image_path = os.path.join(res.PATH, "icons", self.icon_name)
        icon_size = self.get_icon_size()
        if self.svg:
            pixbuf = self.svg.get_pixbuf()
            if icon_size:
                pixbuf = pixbuf.scale_simple(icon_size, icon_size, 3)
            self.image.set_from_data(pixbuf.get_pixels(),
                                     Cogl.PixelFormat.RGBA_8888,
                                     pixbuf.get_width(),
                                     pixbuf.get_height(),
                                     pixbuf.get_rowstride())
            try:
                if self.get_property("disabled"):
                    self.image.set_opacity(100)
            except AttributeError:  # if the disabled props is not yet set
                pass
        else:
            try:
                self.image.set_from_file(''.join([self.image_path, '.png']))
            except:  # GError as error:
                print("No PNG, trying JPG")
                try:
                    self.image.set_from_file(''.join([self.image_path,
                                                      '.jpg']))
                except:  # GError as error:
                    text = "No PNG, SVG or JPG icon found of name {}."
                    print(text.format(self.icon_name))
            self.image.set_scale_mode(1)  # 1 is FIT, 0 is None, 2 is CROP
            if icon_size:
                image_size = self.image.get_size()
                print(image_size, icon_size)
                self.image.set_scale(icon_size * 10 / image_size[1],
                                     icon_size * 10 / image_size[0])

    def read_svg(self):
        try:
            handle = Rsvg.Handle()
            svg_path = ''.join([os.path.join(res.PATH, 'icons',
                                             self.icon_name), '.svg'])
            self.svg = handle.new_from_file(svg_path)
        except:  # GError as error:
            print('No file found at {}.'.format(svg_path))
            self.svg = False

    def set_image_white(self):
        handle = Rsvg.Handle()
        svg_path = ''.join([os.path.join(res.PATH, 'icons',
                                         self.icon_name), '_white', '.svg'])
        self.svg_white = handle.new_from_file(svg_path)
        icon_size = self.get_icon_size()
        pixbuf = self.svg_white.get_pixbuf()
        if icon_size:
            pixbuf = pixbuf.scale_simple(icon_size, icon_size, 3)
        self.image.set_from_data(pixbuf.get_pixels(),
                                 Cogl.PixelFormat.RGBA_8888,
                                 pixbuf.get_width(),
                                 pixbuf.get_height(),
                                 pixbuf.get_rowstride())

    def change_icon_white(self):
        try:
            if self.icon_name:
                if self.style_pseudo_class_contains("scanning") or self.style_pseudo_class_contains("hover"):
                    if self.disabled and self.style_pseudo_class_contains("hover") and self.style_pseudo_class_contains("scanning"):
                        self.set_image_white()
                    elif self.disabled and not self.style_pseudo_class_contains("hover") and self.style_pseudo_class_contains("scanning"):
                        pixbuf = self.svg.get_pixbuf()
                        icon_size = self.get_icon_size()
                        if icon_size:
                            pixbuf = pixbuf.scale_simple(icon_size, icon_size, 3)
                            self.image.set_from_data(pixbuf.get_pixels(),
                                                     Cogl.PixelFormat.RGBA_8888,
                                                     pixbuf.get_width(),
                                                     pixbuf.get_height(),
                                                     pixbuf.get_rowstride())
                    elif not self.disabled and (self.style_pseudo_class_contains("scanning") or self.style_pseudo_class_contains("hover")):
                        self.set_image_white()
                else:
                    pixbuf = self.svg.get_pixbuf()
                    icon_size = self.get_icon_size()
                    if icon_size:
                        pixbuf = pixbuf.scale_simple(icon_size, icon_size, 3)
                        self.image.set_from_data(pixbuf.get_pixels(),
                                                 Cogl.PixelFormat.RGBA_8888,
                                                 pixbuf.get_width(),
                                                 pixbuf.get_height(),
                                                 pixbuf.get_rowstride())
        except AttributeError:
            pass
            
    def hilite_off(self):
        self.style_pseudo_class_remove("hover")
    
    def hilite_on(self):
        self.style_pseudo_class_add("hover")

    #def select_on(self):
    #    self.style_pseudo_class_add("active")

    #def inactivate(self):
    #    self.style_pseudo_class_remove("active")

    def on_select_hilite_off(self, token):
        if token == self.timeout_token:
            self.style_pseudo_class_remove("active")

    def on_click_activate(self, source):
        if self.on_select_hilite_duration:
            self.style_pseudo_class_add("active")
            self.timeout_token = object()
            Clutter.threads_add_timeout(0, self.on_select_hilite_duration, self.on_select_hilite_off, self.timeout_token)
        #self.emit("activate")
    
    def activate(self):
        """
        Completion of scannable interafece.
        :see: Scannable
        """
        self.emit("clicked")

    def is_disabled(self):
        return self.get_disabled()


class BackgroundImage(Clutter.Actor, properties.PropertyAdapter):
    """
    Widget that contains image presenting Pisak standard background pattern
    """
    __gtype_name__ = "PisakBackgroundImage"
    __gproperties__ = {
        "ratio_width": (
            GObject.TYPE_FLOAT, None, None,
            0, 1., 0, GObject.PARAM_READWRITE),
        "ratio_height": (
            GObject.TYPE_FLOAT, None, None,
            0, 1., 0, GObject.PARAM_READWRITE)
    }
    def __init__(self):
        super().__init__()
        self.image_res_path = "background_image.png"
        self.background_image = Clutter.Image()
        self.set_content(self.background_image)
        self._load_image()

    def _load_image(self):
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(res.get(self.image_res_path))
        self.background_image.set_data(pixbuf.get_pixels(),
                                     Cogl.PixelFormat.RGBA_8888,
                                     pixbuf.get_width(),
                                     pixbuf.get_height(),
                                     pixbuf.get_rowstride())

    @property
    def ratio_width(self):
        return self._ratio_width

    @ratio_width.setter
    def ratio_width(self, value):
        self._ratio_width = value
        self.set_width(unit.w(value))

    @property
    def ratio_height(self):
        return self._ratio_height

    @ratio_height.setter
    def ratio_height(self, value):
        self._ratio_height = value
        self.set_height(unit.h(value))


class BackgroundPattern(Clutter.Actor, properties.PropertyAdapter):
    """
    Widget displaying Pisak standard background pattern
    """
    __gtype_name__ = "PisakBackgroundPattern"
    __gproperties__ = {
        "ratio_width": (
            GObject.TYPE_FLOAT, None, None,
            0, 1., 0, GObject.PARAM_READWRITE),
        "ratio_height": (
            GObject.TYPE_FLOAT, None, None,
            0, 1., 0, GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        background_image = Clutter.Canvas()
        background_image.set_size(unit.mm(2), unit.mm(2))
        background_image.connect("draw", self.fence_pattern)
        background_image.invalidate()
        self.set_content(background_image)
        self.set_content_repeat(Clutter.ContentRepeat.BOTH)
        self.set_content_scaling_filters(Clutter.ScalingFilter.TRILINEAR,
                                         Clutter.ScalingFilter.TRILINEAR)

    @staticmethod
    def fence_pattern(canvas, context, w, h):
        context.scale(w, h)
        context.set_line_width(0.05)
        context.set_source_rgba(0, 0, 0, 0.15)
        lines = [(0, 0, 1, 1), (0, 1, 1, 0)]
        for x1, y1, x2, y2 in lines:
            context.move_to(x1, y1)
            context.line_to(x2, y2)
            context.stroke()
        return True

    @property
    def ratio_width(self):
        return self._ratio_width

    @ratio_width.setter
    def ratio_width(self, value):
        self._ratio_width = value
        self.set_width(unit.w(value))

    @property
    def ratio_height(self):
        return self._ratio_height

    @ratio_height.setter
    def ratio_height(self, value):
        self._ratio_height = value
        self.set_height(unit.h(value))
