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
    are_plugins_loaded = False
    cached_plugins = []
    modules = []
    @staticmethod
    def get_all_plugins(force=False):
        if not PluginLoader.are_plugins_loaded or force:
            importlib.reload(plugins)
            plugins_classes = []
            PluginLoader.modules = [importlib.import_module("plugins." + x) for x in plugins.__all__]

            # Load all modules
            for module in PluginLoader.modules:
                # Reload all modules(this is needed for reload_plugins to work properly)
                importlib.reload(module)
                # Get only subclasses of AbstractPluginBase
                plugins_classes += inspect.getmembers(module, PluginLoader.is_plugin)
                del module
            # Return instances of the classes
            PluginLoader.cached_plugins = [(x[0], x[1]()) for x in plugins_classes]
            PluginLoader.are_plugins_loaded = True

        return PluginLoader.cached_plugins

    @staticmethod
    def reload_plugins():
        print("Reloading plugins")
        PluginLoader.get_all_plugins(force=True)

    @staticmethod
    def is_plugin(object):
        return inspect.isclass(object) and issubclass(object, AbstractPluginBase) and object is not AbstractPluginBase
