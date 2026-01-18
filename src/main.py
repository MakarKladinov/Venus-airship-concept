import tkinter as tk
from gui import SimulationApp

def main():
    root = tk.Tk()
    root.title("Моделирование входа в атмосферу Венеры")
    window_width = 900
    window_height = 750
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    app = SimulationApp(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
