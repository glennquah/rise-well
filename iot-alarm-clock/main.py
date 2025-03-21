import tkinter as tk
from tkinter import ttk
from gui.start_window import start_window


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("White.TRadiobutton", background="white", foreground="black")
    rb = ttk.Radiobutton(root, text="Option", variable=tk.StringVar(), value="1", style="White.TRadiobutton")
    start_window(root)
    root.mainloop()



#     from sensors.shake_sensor import shake_game

# def main(): 
#     while True:
#         print("Select game choice: ")
#         print("1. Shake Game")

#         choice = input("Enter: ")

#         if (choice == '1'): 
#             shake_game()
#         else:
#             print("Invalid Choice")

# if __name__ == "__main__":
#     main()