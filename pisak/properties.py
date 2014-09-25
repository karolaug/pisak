class PropertyAdapter(object):
    """
    Utility class for gobject vs python types of properties conversion.
    Contains gobject obligatory property setter and getter
    """
    def find_attribute(self, name):
        name = self._repair_prop_name(name)
        for relative in self.__class__.mro():
            attribute = relative.__dict__.get(name)
            if attribute:
                break
        return attribute

    @staticmethod
    def _repair_prop_name(name):
        if '-' in name:
            name = name.replace('-', '_')
        return name

    def do_set_property(self, spec, value):
        """
        Introspect object properties and set the value.
        """
        attribute = self.find_attribute(spec.name)
        if attribute is not None and isinstance(attribute, property):
            attribute.fset(self, value)
        else:
            raise ValueError("No such property", spec.name)

    def do_get_property(self, spec):
        """
        Introspect object properties and get the value.
        """
        attribute = self.find_attribute(spec.name)
        if attribute is not None and isinstance(attribute, property):
            return attribute.fget(self)
        else:
            raise ValueError("No such property", spec.name)
