from menu import Menu
from plugin_handler import PluginLoader

if __name__ == "__main__":
    plugin_loader = PluginLoader()
    menu = Menu(plugin_loader)
    menu.run()