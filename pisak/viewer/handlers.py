from pisak import signals
from pisak.viewer import database_agent, widgets


@signals.registered_handler("viewer/next_page")
def next_page(pager):
    pager.flip()


@signals.registered_handler("viewer/previous_page")
def previous_page(pager):
    pager.previous_page()


@signals.registered_handler("viewer/slideshow_toggle")
def slideshow_toggle(slideshow_widget):
    if slideshow_widget.slideshow_on is True:
        slideshow_widget.stop()
    else:
        slideshow_widget.run()


@signals.registered_handler("viewer/next_slide")
def next_slide(slideshow_widget):
    slideshow_widget.next_slide()


@signals.registered_handler("viewer/previous_slide")
def previous_slide(slideshow_widget):
    slideshow_widget.previous_slide()


@signals.registered_handler("viewer/add_to_favourite_photos")
def add_to_favourite_photos(slideshow_widget):
    path = slideshow_widget.slide.photo_path
    album = slideshow_widget.data_source.data[slideshow_widget.index]["category"]
    database_agent.add_to_favourite_photos(path, album)
    

@signals.registered_handler("viewer/zoom")
def zoom(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.zoom()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.zoom()


@signals.registered_handler("viewer/contour")
def contour(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.contour()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.contour()


@signals.registered_handler("viewer/edges")
def edges(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.edges()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.edges()


@signals.registered_handler("viewer/sepia")
def sepia(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.sepia()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.sepia()

@signals.registered_handler("viewer/invert")
def invert(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.invert()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.invert()


@signals.registered_handler("viewer/rotate")
def rotate(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.rotate()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.rotate()


@signals.registered_handler("viewer/mirror")
def mirror(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.mirror()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.mirror()


@signals.registered_handler("viewer/grayscale")
def grayscale(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.grayscale()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.grayscale()


@signals.registered_handler("viewer/noise")
def noise(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.noise()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.noise()


@signals.registered_handler("viewer/solarize")
def solarize(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.solarize()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.solarize()


@signals.registered_handler("viewer/original")
def original(item):
    if isinstance(item, widgets.PhotoSlide):
        item.image_buffer.original()
    elif isinstance(item, widgets.SlideShow):
        item.slide.image_buffer.original()
