"""
Manages the text content and user input for the application menu.
"""

from typing import List, Union


class Menu:
    """Handles the definitions of menu items and user interaction logic.

    This class serves as a text repository for the UI. It generates the
    formatted strings for menu options based on the application's current state
    (e.g., toggling "Show/Hide Path" text) and processes raw user input
    into command IDs.

    Attributes:
        title (str): The main title of the application.
        menu_list (List[str]): Caches the current list of menu strings.
    """
    CMD_GENERATE_NEW: int = 1
    CMD_SHOW_PATH: int = 2
    CMD_CHAR_STYLE: int = 3
    CMD_CHANGE_COLORS: int = 4
    CMD_CHANGE_GENERATOR: int = 5
    CMD_EXIT: int = 6

    def __init__(self) -> None:
        """Initializes the Menu instance."""
        self.title: str = "=== A-MAZE-ING GENERATOR ==="
        self.menu_list: List[str] = []

    @staticmethod
    def get_user_choice() -> Union[int, str]:
        """Reads and parses the user's input from the console.

        Attempts to convert the input into a command ID (int).
        If the input is a number within the valid range of commands (1-6),
        it returns the integer. Otherwise, it returns the raw string.

        Returns:
            Union[int, str]: The command ID if valid, or the raw input string.
        """
        choice: str = input("").strip()
        if choice.isdigit():
            cmd: int = int(choice)
            # Check if the number corresponds to a known command constant
            if 1 <= cmd <= 6:
                return cmd
        return str(choice)

    @staticmethod
    def get_choice() -> str:
        """Returns the prompt string for the user input line."""
        return "Choose command: "

    def get_title_text(self) -> str:
        """Returns the main title of the application."""
        return f"{self.title}"

    def get_generate_btn_text(self) -> str:
        """Returns the text for the 'Generate New Maze' option."""
        return f"[{self.CMD_GENERATE_NEW}] Generate new maze"

    def get_path_btn_text(self, is_path_visible: bool = False) -> str:
        """Returns the text for the 'Show/Hide Path' option.

        Args:
            is_path_visible (bool): Current visibility state of the solution.

        Returns:
            str: Dynamic text (e.g., "Show path" or "Hide path").
        """
        path_action: str = "Hide" if is_path_visible else "Show"
        return f"[{self.CMD_SHOW_PATH}] {path_action} path"

    def get_char_style_btn_text(self, char_style: str) -> str:
        """Returns the text for changing character styles (ASCII/Unicode)."""
        return (f"[{self.CMD_CHAR_STYLE}] "
                f"Change characters style. Now: ({char_style})")

    def get_color_style_btn_text(self, color_style: str) -> str:
        """Returns the text for changing color themes."""
        return (f"[{self.CMD_CHANGE_COLORS}] "
                f"Change color style. Now: ({color_style})")

    def get_generator_btn_text(self, gen_name: str) -> str:
        """Returns the text for changing the generator algorithm."""
        return (f"[{self.CMD_CHANGE_GENERATOR}] "
                f"Change generator. Now: ({gen_name})")

    def get_exit_btn_text(self) -> str:
        """Returns the text for the exit option."""
        return f"[{self.CMD_EXIT}] Quit program"

    def get_current_list(self, path_visible: bool,
                         char_style: str, color_style: str,
                         gen_name: str) -> List[str]:
        """Compiles the full list of menu lines based on current state.

        Args:
            path_visible (bool): Whether the path is currently shown.
            char_style (str): The name of the current character set.
            color_style (str): The name of the current color theme.
            gen_name (str): The name of the active generator algorithm.

        Returns:
            List[str]: A list of strings, where each string is a line
            to be rendered in the menu section.
        """
        self.menu_list = [
            self.get_title_text(),
            self.get_generate_btn_text(),
            self.get_path_btn_text(path_visible),
            self.get_char_style_btn_text(char_style),
            self.get_color_style_btn_text(color_style),
            self.get_generator_btn_text(gen_name),
            self.get_exit_btn_text(),
            self.get_choice(),
        ]
        return self.menu_list

    @staticmethod
    def _show_error(message: str) -> None:
        """Prints a standardized error message to the console."""
        print(f">>> ERROR: {message} <<<")
