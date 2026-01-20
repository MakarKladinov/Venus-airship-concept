
"""
Пакет gui - графический интерфейс пользователя
"""

try:
    from .main_window import SimpleSimulationApp
    from .results_window import SimpleResultsWindow
    __all__ = ['SimpleSimulationApp', 'SimpleResultsWindow']
except ImportError as e:
    print(f"Ошибка импорта в gui: {e}")
    __all__ = []