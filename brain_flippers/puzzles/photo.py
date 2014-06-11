from PIL import Image, ImageDraw

class Photo(object):
    DIVISIONS = {2 : (2, 1), 4: (2, 2), 6 : (3, 2), 12 : (4, 3), 16 : (4, 4),
                 20 : (5, 4), 24 : (6, 4), 30 : (6, 5), 35 : (7, 5), 
                 40 : (8, 5), 48 : (8, 6)}

    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.resize()
        self.mask = Image.new('1', self.image.size)
        shade = Image.new('RGB', self.image.size, 'grey')
        self.shaded = Image.blend(self.image, shade, 0.7)
        self.maskDraw = ImageDraw.Draw(self.mask)
        self.rect_div()

    def resize(self, size=(600, 600)):
        if self.image.size != size:
            self.image = self.image.resize(size, Image.ANTIALIAS)

    def rect_div(self, nr_parts=6):
        self.diff = tuple(self.image.size[i] // self.DIVISIONS[nr_parts][i] 
                          for i in range(2))
        self.parts = []
        for row in range(self.DIVISIONS[nr_parts][1]):
            for column in range(self.DIVISIONS[nr_parts][0]):
                start = (self.diff[0] * column, self.diff[1] * row)
                end = (self.diff[0] * (column + 1) - 1, 
                       self.diff[1] * (row + 1) - 1)
                for i in range(2):
                    if self.image.size[i] - end[i] < self.diff[i]:
                        end = list(end)
                        end[i] = self.image.size[i]
                        end = tuple(end)
                self.parts.append((start, end))
        self.work_parts = self.parts.copy()
        
    def next_square(self):
        try:
            self.square = self.work_parts.pop(0)
            (left, upper), (right, lower) = self.square
            self.part_image = self.image.crop((left, upper, right, lower))
            self.maskDraw.rectangle(self.square, fill=255)
            self.unshaded = Image.composite(self.image, self.shaded, 
                                            self.mask)
            self.unshadedDraw = ImageDraw.Draw(self.unshaded)
            self.unshadedDraw.rectangle(self.square, outline=(255, 0, 0))
        except IndexError:
            print('Whole image has been uncovered.')
        
