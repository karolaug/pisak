import sys
from pisak import switcher_app
from gi.repository import Clutter, GObject, Mx, Gst, ClutterGst

class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        ClutterGst.init()
        self.button = Mx.Button()
        self.button.set_label("Don't click")
        self.add_child(self.button)
        
        self.video_texture = ClutterGst.VideoTexture(**{"disable-slicing": True})
        self.add_child(self.video_texture)
        
        try:
            filename = sys.argv[1]
        except IndexError:
            filename = input('Please provide the path to the video file you want to be played:\n')
        self.video_texture.set_filename(filename)
        self.video_texture.set_playing(True)
        
        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.set_layout_manager(self.layout)


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()
        

if __name__ == '__main__':
    ButtonApp(sys.argv).main()
