'''
Module with operations on image data.
'''
from PIL import Image, ImageFilter
from gi.repository import Cogl, Clutter
import random

class PhotoBuffer(object):
    """
    Buffer containing a currently edited photo.
    """
    PIXEL_FORMATS = {'1_1': Cogl.PixelFormat.G_8, 'L_1': Cogl.PixelFormat.A_8,
                     'RGB_2': Cogl.PixelFormat.RGB_565, 'RGB_3': Cogl.PixelFormat.RGB_888,
                     'RGBA_2': Cogl.PixelFormat.RGBA_4444, 'RGBA_4': Cogl.PixelFormat.RGBA_8888}
    def __init__(self, view, photo, slide):
        self.view = view
        self.path = photo.path
        self.slide = slide
        self.original_photo = Image.open(self.path)
        if self.original_photo.mode == 'P':
            self.original_photo = self.original_photo.convert() #translates through built-in palette
        self.buffer = self.original_photo.copy()
        self.zoom_timer = None
        self.noise_timer = None

    def mirror(self, source, event):
        self.buffer = self.buffer.transpose(Image.FLIP_LEFT_RIGHT)

    def grayscale(self, source, event):
        self.buffer = self.buffer.convert('L')

    def rotate(self, source, event):
        self.buffer = self.buffer.transpose(Image.ROTATE_90)

    def solarize(self, source, event):
        threshold = 80
        bands = self.buffer.getbands()
        source = self.buffer.split()
        for idx in range(len(source)):
            if bands[idx] != 'A':
                out = source[idx].point(lambda i: i>threshold and 255-i)
                mask = source[idx].point(lambda i: i>threshold and 255)
                source[idx].paste(out, None, mask)
        mode = self.buffer.mode
        self.buffer = Image.merge(mode, source)

    def invert(self, source, event):
        bands = self.buffer.getbands()
        source = self.buffer.split()
        for idx in range(len(source)):
            if bands[idx] != 'A':
                out = source[idx].point(lambda i: 255-i)
                source[idx].paste(out, None)
        mode = self.buffer.mode
        self.buffer = Image.merge(mode, source)

    def sepia(self, source, event):
        level = 50
        grayscale = self.buffer.convert('L')
        red = grayscale.point(lambda i: i + level*1.5)
        green = grayscale.point(lambda i: i + level)
        blue = grayscale.point(lambda i: i - level*0.5)
        bands = self.buffer.getbands()
        if 'A' not in bands:
            self.buffer = Image.merge('RGB', (red, green, blue))
        else:
            source = self.buffer.split()
            alpha = source[bands.index('A')]
            self.buffer = Image.merge('RGBA', (red, green, blue, alpha))

    def edges(self, source, event):
        bands = self.buffer.getbands()
        source = self.buffer.split()
        for idx in range(len(source)):
            if bands[idx] != 'A':
                out = source[idx].filter(ImageFilter.FIND_EDGES)
                source[idx].paste(out, None)
        mode = self.buffer.mode
        self.buffer = Image.merge(mode, source)

    def contour(self, source, event):
        bands = self.buffer.getbands()
        source = self.buffer.split()
        for idx in range(len(source)):
            if bands[idx] != 'A':
                out = source[idx].filter(ImageFilter.CONTOUR)
                source[idx].paste(out, None)
        mode = self.buffer.mode
        self.buffer = Image.merge(mode, source)

    def noise(self, source, event):
        if not self.noise_timer:
            self.noise_timer = Clutter.Timeline.new(200)
            self.noise_timer.set_repeat_count(50)
            self.noise_timer.connect('completed', self._noise_update)
            self.noise_timer.start()
        else:
            self.noise_timer.stop()
            self.noise_timer = None

    def _noise_update(self, event):
        level = 40
        bands = self.buffer.getbands()
        source = self.buffer.split()
        for idx in range(len(source)):
            if bands[idx] != 'A':
                out = source[idx].point(lambda i: i + random.uniform(-level, level))
                source[idx].paste(out, None)
        mode = self.buffer.mode
        self.buffer = Image.merge(mode, source)

    def zoom(self, source, event):
        if not self.zoom_timer:
            self.zoom_timer = Clutter.Timeline.new(200)
            self.zoom_timer.set_repeat_count(35)
            self.zoom_timer.connect('completed', self._zoom_update)
            self.zoom_timer.start()
        else:
            self.zoom_timer.stop()
            self.zoom_timer = None

    def _zoom_update(self, event):
        width, height = self.buffer.size[0], self.buffer.size[1]
        x0, y0 = width/50, height/50
        x1, y1 = width-x0, height-y0
        self.buffer = self.buffer.transform((width, height), Image.EXTENT, (x0, y0, x1, y1))

    def original(self, source, event):
        self.buffer = self.original_photo.copy()

    def save(self, source, event):
        raise NotImplementedError()

    def _pre_update(self):
        data = self.buffer.tobytes()
        width, height = self.buffer.size[0], self.buffer.size[1]
        pixel_count = width*height
        byte_count = len(data)
        byte_per_pixel = int(byte_count/pixel_count)
        row_stride = byte_count/height
        mode = self.buffer.mode
        pixel_format = '_'.join([mode, str(byte_per_pixel)])
        if pixel_format not in self.PIXEL_FORMATS:
            print('Pixel format {} not supported.'.format(pixel_format))
        else:
            cogl_pixel_format = self.PIXEL_FORMATS[pixel_format]
        return data, cogl_pixel_format, width, height, row_stride

    def _update(self):
        # pass these to the photo_actor and load from data
        # data, pixel_format, width, height, row_stride = self._pre_update()
        pass
