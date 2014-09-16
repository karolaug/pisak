from collections import ChainMap

from pisak import launcher
import pisak.viewer.app
import pisak.speller.app
import pisak.main_panel.app



_ALL_VIEWS = dict(ChainMap(
        pisak.main_panel.app.VIEWS,
        pisak.viewer.app.VIEWS,
        pisak.speller.app.VIEWS))


_PISAK_MAIN = {
    "views": _ALL_VIEWS,
    "initial-view": "main_panel/main",
    "initial-data": None
    }


if __name__ == "__main__":
    launcher.run(_PISAK_MAIN)
