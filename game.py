import tkinter as tk
import time
from PIL import Image, ImageTk
leaderboard = {}
def open_fast_reaction():

    fast_reaction = tk.Toplevel(training_reaction)
    fast_reaction.title('Быстрая реакция')
    fast_reaction.resizable(width=False, height=False)
    fast_reaction.geometry("700x700")
    fast_reaction.iconbitmap('icon1.ico')

    image = Image.open("table.png")
    image = image.resize((int(image.width * 0.95), int(image.height * 0.8)))
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(fast_reaction, image=photo)
    image_label.place(x=10, y=175)
    image_label.image = photo

    def button_click():
        nonlocal start_time
        button.config(bg='blue', command=None)
        start_time = time.time()
        training_reaction.after(1000, lambda: button.config(bg='green', command=button_release))

    def button_release(event):
        nonlocal start_time
        elapsed_time = time.time() - start_time
        if elapsed_time < 1:
            button.config(text='Слишком рано!', bg='blue',
                          command=button_click)
        else:
            elapsed_time = round(elapsed_time - 1, 3)
            button.config(text=f'Время реакции: {elapsed_time} ms')
            if elapsed_time not in leaderboard or elapsed_time < min(leaderboard.keys()):
                leaderboard[elapsed_time] = name_entry.get()
                update_leaderboard()



    def limit_chars(P):
        return len(P) <= 21
        return True
    start_time = None

    button = tk.Button(fast_reaction, text='Тренировка реакции', command=button_click, bg='blue', height=10, width=100)
    button.pack(padx=10, pady=10)
    button.bind('<ButtonRelease-1>', button_release)

    name_label = tk.Label(fast_reaction, text='Напиши свое имя:')
    name_label.place(x=530, y=200)
    chars = (fast_reaction.register(limit_chars), '%P')
    name_chars = tk.StringVar()
    name_entry = tk.Entry(fast_reaction,textvariable=name_chars, validate='key', validatecommand=chars, width=25)
    name_entry.place(x=530, y=250)

    def back_button_click():
        fast_reaction.destroy()

    back_button = tk.Button(fast_reaction, text='Главное меню', command=back_button_click)
    back_button.pack(padx=10, pady=10)
    back_button.place(x=530, y=300)

def save_leaderboard():
    with open('leaderboard.txt', "w") as f:
        for elapsed_time, name in leaderboard.items():
            f.write(f"{name}: {elapsed_time} ms\n")
def update_leaderboard():
    global leaderboard
    leaderboard = {k: v for k, v in sorted(leaderboard.items(), key=lambda item: item[0])[:10]}
    table_text.configure(state='normal')
    table_text.delete('1.0', tk.END)
    for i, (elapsed_time, name) in enumerate(sorted(leaderboard.items(), key=lambda item: item[0]), start=1):
        table_text.insert(tk.END, f"{i}. {name}: {elapsed_time} ms\n")
    table_text.configure(state='disabled')
    save_leaderboard()

    def on_closing():
        save_leaderboard()
        training_reaction.destroy()


    training_reaction.protocol('WM_DELETE_WINDOW', on_closing)



training_reaction = tk.Tk()
training_reaction.title('Training reaction')
training_reaction.resizable(width=False, height=False)
training_reaction.geometry("700x700")
training_reaction.iconbitmap('icon1.ico')


table_label = tk.Label(training_reaction, text='Топ 10 пользователей:')
table_label.place(x=450, y=175)
table_text = tk.Text(training_reaction, height=10, width=30)
table_text.configure(state='normal')
table_text.configure(state='disabled')
table_text.place(x=400, y=200)
blue_button = tk.Button(training_reaction, text='Тренировка реакции', bg='blue', height=10, width=100, state='disabled')
blue_button.place(x=2, y=10)

button = tk.Button(training_reaction, text='Быстрая реакция', command=open_fast_reaction, height=3, width=15)
button.place(x=5, y=200)

training_reaction.mainloop()