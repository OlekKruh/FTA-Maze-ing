from typing import Optional


class Menu:
    CMD_GENERATE_NEW = 1
    CMD_SHOW_PATH = 2
    CMD_CHAR_STYLE = 3
    CMD_CHANGE_COLORS = 4
    CMD_EXIT = 5

    def __init__(self):
        self.title = "=== A-MAZE-ING GENERATOR ==="
        self.menu_list = []


    def get_user_choice(self) -> Optional[int, str]:
        while True:
            choice = input("").strip() # глушит stdout.write если добавить в список для вывода

            if choice.isdigit():
                cmd = int(choice)
                if 1 <= cmd <= 5:
                    return cmd
            return str(choice)

    def get_choice(self) -> str:
        return "Choose command: "

    def get_title_text(self) -> str:
        return f"{self.title}"

    def get_generate_btn_text(self) -> str:
        return f"[{self.CMD_GENERATE_NEW}] Generate new maze"

    def get_path_btn_text(self, is_path_visible: bool = False) -> str:
        path_action = "Hide" if is_path_visible else "Show"
        return f"[{self.CMD_SHOW_PATH}] {path_action} path"

    def get_char_style_btn_text(self, char_style: str) -> str:
        return f"[{self.CMD_CHAR_STYLE}] Change characters style. Now: ({char_style})"

    def get_color_style_btn_text(self, color_style: str) -> str:
        return f"[{self.CMD_CHANGE_COLORS}] Change color style. Now: ({color_style})"

    def get_exit_btn_text(self) -> str:
        return f"[{self.CMD_EXIT}] Quit program"

    @staticmethod
    def _show_error(message: str) -> None:
        print(f">>> ERROR: {message} <<<")
