App developer guide
===================

Most basic Pisak applications consist of:

- one or more JSON files
- python module with app descriptor.

JSON files contain declarative description of application views. Python module
uses launcher module to set up view transitions and acts as app's executable.
This guide will show how to create a simple Pisak application.

App descriptor
--------------

App descriptor is simply a containing paths to JSON files, callbacks and other
data needed to launch an application. Here is description of necessary
entries and their keys:

views
    Dictionary of all views available in an application.
    
    For each view there should be an entry where view name is the key and
    value is a pair of a path to JSON file and a callback function. Callback
    functions are used to prepare view after loading it and they are described
    below.
    
initial-view
    Name of view shown when the application starts.
    
initial-data
    Value passed to callback when preparing view.


Callback functions are called each time a view is loaded. Their purpose is to
connect a standalone view with the rest of the application. Each such function
should have a folowing signature::

    def prepare_view_1(stage, script, data):

Where stage is a reference to the default stage, script is ClutterScript
object with loaded JSON file and data is an arbitraty value passed from view
loader.

Here is an example of app descriptor::

    EXAMPLE_APP = {
        "views": {
            "view_1": ("view_1.json", prepare_view_1),
            "view_2": ("view_2.json", prepare_view_2))
        },
        "initial-view": "view_1",
        "initial-data": None
    }
    
It declares 2 views: `view_1` and `view_2`, View named `view_1` is the initial
one and it is prepared by sending `None` value to `prepare_view_1` function.
After loading `view_2` it will be prepared by calling `prepare_view_2`
function. 


JSON views
----------

JSON views are simply scripts loaded by ClutterScript with some additional
capabilities. Each view should have an object with id "main". After
loading a script its main object is added as a child to the application stage.


What next?
----------
- `Useful widgets`_
- `Switch and groups`_
- Connect `signal handlers`_
