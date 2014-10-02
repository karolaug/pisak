import configobj

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
            raise ValueError("__gtype_name__ not overwritten by child.")

    def applyProps(self):
        if self.__gproperties__:
            for prop in self.__gproperties__.keys():
                default = getattr(self, prop)
                setattr(self, prop, self.getProp(prop, default))
        else:
            raise ValueError("__gproperties__ not overwritten by child.")

    def writeConfig(self, where):
        self.config.filename = where
        self.config.write()
        

if __name__ == '__main__':
    import os.path
    from pisak import res
    config_wrapper = Configurable()
    config_wrapper.config = os.path.join(res.get("configs"), "config.ini")
    print(*('{}: {}'.format(group, config_wrapper.config[group]) for group in config_wrapper.config.keys()), sep='\n')
