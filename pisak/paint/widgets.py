import sys
import os
import math

from gi.repository import GObject, Clutter, Gdk, Mx
import cairo

from pisak import widgets, layout, xdg


SAVING_PATH  = os.path.join(xdg.get_dir("pictures"), "pisak_paint.png")


class Button(widgets.Button):
    """
    Stylable, paint-specific button widget.
    """
    __gtype_name__ = "PisakPaintButton"


class EaselTool(Clutter.Actor):
    """
    Interface of the easel tools.
    """
    def run(self):
        """
        Make the tool going.
        """
        raise NotImplementedError

    def kill(self):
        """
        Stop all the on-going activity and kill the tool.
        """
        raise NotImplementedError

    def on_user_click(self):
        """
        Public signal handler.
        """
        raise NotImplementedError
    

class Navigator(EaselTool):
    """
    Easel tool, widget displaying straight, rotating line that indicates angle
    of the line to be drawn.
    """
    __gsignals__ = {
        "angle-declared": (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_FLOAT,)),
        "idle": (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    
    def __init__(self):
        super().__init__()
        self.canvas = Clutter.Canvas()
        self.set_content(self.canvas)
        self.rotations_count = 1 # limit of navigator idle rotations
        self.step_duration = 50  # pace of navigator in mscs
        self.step = 0.007  # navigator rotation fluency in radians
        self.rgba = (0, 0, 0, 255)  # current navigator color
        self.line_width = 5  # current navigator line width
        self.click_handlers = [self._on_user_decision]  # handlers of user click

    def run(self, from_x, from_y, color, line_width):
        """
        Turn on the navigator, begin line rotation.
        :param from_x: x coordinate of the navigator base point
        :param from_y: y coordinate of the navigator base point
        :param color: color of the navigator line
        :line_width:: width of the navigator line in pixels
        """
        self.angle = 0
        self.width, self.height = self.get_size()
        self.diagonal = (self.width**2 + self.height**2)**0.5
        self.canvas.set_size(self.width, self.height)
        self.canvas.connect("draw", self._draw)
        self.from_x = from_x
        self.from_y = from_y
        self.timer = Clutter.Timeline.new(self.step_duration)
        repeat_count = -1 if self.rotations_count == -1 else \
                       self.rotations_count * 2 * math.pi / self.step
        self.timer.set_repeat_count(repeat_count)
        self.timer.connect("completed", self._update_navigator)
        self.timer.connect("stopped", self._on_user_idle)
        self.timer.start()

    def on_user_click(self, source, event):
        """
        Public signal handler calling internally declared functions.
        """
        for handler in self.click_handlers:
            handler(source, event)

    def kill(self):
        """
        Stop all the on-going activities and kill the navigator.
        """
        self._clean_up()
        self.timer.stop()

    def _on_user_decision(self, source, event):
        self._clean_up()
        self.timer.stop()
        self.emit("angle-declared", self.angle)

    def _on_user_idle(self, source, event):
        self._clean_up()
        self.emit("idle")

    def _clean_up(self):
        self._clear_canvas()
        self.timer.disconnect_by_func(self._on_user_idle)
        self.timer.disconnect_by_func(self._update_navigator)
        self.canvas.disconnect_by_func(self._draw)

    def _clear_canvas(self):
        self.canvas.disconnect_by_func(self._draw)
        self.canvas.connect("draw", self._draw_clear)
        self.canvas.invalidate()
        self.canvas.disconnect_by_func(self._draw_clear)
        self.canvas.connect("draw", self._draw)

    def _update_navigator(self, event):
        self.angle += self.step
        self.canvas.invalidate()

    def _draw_clear(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(0, 0, 0, 0)
        ctxt.paint()
        return True

    def _draw(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(0, 0, 0, 0)
        ctxt.paint()
        ctxt.translate(self.from_x, self.from_y)
        ctxt.rotate(self.angle)
        ctxt.scale(self.diagonal/width, 1)
        ctxt.move_to(0, 0)
        ctxt.line_to(width, 0)
        ctxt.set_line_width(self.line_width)
        ctxt.set_source_rgba(self.rgba[0],
                             self.rgba[1],
                             self.rgba[2],
                             self.rgba[3])
        ctxt.stroke()
        return True


class Localizer(EaselTool):
    """
    Easel tool, used for localization of the new point for drawing.
    Displays straight lines, first one moving in vertical and the second one in
    horizontal direction.
    """
    __gsignals__ = {
        "point-declared": (
            GObject.SIGNAL_RUN_FIRST,
            None, (GObject.TYPE_FLOAT, GObject.TYPE_FLOAT,)),
        "horizontal-idle": (
            GObject.SIGNAL_RUN_FIRST,
            None, ()),
        "vertical-idle": (
            GObject.SIGNAL_RUN_FIRST,
            None, ())
    }
    def __init__(self):
        super().__init__()
        self.canvas = Clutter.Canvas()
        self.set_content(self.canvas)
        self.horizontal_timer = None  # timer ticking on horizontal movement
        self.vertical_timer = None  # timer ticking on vertical movement
        self.vertical_count = -1  # limit of vertical localizer cycles
        self.horizontal_count = -1  # limit of horizontal localizer cycles
        self.rgba = (0, 0, 0, 255)  # current localizer color
        self.line_width = 5  # localizer line width
        self.step_duration = 10  # pace of localizer in mscs
        self.step = 1  # localizer fluency in pixels
        self.click_handlers = []  # handlers of user click

    def run(self):
        """
        Turn on the localizer, declare initial parameters, begin the
        vertical line movement.
        """
        self.localized_x = None
        self.localized_y = None
        self.x = 0
        self.y = 0
        self.from_x = 0
        self.from_y = 0
        self.to_x = 0
        self.to_y = 0
        self.width, self.height = self.get_size()
        self.canvas.set_size(self.width, self.height)
        self.canvas.connect("draw", self._draw)
        self._run_vertical()

    def on_user_click(self, source, event):
        """
        Public signal handler calling internally declared functions.
        """
        for handler in self.click_handlers:
            handler(source, event)

    def kill(self):
        """
        Stop all the on-going activities and kill the localizer.
        """
        if self.vertical_timer is not None and self.vertical_timer.is_playing():
            self._clean_up_vertical()
            self.vertical_timer.stop()
        if self.horizontal_timer is not None and \
               self.horizontal_timer.is_playing():
            self._clean_up_horizontal()
            self.horizontal_timer.stop()

    def _run_vertical(self):
        self.vertical_timer = Clutter.Timeline.new(self.step_duration)
        repeat = self.vertical_count if self.vertical_count == -1 \
                 else self.vertical_count * self.width / self.step
        self.vertical_timer.set_repeat_count(repeat)
        self.vertical_timer.connect("completed", self._update_vertical)
        self.vertical_timer.connect("stopped", self._on_vertical_idle)
        self.click_handlers = [self._stop_vertical, self._run_horizontal]
        self.vertical_timer.start()

    def _update_vertical(self, event):
        self.x = self.from_x = self.to_x = (self.from_x + self.step) \
                 % self.width
        self.from_y, self.to_y = 0, self.height
        self.canvas.invalidate()

    def _on_vertical_idle(self, source, event):
        self._clean_up_vertical()
        self.emit("vertical-idle")
        
    def _stop_vertical(self, source, event):
        self._clean_up_vertical()
        self.vertical_timer.stop()
        self.localized_x = self.x

    def _clean_up_vertical(self):
        self.vertical_timer.disconnect_by_func(self._on_vertical_idle)
        self.vertical_timer.disconnect_by_func(self._update_vertical)

    def _run_horizontal(self, source, event):
        self.horizontal_timer = Clutter.Timeline.new(self.step_duration)
        repeat = self.horizontal_count if self.horizontal_count == -1 \
                 else self.horizontal_count * self.width / self.step
        self.horizontal_timer.set_repeat_count(repeat)
        self.horizontal_timer.connect("completed", self._update_horizontal)
        self.horizontal_timer.connect("stopped", self._on_horizontal_idle)
        self.click_handlers = [self._stop_horizontal]
        self.horizontal_timer.start()

    def _update_horizontal(self, event):
        self.from_x, self.to_x = 0, self.width
        self.y = self.from_y = self.to_y = (self.y + self.step) % self.height
        self.canvas.invalidate()

    def _stop_horizontal(self, source, event):
        self._clean_up_horizontal()
        self.horizontal_timer.stop()
        self.localized_y = self.y
        self._point_declared()

    def _on_horizontal_idle(self, source, event):
        self._clean_up_horizontal()
        self.emit("horizontal-idle")

    def _clean_up_horizontal(self):
        self._clear_canvas()
        self.horizontal_timer.disconnect_by_func(self._on_horizontal_idle)
        self.horizontal_timer.disconnect_by_func(self._update_horizontal)
        self.canvas.disconnect_by_func(self._draw)

    def _point_declared(self, *args):
        self.emit("point-declared", self.localized_x, self.localized_y)

    def _clear_canvas(self):
        self.canvas.disconnect_by_func(self._draw)
        self.canvas.connect("draw", self._draw_clear)
        self.canvas.invalidate()
        self.canvas.disconnect_by_func(self._draw_clear)
        self.canvas.connect("draw", self._draw)

    def _draw_clear(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(0, 0, 0, 0)
        ctxt.paint()
        return True

    def _draw(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(0, 0, 0, 0)
        ctxt.paint()
        ctxt.set_line_width(self.line_width)
        ctxt.set_source_rgba(self.rgba[0],
                             self.rgba[1],
                             self.rgba[2],
                             self.rgba[3])
        if self.localized_x is not None:
            ctxt.move_to(self.localized_x, 0)
            ctxt.line_to(self.localized_x, self.height)
            ctxt.stroke()
        ctxt.move_to(self.from_x, self.from_y)
        ctxt.line_to(self.to_x, self.to_y)
        ctxt.stroke()
        return True


class Bender(EaselTool):
    """
    Easel tool, displays line spanned between two declared points,
    with different levels of curvature.
    """
    __gsignals__ = {
        "bend-point-declared": (
            GObject.SIGNAL_RUN_FIRST,
            None, (GObject.TYPE_FLOAT, GObject.TYPE_FLOAT)),
        "idle": (
            GObject.SIGNAL_RUN_FIRST, None, ())    
    }
    def __init__(self):
        super().__init__()
        self.canvas = Clutter.Canvas()
        self.set_content(self.canvas)
        self.bender_cycles_count = -1  # bender cycles repeat count
        self.step_duration = 50  # pace of nbender in mscs
        self.step = 10 # bender fluency in pixels
        self.repeat_index = 0  # counter of cycles repeats
        self.click_handlers = [self._on_user_decision] # handlers of user click

    def run(self, from_x, from_y, to_x, to_y, angle, color, line_width):
        """
        Turn on the bender, declare initial parameters, begin the
        bending animation.
        :param from_x: x coordinate of the line first point
        :param from_y: y coordinate of the line first point
        :param to_x: x coordinate of the line second point
        :param to_y: y coordinate of the line second point
        :param angle: angle of the line's plane in user's space in radians
        :param color: color of the bender line
        :param line_width: width of the bender line
        """
        self.width, self.height = self.get_size()
        self.canvas.set_size(self.width, self.height)
        self.angle = angle + math.pi/2
        self.canvas.connect("draw", self._draw)
        self.rgba = color
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.middle_x = self.through_x = self.from_x + \
                        (self.to_x - self.from_x) / 2
        self.middle_y = self.through_y = self.from_y + \
                        (self.to_y - self.from_y) / 2
        self.step_x = math.cos(self.angle) * self.step
        self.step_y = math.sin(self.angle) * self.step
        self.line_width = line_width
        self.timer = Clutter.Timeline.new(self.step_duration)
        self.timer.set_repeat_count(-1)
        self.timer.connect("completed", self._update_bender)
        self.timer.connect("stopped", self._on_user_idle)
        self.timer.start()
            
                
    def on_user_click(self, source, event):
        """
        Public signal handler calling internally declared functions.
        """
        for handler in self.click_handlers:
            handler(source, event)

    def kill(self):
        """
        Stop all the on-going activities and kill the bender.
        """
        self._clean_up()
        self.timer.stop()

    def _on_user_decision(self, source, event):
        self._clean_up()
        self.timer.stop()
        self.emit("bend-point-declared", self.through_x, self.through_y)

    def _on_user_idle(self, source, event):
        self._clean_up()
        self.emit("idle")  
    
    def _clean_up(self):
        self.timer.disconnect_by_func(self._update_bender)
        self.timer.disconnect_by_func(self._on_user_idle)
        self._clear_canvas()
        self.canvas.disconnect_by_func(self._draw)

    def _clear_canvas(self):
        self.canvas.disconnect_by_func(self._draw)
        self.canvas.connect("draw", self._draw_clear)
        self.canvas.invalidate()
        self.canvas.disconnect_by_func(self._draw_clear)
        self.canvas.connect("draw", self._draw)

    def _update_bender(self, event):
        through_x = self.through_x + self.step_x
        through_y = self.through_y + self.step_y
        if (through_x > self.width or through_x < 0
            or through_y > self.height or through_y < 0):
            self.step_x *= -1
            self.step_y *= -1
        self.through_x += self.step_x
        self.through_y += self.step_y
        self.canvas.invalidate()
        self._check_repeat_count()

    def _check_repeat_count(self):
        if math.ceil(self.through_x) == math.floor(self.middle_x):
            self.repeat_index += 1
            if self.repeat_index / 2 == self.bender_cycles_count:
                self.timer.stop()
                self.repeat_index = 0

    def _draw_clear(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(0, 0, 0, 0)
        ctxt.paint()
        return True
        
    def _draw(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(0, 0, 0, 0)
        ctxt.paint()
        ctxt.set_line_cap(cairo.LINE_CAP_ROUND)
        ctxt.set_line_width(self.line_width)
        ctxt.move_to(self.from_x, self.from_y)
        ctxt.curve_to(self.from_x, self.from_y, self.through_x,
                      self.through_y, self.to_x, self.to_y)
        ctxt.set_source_rgba(self.rgba[0],
                             self.rgba[1],
                             self.rgba[2],
                             self.rgba[3])
        ctxt.stroke()
        return True


class Yardstick(EaselTool):
    """
    Easel tool, widget displaying straigh line of increasing length, reflecting
    user's need for specifing line length.
    """
    __gsignals__ = {
        "destination-declared": (
            GObject.SIGNAL_RUN_FIRST,
            None, (GObject.TYPE_FLOAT, GObject.TYPE_FLOAT)),
        "idle": (
            GObject.SIGNAL_RUN_FIRST,
            None, ()),
    }
    def __init__(self):
        super().__init__()
        self.canvas = Clutter.Canvas()
        self.set_content(self.canvas)
        self.step_duration = 100  # pace of yardstick in mscs
        self.step = 10 # yardstick fluency in pixels
        self.click_handlers = [self._on_user_decision] # handlers of user click

    def run(self, from_x, from_y, angle, color, line_width):
        """
        Turn on the yardstick, declare initial parameters, begin the
        measuring animation.
        :param from_x: x coordinate of the line base point
        :param from_y: y coordinate of the line base point
        :param angle: angle of the line's plane in user's space in radians
        :param color: color of the yardstick line
        :param line_width: width of the yardstick line
        """
        self.to_x = self.base_x = self.from_x = from_x
        self.to_y = self.base_y = self.from_y = from_y
        self.angle = angle
        self.rgba = color
        self.step_x = math.cos(self.angle) * self.step
        self.step_y = math.sin(self.angle) * self.step
        self.line_width = line_width
        self.width, self.height = self.get_size()
        self.canvas.set_size(self.width, self.height)
        self.canvas.connect("draw", self._draw)
        self.timer = Clutter.Timeline.new(self.step_duration)
        self.timer.set_repeat_count(-1)
        self.timer.connect("stopped", self._on_user_idle)
        self.timer.connect("completed", self._update_yardstick)
        self.timer.start()

    def on_user_click(self, source, event):
        """
        Public signal handler calling internally declared functions.
        """
        for handler in self.click_handlers:
            handler(source, event)

    def kill(self):
        """
        Stop all the on-going activities and kill the yardstick.
        """
        self._clean_up()
        self.timer.stop()

    def _on_user_idle(self, source, event):
        self._clean_up()
        self.emit("idle")

    def _on_user_decision(self, source, event):
        self._clean_up()
        self.timer.stop()
        self.emit("destination-declared", self.to_x, self.to_y)

    def _clean_up(self):
        self.timer.disconnect_by_func(self._on_user_idle)
        self.timer.disconnect_by_func(self._update_yardstick)
        self._clear_canvas()
        self.canvas.disconnect_by_func(self._draw)

    def _clear_canvas(self):
        self.canvas.disconnect_by_func(self._draw)
        self.canvas.connect("draw", self._draw_clear)
        self.canvas.invalidate()
        self.canvas.disconnect_by_func(self._draw_clear)
        self.canvas.connect("draw", self._draw)

    def _on_screen_border(self):
        self._on_user_decision(None, None)
        
    def _update_yardstick(self, event):
        to_x = self.to_x + self.step_x
        to_y = self.to_y + self.step_y
        if 0 <= to_x <= self.width and 0 <= to_y <= self.height:
            self.to_x, self.to_y = to_x, to_y
            self.canvas.invalidate()
        else:
            self._on_screen_border()

    def _draw_clear(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(0, 0, 0, 0)
        ctxt.paint()
        return True

    def _draw(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(0, 0, 0, 0)
        ctxt.paint()
        ctxt.set_line_cap(cairo.LINE_CAP_ROUND)
        ctxt.set_line_width(self.line_width)
        ctxt.move_to(self.base_x, self.base_y)
        ctxt.line_to(self.to_x, self.to_y)
        ctxt.set_source_rgba(self.rgba[0],
                             self.rgba[1],
                             self.rgba[2],
                             self.rgba[3])
        ctxt.stroke()
        return True


class Easel(layout.Bin):
    """
    Paint main widget, displaying canvas on which all the drawing is going on.
    Displays all the tools needed for proper drawing.
    Communicates with its own stage, connects signals.
    """
    __gtype_name__ = "PisakPaintEasel"
    __gsignals__ = {
        "exit": (
            GObject.SIGNAL_RUN_FIRST,
            None, ())
    }
    
    def __init__(self):
        self.canvas = Clutter.Canvas()
        self.set_content(self.canvas)
        self.localizer = None
        self.navigator = None
        self.yardstick = None
        self.bender = None
        self.stage = None
        self.working_tool = None  # currently working tool
        self.line_width = 10  # width of the drawing line
        self.rgba = (0, 0, 0, 1)  # current drawing color
        self.from_x = 0  # x coordinate of current spot
        self.from_y = 0  # x coordinate of current spot
        self.to_x = 0 # x coordinate of current destination spot
        self.to_y = 0 # y coordinate of current destination spot
        self.through_x = 0  # x coordinate of current through spot
        self.through_y = 0  # y coordinate of current through spot
        self.background_color = (1, 1, 1, 1)  # color of the background
                                                      # canvas
        self.path_history = []  # history of drawing
        self.line_cap = cairo.LINE_CAP_ROUND  # cap of the draw lines
        self.angle = 0  # angle of the draw line direction
        self.stage_handler_id = 0  # id of the current stage handler
        self.set_background_color(Clutter.Color.new(255*self.background_color[0],
                                                     255*self.background_color[1],
                                                     255*self.background_color[2],
                                                     255*self.background_color[3]))
        self.connect("notify::mapped", self._on_mapped)

    def _on_mapped(self, source, args):
        try:
            self.disconnect_by_func(self._on_mapped)
        except TypeError:
            pass
        if self.stage is None:
            self.width, self.height = self.get_allocation_box().get_size()
            self.canvas.set_size(self.width, self.height)
            self.canvas.connect("draw", self._draw)
            self._set_canvas_background()
            self.stage = self.get_stage()
        
    def run(self):
        """
        Run the initial easel tool.
        """
        self.run_localizer()

    def _set_canvas_background(self):
        try:
            self.canvas.disconnect_by_func(self._draw)
        except TypeError:
            pass
        self.canvas.connect("draw", self._draw_background)
        self.canvas.invalidate()
        self.canvas.disconnect_by_func(self._draw_background)
        self.canvas.connect("draw", self._draw)
        
    def run_localizer(self):
        """
        Run the localizer tool, connect proper handler to the stage, connect
        signal to the localizer.
        """
        if self.localizer is None:
            self.localizer = Localizer()
            self.localizer.set_size(self.width, self.height)
            self.add_child(self.localizer)
            self.localizer.connect("point-declared", self._exit_localizer)
            self.localizer.connect("horizontal-idle", self._exit)
        self.set_child_above_sibling(self.localizer, None)
        for tool in self.get_children():
            if tool is not self.localizer:
                tool.hide()
        self.localizer.show()
        self.working_tool = self.localizer
        self.localizer.run()
        self.stage_handler_id = self.stage.connect("button-press-event",
                                                   self.localizer.on_user_click)

    def _exit_localizer(self, source, from_x, from_y):
        self.working_tool = None
        self.from_x = from_x
        self.from_y = from_y
        self.stage.disconnect_by_func(self.localizer.on_user_click)
        self.run_navigator()

    def run_navigator(self):
        """
        Run the navigator tool, connect proper handler to the stage, connect
        signal to the navigator.
        """
        if self.navigator is None:
            self.navigator = Navigator()
            self.navigator.set_size(self.width, self.height)
            self.add_child(self.navigator)
            self.navigator.connect("angle-declared", self._exit_navigator)
            self.navigator.connect("idle", self._exit)
        self.set_child_above_sibling(self.navigator, None)
        self.working_tool = self.navigator
        for tool in self.get_children():
            if tool is not self.navigator:
                tool.hide()
        self.navigator.show()
        self.stage_handler_id = self.stage.connect("button-press-event", self.navigator.on_user_click)
        self.navigator.run(self.from_x, self.from_y, self.rgba, self.line_width)

    def _exit_navigator(self, source, angle):
        self.working_tool = None
        self.angle = angle
        self.stage.disconnect_by_func(self.navigator.on_user_click)
        self.run_yardstick()

    def run_yardstick(self):
        """
        Run the yardstick tool, connect proper handler to the stage, connect
        signal to the yardstick.
        """
        if self.yardstick is None:
            self.yardstick = Yardstick()
            self.yardstick.set_size(self.width, self.height)
            self.add_child(self.yardstick)
            self.yardstick.connect("destination-declared", self._exit_yardstick)
            self.yardstick.connect("idle", self._exit)
            self.working_tool = self.yardstick
        self.stage_handler_id = self.stage.connect("button-press-event",
                                                   self.yardstick.on_user_click)
        for tool in self.get_children():
            if tool is not self.yardstick:
                tool.hide()
        self.yardstick.show()
        self.set_child_above_sibling(self.yardstick, None)
        self.yardstick.run(self.from_x, self.from_y, self.angle, self.rgba,
                           self.line_width)

    def _exit_yardstick(self, event, to_x, to_y):
        self.working_tool = None
        self.to_x = to_x
        self.to_y = to_y
        self.stage.disconnect_by_func(self.yardstick.on_user_click)
        self.run_bender()

    def run_bender(self):
        """
        Run the bender tool, connect proper handler to the stage, connect
        signal to the bender.
        """
        if self.bender is None:
            self.bender = Bender()
            self.bender.set_size(self.width, self.height)
            self.add_child(self.bender)
            self.bender.connect("bend-point-declared", self._exit_bender)
            self.bender.connect("idle", self._exit)
        self.working_tool = self.bender
        self.stage_handler_id = self.stage.connect("button-press-event",
                                                   self.bender.on_user_click)
        for tool in self.get_children():
            if tool is not self.bender:
                tool.hide()
        self.bender.show()
        self.set_child_above_sibling(self.bender, None)
        self.bender.run(self.from_x, self.from_y, self.to_x, self.to_y,
                        self.angle, self.rgba, self.line_width)

    def _exit_bender(self, event, through_x, through_y):
        self.working_tool = None
        self.through_x = through_x
        self.through_y = through_y
        self.stage.disconnect_by_func(self.bender.on_user_click)
        self.run_drawing()

    def run_drawing(self):
        """
        Run drawing with previously declared parameters.
        """
        self.working_tool = None
        for tool in self.get_children():
            tool.hide()
        self.canvas.invalidate()
        self._update_values()
        for tool in self.get_children():
            tool.show()
        self.run_navigator()

    def _update_values(self):
        self.from_x, self.from_y = self.to_x, self.to_y

    def _draw_background(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(self.background_color[0],
                             self.background_color[1],
                             self.background_color[2],
                             self.background_color[3])
        ctxt.paint()
        self.path_history = []
        return True

    def _draw_to_file(self, cnvs, ctxt, width, height):
        ctxt.get_target().write_to_png(SAVING_PATH)
        return True

    def _draw_erase(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(self.background_color[0],
                            self.background_color[1],
                            self.background_color[2],
                            self.background_color[3])
        ctxt.paint()
        if len(self.path_history) > 0:
            self.path_history.pop()
            for desc in self.path_history:
                ctxt.append_path(desc["path"])
                ctxt.set_line_width(desc["line_width"]+1)
                ctxt.set_line_cap(desc["line_cap"])
                color = desc["color"]
                ctxt.set_source_rgba(color[0],
                                color[1],
                                color[2],
                                color[3])
                ctxt.stroke()
        return True
    
    def _draw(self, cnvs, ctxt, width, height):
        ctxt.set_operator(cairo.OPERATOR_SOURCE)
        ctxt.set_source_rgba(self.background_color[0],
                            self.background_color[1],
                            self.background_color[2],
                            self.background_color[3])
        ctxt.paint()
        for desc in self.path_history:
            ctxt.append_path(desc["path"])
            ctxt.set_line_width(desc["line_width"])
            ctxt.set_line_cap(desc["line_cap"])
            color = desc["color"]
            ctxt.set_source_rgba(color[0],
                                color[1],
                                color[2],
                                color[3])
            ctxt.stroke()
        ctxt.curve_to(self.from_x, self.from_y, self.through_x,
                      self.through_y, self.to_x, self.to_y)
        ctxt.set_line_width(self.line_width)
        ctxt.set_line_cap(self.line_cap)
        ctxt.set_source_rgba(self.rgba[0],
                             self.rgba[1],
                             self.rgba[2],
                             self.rgba[3])
        self.path_history.append({"path": ctxt.copy_path(),
                                  "line_width": self.line_width,
                                  "line_cap": self.line_cap,
                                  "color": self.rgba})
        ctxt.stroke()
        return True

    def _exit(self, event):
        self.working_tool = None
        if self.stage.handler_is_connected(self.stage_handler_id):
            self.stage.handler_disconnect(self.stage_handler_id)
        self.emit("exit")

    def clear_canvas(self):
        """
        Clear all the canvas, paint background.
        """
        self._set_canvas_background()

    def back_to_drawing(self):
        """
        Return to easel, run the navigator tool.
        """
        if not self.working_tool:
            self.run_navigator()

    def localize_new_spot(self):
        """
        Run the localizer tool in order to find the new spot for drawing.
        """
        if not self.working_tool:
            self.run_localizer()

    def erase(self):
        """
        Erase the last drawn element.
        """
        try:
            self.canvas.disconnect_by_func(self._draw)
        except TypeError:
            pass
        self.canvas.connect("draw", self._draw_erase)
        self.canvas.invalidate()
        self.canvas.disconnect_by_func(self._draw_erase)
        self.canvas.connect("draw", self._draw)

    def save_to_file(self):
        """
        Save the canvas' current target to file in png format.
        """
        try:
            self.canvas.disconnect_by_func(self._draw)
        except TypeError:
            pass
        self.canvas.connect("draw", self._draw_to_file)
        self.canvas.invalidate()
        self.canvas.disconnect_by_func(self._draw_to_file)
        self.canvas.connect("draw", self._draw)

    def clean_up(self, source):
        """
        Stop all the on-going activities, disconnect signals from the stage.
        """
        if self.working_tool is not None:
            self.working_tool.kill()
        if self.stage.handler_is_connected(self.stage_handler_id):
            self.stage.handler_disconnect(self.stage_handler_id)
