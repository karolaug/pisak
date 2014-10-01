import configobj

class Configurable(object):
    
    __gtype_name__ = False # __gtype_name__ should be overwritten by child
    __gproperties__ = {} # __gproperties__ should be overwritten by child


    def __init__(self, filename):
        self.filename = filename
        self.readConfig()

    def readConfig(self):
        self.config = configobj.ConfigObj(self.filename)

    def applyProp(self, prop, default):
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
                default = self.config["defaults"][self.__gtype_name__][prop]
                setattr(self, prop, self.applyProp(prop, default))
        else:
            raise ValueError("__gproperties__ not overwritten by child.")
            
    
    def writeConfig(self, where):
        self.config.filename = where
        self.config.write()
        

if __name__ == '__main__':
    import os.path
    from pisak import res
    config = Configurable(os.path.join(res.get("configs"), "config.ini"))
    print('{}: {}'.format(group, config.config[group]) for group in config.config.keys())
