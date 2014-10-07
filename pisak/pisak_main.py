from collections import ChainMap

from pisak import launcher
import pisak.viewer.app
import pisak.speller.app
import pisak.paint.app
import pisak.main_panel.app
import pisak.symboler.app


ALL_VIEWS = dict(ChainMap(
        pisak.main_panel.app.VIEWS,
        pisak.viewer.app.VIEWS,
        pisak.paint.app.VIEWS,
        pisak.speller.app.VIEWS,
        pisak.symboler.app.VIEWS))


if __name__ == "__main__":
    _pisak_main = {
        "views": ALL_VIEWS,
        "initial-view": "main_panel/main",
        "initial-data": None
    }
    launcher.run(_pisak_main)
