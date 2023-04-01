import sys
from functools import partial
from simple_term_menu import TerminalMenu
from typing import Callable
from pygments import formatters, highlight, lexers
from pathlib import Path

class Menu:
    def __init__(self, plugin_loader):
        self.title = "Pykit v[0.0.1]\n"
        self.plugin_loader = plugin_loader
        self.menu = {
            'plugins':plugin_loader.plugins
        }
        self.current_menu = self.menu
        self.current_menu_path = [] # absolute path of currently viewed menu
        self.directory_title = 'Location: '

    def run(self):
        while True:
            if self.current_menu_path:
                current_location = f"{'/'.join(self.current_menu_path)}"
                self.current_menu['../'] = partial(self.back)
            else:
                current_location = ""
            terminal_menu = self.create_menu(current_location)
            selection_index = terminal_menu.show()
            selection = list(self.current_menu.keys())[selection_index]
            self.option_selected(selection)

    def create_menu(self, current_location):
        return TerminalMenu(
                self.current_menu,
                title=self.title+f"\n{self.directory_title} [Pykit/{current_location}]\n",
                status_bar="\n[Folder Preview]",
                menu_cursor='* ',
                clear_screen=True,
                preview_command=self.preview_command(current_location),
                cycle_cursor=True,
                preview_border=False,
                menu_highlight_style=('bold','bold')
            )

    def preview_command(self, location):
        ignore_files = f" -I {'|'.join(self.plugin_loader.excluded_names)} -L 1"
        if location:
            command = "tree "+ f"{location}/" + "{}" + ignore_files
        else:
            command = "tree {}" + ignore_files
        return command

    def back(self):
        self.current_menu_path.pop()
        self._traverse_menu(selection=None)


    def option_selected(self, selection: str | Callable=None) -> None:
        # if the selection is a sub menu
        if isinstance(self.current_menu[selection], dict):
            # update the menu accordingly
            self._traverse_menu(selection)
        # if it was a function
        elif isinstance(self.current_menu[selection], Callable):
            # run it
            self.current_menu[selection]()
        # Return selection path of current menu


    def _traverse_menu(self, selection:str=None) -> None:
        """
        Navigates through the menu recursively to find the selected option.
        
        arguments [selection: str] 
        returns self.current_menu_path: list[str]
        """
        if selection: selection = selection.lower()
        if selection in self.current_menu.keys():    
            # append user selection to menu path
            self.current_menu_path.append(selection)
        # resent currently known menu path, 
        self.current_menu = self.menu
        # update current menu iteratively using selection path to the
        #   users choice.
        for selection in self.current_menu_path:
            self.current_menu = self.current_menu[selection]