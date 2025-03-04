import subprocess
import sys
import traceback

if __name__ == "__main__":
    try:
        subprocess.run(['python', 'main.py'], check=True)
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
        input("Нажмите Enter для выхода...")