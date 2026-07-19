import tkinter as tk

screen = tk.Tk()
screen.title("test_tkinter")
screen.geometry("400x300")

label = tk.Label(screen, text = "Hello Mom")
label.pack()

screen.mainloop()


