import tkinter as tk
import time
import random
from PIL import Image, ImageTk


# A dictionary to store the top elapsed times and corresponding names
leaderboard = {}
def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Быстрая реакция")
    new_window.resizable(width=False, height=False)
    new_window.geometry("700x700")
    # Load the image
    image = Image.open("table.png")
    image = image.resize((int(image.width * 0.95), int(image.height * 0.8)))
    photo = ImageTk.PhotoImage(image)
    # Create a Label widget to display the image
    image_label = tk.Label(new_window, image=photo)
    image_label.place(x=10, y=175)  # adjust the position as needed
    # Keep a reference to the image to prevent it from being garbage collected
    image_label.image = photo

    def button_click():
        nonlocal start_time
        button.config(bg='blue', command=None)  # Изменить цвет кнопки на красный и отключить команду
        start_time = time.time()
        root.after(1000, lambda: button.config(bg='green', command=button_release))

    def button_release(event):
        nonlocal start_time
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            button.config(text='Слишком рано!', bg='blue',
                          command=button_click)  # Сбросить таймер, изменить текст и цвет кнопки на синий
        else:
            elapsed_time = round(elapsed_time - 1, 3)
            button.config(text=f'Время реакции: {elapsed_time} ms')
            # Update the leaderboard if the elapsed time is better than any existing time
            if elapsed_time not in leaderboard or elapsed_time < min(leaderboard.keys()):
                leaderboard[elapsed_time] = name_entry.get()
                update_leaderboard()

    start_time = None
    button = tk.Button(new_window, text="Тренировка реакции", command=button_click, bg='blue', height=10, width=100)
    button.pack(padx=10, pady=10)
    button.bind('<ButtonRelease-1>', button_release)

    # A Label and Entry widget to input the name
    name_label = tk.Label(new_window, text="Напиши свое имя:")
    name_label.place(x=530, y=200)
    name_entry = tk.Entry(new_window, width=25)
    name_entry.place(x=530, y=250)

    def back_button_click():
        new_window.destroy()

    back_button = tk.Button(new_window, text="Главное меню", command=back_button_click)
    back_button.pack(padx=10, pady=10)
    back_button.place(x=530, y=300)

def save_leaderboard():
    with open("leaderboard.txt", "w") as f:
        for elapsed_time, name in leaderboard.items():
            f.write(f"{name}: {elapsed_time} ms\n")
def update_leaderboard():
    # Update the leaderboard dictionary with the latest top elapsed times
    global leaderboard
    leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[0])}

    # Update the leaderboard table in the root window
    table_text.delete('1.0', tk.END)
    for i, (elapsed_time, name) in enumerate(sorted(leaderboard.items(), key=lambda item: item[0]), start=1):
        table_text.insert(tk.END, f"{i}. {name}: {elapsed_time} ms\n")
        # Save the leaderboard data to a text file
        save_leaderboard()

    def on_closing():
        save_leaderboard()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)



root = tk.Tk()
root.title("Training reaction")
root.resizable(width=False, height=False)
root.geometry("700x700")



# A Label and Text widget to display the leaderboard table
table_label = tk.Label(root, text="Топ 10 пользователей:")
table_label.place(x=450, y=175)
table_text = tk.Text(root, height=10, width=30)
table_text.place(x=400, y=200)

# A blue button with the text "Training reaction"
blue_button = tk.Button(root, text="Тренировка реакции", bg='blue', height=10, width=100, state='disabled')
blue_button.place(x=2, y=10)

button = tk.Button(root, text="Быстрая реакция", command=open_new_window, height=3, width=15)
button.place(x=5, y=200)

root.mainloop()