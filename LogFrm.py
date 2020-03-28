from tkinter import *
from tkinter.messagebox import showinfo, showerror
import mysql.connector


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master['padx'] = 10
        self.master['pady'] = 10
        self.master.title('Завуч')
        self.master.geometry("260x90")
        self.label_username = Label(self, text="Имя пользователя")
        self.label_password = Label(self, text="Пароль")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=W)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.log_btn = Button(self, text="Войти", command=self.login_click)
        self.log_btn.grid(columnspan=2)

        self.pack()

    def login_click(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        self.con = connect(username, password)
        if self.con:
            showinfo("Вход", "Корректно")
            self.master.destroy()
        else:
            showerror("Ошибка", "Неправильный логин или пароль")


def connect(in_user, in_pass):
    con = 0
    try:
        print('Connecting...')
        con = mysql.connector.connect(host = 'localhost',
        database = 'Course',
        user = in_user,
        password = in_pass)
        if con.is_connected():
            print('Connected to MySQL db')
    except mysql.connector.Error as e:
        print(e)
    finally:
        return con
