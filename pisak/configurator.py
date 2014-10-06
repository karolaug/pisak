import configobj, logging

_LOG = logging.getLoger(__name__)

class Configurable(object):
    
    __gtype_name__ = False # __gtype_name__ should be overwritten by child
    __gproperties__ = {} # __gproperties__ should be overwritten by child

    def __init__(self):
        self.config_path = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config_path):
        self.config_path = config_path
        if self.config_path:
            self._config = configobj.ConfigObj(self.config_path)
        else:
            raise ValueError("No config specified.")

    def getProp(self, prop, default):
        if self.__gtype_name__:
            try:
                return self.config[self.__gtype_name__][prop]
            except KeyError:
                return default
        else:
            raise KeyError("__gtype_name__ not overwritten by child.")

    def applyProps(self):
        try:
            for prop in self.config[self.__gtype_name__].iterkeys():
                default = getattr(self, prop)
                setattr(self, prop, self.getProp(prop, default))
        except AttributeError:
            _LOG.warning("No such {} __gtype_name__ specified in the config."\
                         .format(self.__gtype_name__))
        except KeyError as e:
            raise KeyEror("__gtype_name__ not overwritten by child."\
                          .format(e.args[0]))

    def writeConfig(self, where):
        self.config.filename = where
        self.config.write()
        

if __name__ == '__main__':
    import os.path
    from pisak import res
    config_wrapper = Configurable()
    config_wrapper.config = os.path.join(res.get("configs"), "config.ini")
    print(*('{}: {}'.format(group, config_wrapper.config[group]) for group in config_wrapper.config.keys()), sep='\n')
