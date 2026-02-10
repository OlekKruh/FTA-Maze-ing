class Menu:
    CMD_EXIT = 0
    CMD_GENERATE_NEW = 1
    CMD_SHOW_PATH = 2
    CMD_CHAR_STYLE = 3
    CMD_CHANGE_COLORS = 4

    def __init__(self):
        self.title = "=== A-MAZE-ING GENERATOR ==="

    def get_user_choice(self, is_path_visible: bool,
                      current_char_style: str,
                      current_color_style: str) -> int:
        while True:
            self._print_menu(is_path_visible,
                               current_char_style,
                               current_color_style)
            choice = input("Choice (0-4): ").strip()

            if choice.isdigit():
                cmd = int(choice)
                if 0 <= cmd <= 4:
                    return cmd
            self._show_error("Unknown command! Please select command from the list.")

    def _print_menu(self, is_path_visible: bool,
                     char_style: str,
                     color_style: str) -> None:
        path_action = "Hide" if is_path_visible else "Show"

        print(f"{self.title}")
        print(f"[{self.CMD_GENERATE_NEW}] Generate new maze")
        print(f"[{self.CMD_SHOW_PATH}] {path_action} path")
        print(f"[{self.CMD_CHAR_STYLE}] Change characters stile"
              f"(Now: {char_style})")
        print(f"[{self.CMD_CHANGE_COLORS}] Change color stile"
              f"(Now: {color_style})")
        print(f"[{self.CMD_EXIT}] Quit program")

    @staticmethod
    def _show_error(message: str) -> None:
        print(f">>> ERROR: {message} <<<")
