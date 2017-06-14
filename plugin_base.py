import abc
import importlib
import inspect

import plugins


class AbstractPluginBase:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def check_pattern(self, message):
        return False

    @abc.abstractmethod
    def handle_message(self, message):
        return ""


class PluginLoader:
    @staticmethod
    def get_all_plugins():
        plugins_classes = []
        # Load all modules
        for module in [importlib.import_module("plugins." + x) for x in plugins.__all__]:
            # Get only subclasses of AbstractPluginBase
            plugins_classes += inspect.getmembers(module, PluginLoader.is_plugin)
        # Return instances of the classes
        return [(x[0], x[1]()) for x in plugins_classes]

    @staticmethod
    def is_plugin(object):
        return inspect.isclass(object) and issubclass(object, AbstractPluginBase) and object is not AbstractPluginBase
