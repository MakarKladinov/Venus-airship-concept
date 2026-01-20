"""
Основной файл запуска приложения симуляции входа в атмосферу Венеры
"""

import tkinter as tk
import sys
import os

# Добавить родительскую директорию в путь Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from gui.main_window import SimpleSimulationApp
except ImportError:
    print("Ошибка: Не удалось импортировать SimpleSimulationApp")
    print("Проверьте структуру проекта и пути импорта")
    sys.exit(1)

def main():
    """Главная функция запуска приложения"""
    # Создаем главное окно
    root = tk.Tk()
    root.title("Симуляция входа в атмосферу Венеры")
    
    # Создаем и запускаем приложение
    try:
        app = SimpleSimulationApp(root)
    except Exception as e:
        print(f"Ошибка создания приложения: {e}")
        tk.messagebox.showerror("Ошибка", f"Не удалось создать приложение:\n{e}")
        return
    
    # Центрируем окно на экране
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Запускаем главный цикл
    try:
        root.mainloop()
    except Exception as e:
        print(f"Ошибка в главном цикле: {e}")

if __name__ == "__main__":
    main()