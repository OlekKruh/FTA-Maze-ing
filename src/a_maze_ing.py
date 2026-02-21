import sys
from pathlib import Path
from mazegen import MazeConfig, Manager

# Путь к папке, где лежит сам скрипт (скорее всего, src/)
BASE_DIR = Path(__file__).resolve().parent


def main():
    if len(sys.argv) != 2:
        print("Error: Invalid number of arguments.")
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    con_file_name = sys.argv[1]

    # Умный поиск файла конфигурации
    cwd_path = Path(con_file_name)
    if cwd_path.is_file():
        # Если файл есть в папке запуска (CWD)
        full_config_path = cwd_path.resolve()
    else:
        # Если нет - ищем рядом со скриптом a_maze_ing.py
        full_config_path = (BASE_DIR / con_file_name).resolve()

    try:
        configs = MazeConfig.load_config(full_config_path)
        app = Manager(configs)
        app.run()

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nCritical Error: An unexpected issue occurred during execution.")
        print(f"Details: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()