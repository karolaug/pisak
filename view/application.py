import sys
from gi.repository import Clutter, Mx
import unit

class VignetteShader(Clutter.ShaderEffect):
    pass    


class CategoryTile(Clutter.Actor):
    def __init__(self, category):
        super(CategoryTile, self).__init__()
        self.category = category
        self._init_elements()
        
    def _init_elements(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_vertical(True)
        self.preview = Mx.Image()
        self.preview.set_from_file("view/krolikarnia.jpg")
        self.preview.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.label = Mx.Label()
        self.label.set_text(self.category)
        self.add_actor(self.preview)
        self.add_actor(self.label)


class LibraryScroll(Clutter.Actor):
    def __init__(self, contents):
        super(LibraryScroll, self).__init__()
        self.contents=contents
        self.categories = ["Kategoria %d" % i for i in range(12)]
        self.page = 0
        self.time_interval=1000
        self.animation_speed=500
        self.page_count = int((len(self.categories) + (6 // 2)) // 6)
        self._init_tiles()
        self.set_x_expand(True)
        self.set_y_expand(True)
        margin = Clutter.Margin()
        margin.left = margin.right = unit.mm(12)
        self.set_margin(margin)
        self.connect("allocation-changed", self.resize_page)
        self._init_timer()

    def _init_tiles(self):
        self.layout = Clutter.FixedLayout()
        self.set_layout_manager(self.layout)
        self.pop_out = Clutter.Actor()
        self.add_actor(self.pop_out)
        self.page_actor = self.generate_page(self.page)
        self.add_actor(self.page_actor)
        

    def _init_timer(self):

        self.scroll_timer=Clutter.Timeline.new(self.time_interval)
        self.scroll_timer.set_repeat_count(-1)
        self.scroll_timer.connect('completed', lambda _: self.next_page())
        self.scroll_timer.start() 
        self.is_flipping= True


    def resize_page(self, *args):
        self.page_actor.set_size(self.get_width(), self.get_height())
    
    def generate_page(self, page):
        page_actor = Clutter.Actor()
        page_layout = Clutter.GridLayout()
        page_actor.set_layout_manager(page_layout)
        page_layout.set_row_spacing(unit.mm(12))
        page_layout.set_column_spacing(unit.mm(12))
        for i in range(2):
            for j in range(3):
                index = int(page * 6 + i * 3 + j)
                if index < len(self.categories):
                    tile = CategoryTile(self.categories[index])
                    page_layout.attach(tile, j, i, 1, 1)
        page_actor.set_size(self.get_width(), self.get_height())
        page_actor.set_x_expand(True)
        page_actor.set_y_expand(True)
        #page_actor.set_x(1366 - self.get_x())
        return page_actor
    
    def slide_in(self,page_actor):
        page_actor.set_x(-1366)
        page_actor.animatev(Clutter.AnimationMode.EASE_IN_OUT_QUAD, self.animation_speed, ["x"], [0])
        
    def slide_out(self,page_actor):
        page_actor.animatev(Clutter.AnimationMode.EASE_IN_OUT_QUAD, self.animation_speed, ["x"], [1366])
    
    def next_page(self):
        self.page = (self.page + 1) % self.page_count
        new_page_actor = self.generate_page(self.page)
        
        self.add_actor(new_page_actor)
        self.slide_in(new_page_actor)
        self.slide_out(self.page_actor)
        self.page_actor = new_page_actor

        progress= float(self.page +1 )/self.page_count
        self.update_scrollbar(progress)

    def toggle_flip(self):

        '''Makes pages to start or stop flipping'''
        if self.is_flipping:
            self.scroll_timer.stop()
            self.is_flipping= False
        else:
            self.scroll_timer.start()
            self.is_flipping= True

    def update_scrollbar(self,progress):
        self.contents.update_scrollbar(progress)

class LibraryViewContents(Clutter.Actor):
    def __init__(self):
        super(LibraryViewContents, self).__init__()
        self._init_elements()
        self.set_y_expand(True)
    
    def _init_elements(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_vertical(True)
        self.layout.set_spacing(30)
        self.scroll = LibraryScroll(self)
        #self.scrollbar = Clutter.Texture.new_from_file("view/jagoda.jpg")
        #self.scrollbar.set_height(20)

        self.scrollbar=Mx.ProgressBar.new()
        self.scrollbar.set_x_expand(True)
        page_ratio=1./self.scroll.page_count 
        self.scrollbar.set_progress(page_ratio)
        self.scrollbar.set_height(30)
        
        self.add_actor(self.scroll)
        self.add_actor(self.scrollbar)

    def update_scrollbar(self,progress):
        self.scrollbar.animatev(Clutter.AnimationMode.LINEAR, self.scroll.animation_speed, ['progress'],[progress])
    
    def toggle_flip(self):
        self.scroll.toggle_flip()
        #self.scrollbar.update(self.scroll.get_page())
    

class LibraryView(Clutter.Actor):
    def __init__(self):
        super(LibraryView, self).__init__()
        self.set_clip_to_allocation(True)
        self._init_elements()
    
    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.contents = LibraryViewContents()
        self.add_actor(self.contents)
        self.add_actor(PisakBackground())
    
    def toggle_flip(self):
        self.contents.toggle_flip()


class PisakBackground(Clutter.Actor):
    def __init__(self):
        super(PisakBackground, self).__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.image = Clutter.Texture.new_from_file("hyperbolic_vignette.png")
        self.add_actor(self.image)


class PisakViewerButtons(Clutter.Actor):
    def __init__(self, viewer):
        super(PisakViewerButtons, self).__init__()
        self.viewer = viewer
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.exit_button=Mx.Button()
        self.exit_button.set_label('exit')
        self.exit_button.set_y_expand(True)
        self.exit_button.set_width(unit.mm(30))
        self.exit_button.connect("clicked", lambda _: self.exit_app() )
        self.set_x_align(Clutter.ActorAlign.CENTER)
        
        self.button = Mx.Button()
        self.button.set_label(">>")
        self.button.set_y_expand(True)
        self.button.set_width(unit.mm(30))
        self.button.connect("clicked", lambda _: self.toggle_flip() )
        self.add_actor(self.button)
        self.add_actor(self.exit_button)

    def exit_app(self):
        self.viewer.exit_app()
        
    def toggle_flip(self):
        self.viewer.toggle_flip()


class PisakViewerContainer(Clutter.Actor):
    def __init__(self,stage):
        super(PisakViewerContainer, self).__init__()
        self.stage=stage
        self._init_elements()
        margin = Clutter.Margin()
        margin.left = margin.right = margin.top = margin.bottom = unit.mm(12)
        self.set_margin(margin)
        
    def _init_elements(self):
        color_1 = Clutter.Color.new(128, 160, 224, 255)
        self.main = LibraryView()
        self.main.set_x_expand(True)
        self.main.set_y_expand(True)
        self.buttons = PisakViewerButtons(self)
        self.buttons.set_y_expand(False)
        self.buttons.set_x_expand(True)
        self.buttons.set_height(unit.mm(25))
        
        layout = Clutter.BoxLayout()
        layout.set_vertical(True)
        self.set_layout_manager(layout)
        layout.set_spacing(unit.mm(12))
        self.add_actor(self.main)
        self.add_actor(self.buttons)
     
    def toggle_flip(self):
        self.main.toggle_flip()

    def exit_app(self):
        self.stage.exit_app()


class PisakViewerStage(Clutter.Stage):
    def __init__(self):
        super(PisakViewerStage, self).__init__()
        self._init_elements()
    
    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        #self.background = PisakBackground()
        #self.add_actor(self.background)
        self.contents = PisakViewerContainer(self)
        self.add_actor(self.contents)

    def exit_app(self):
        self.destroy()
    

class PisakViewApp(object):
    def __init__(self, argv):
        PisakViewApp.APP = self
        Clutter.init(argv)
        self.stage = PisakViewerStage()
        self.stage.connect("destroy", lambda _: Clutter.main_quit())
        self.stage.set_fullscreen(True)
        self.stage.show_all()
    
    
    def main(self):
        Clutter.main()

PisakViewApp(sys.argv).main()

