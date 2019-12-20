from tkinter import Tk, ttk, END
import tkinter as tk
from fpdf import FPDF
import datetime
from LogFrm import LoginFrame
import mysql.connector


def pdf_func_num_stud(str1, str2):
    now = datetime.datetime.now()
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, 'Справка', ln=1, align='C')
    pdf.cell(200, 10, 'о количестве обучающихся Белогубского филлиала', ln=1, align='C')
    pdf.cell(200, 10,
             'Покровской ГБОУ СОШ №51 по состоянию на %d.%d.%d' % (now.day, now.month, now.year),
             ln=1, align='C')
    pdf.cell(200, 50, 'Количество обучающихся в ' + str1 + ' классе: ' + str2, ln=1, align='C')
    pdf.cell(200, 100, 'Директор школы', align='L')
    pdf.output('NumberOfStudents.pdf', 'F')


def pdf_func_report(list1, list2, cabinet_num, class_num, num_stud_class, deuce, avrg, excellent):
    now = datetime.datetime.now()
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, 'Отчета о работе', ln=1, align='C')
    pdf.cell(200, 10,
             'Покровской ГБОУ СОШ №51 по состоянию на %d.%d.%d' % (now.day, now.month, now.year),
             ln=1, align='C')
    pdf.cell(200, 10, 'Количество учителей по предметам:', ln=1, align='L')
    for i in range(len(list1)):
        pdf.cell(200, 10, list1[i] + ': ' + list2[i], ln=1, align='L')
    pdf.cell(200, 10, 'Количество кабинетов: ' + cabinet_num, ln=1, align='L')
    pdf.cell(200, 10, 'Число учеников в каждом классе:', ln=1, align='L')
    for i in range(len(class_num)):
        pdf.cell(200, 10, class_num[i] + ': ' + num_stud_class[i], ln=1, align='L')
    pdf.cell(200, 10, 'Число двоечников: ' + deuce, ln=1, align='L')
    pdf.cell(200, 10, 'Число хорошистов: ' + avrg, ln=1, align='L')
    pdf.cell(200, 10, 'Число отличников: ' + excellent, ln=1, align='L')
    pdf.cell(200, 1, 'Директор школы', align='L')
    pdf.output('SchoolPerformanceReport.pdf', 'F')


class TabClass(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.pack(fill=tk.BOTH, expand=1)
        acts = []
        cursor.execute('select distinct №класса from Расписание\
                        order by №класса;')
        row = cursor.fetchone()
        while row is not None:
            acts.append(str(row)[2:-3])
            row = cursor.fetchone()
        self.text1 = tk.Text(self, height=23, width=30)
        self.text1.pack(side='right')
        self.lb = tk.Listbox(self, height=20, width=30)
        for i in acts:
            self.lb.insert(END, i)
            self.lb.bind("<<ListboxSelect>>", self.on_select)
            self.lb.pack(pady=15, side='left')

        self.var = tk.StringVar()
        self.label = tk.Label(self, text=0, textvariable=self.var)
        self.label.pack()

        self.pack()

    def on_select(self, val):
        self.text1.delete('1.0', tk.END)
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)
        self.var.set(value)
        cursor.execute('select Учителя.ФИО ' + \
                       'from (Расписание ' + \
                       'INNER JOIN Учителя ON Расписание.idУчителя=Учителя.idУчителя) ' + \
                       "where Расписание.№класса = '" + str(value) + "';")
        row = cursor.fetchone()
        while row is not None:
            self.text1.insert(1.0, str(row)[2:-3] + '\n')
            row = cursor.fetchone()


class TabSubj(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.lbl_class = tk.Label(self, text='Класс:', font=('Time New Romain', 12))
        self.lbl_class.grid(row=0, column=0)

        self.entr = tk.Entry(self)
        self.entr.grid(row=0, column=1)

        self.lbl_class = tk.Label(self, text='День недели:', font=('Time New Romain', 12))
        self.lbl_class.grid(row=1, column=0)

        self.combo = ttk.Combobox(self)
        self.combo['values'] = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб')
        self.combo.current(1)
        self.combo.grid(row=1, column=1)

        self.lbl_num = tk.Label(self, text='Номер урока:', font=('Time New Romain', 12))
        self.lbl_num.grid(row=2, column=0)

        self.entr_num = tk.Entry(self)
        self.entr_num.grid(row=2, column=1)

        self.button = tk.Button(self, text='Подтвердить', command=self.on_click)
        self.button.grid(row=1, column=3)

        self.lbl_text = tk.Label(self, text='', font=('Time New Romain', 14))
        self.lbl_text.grid(row=1, column=5)

        self.lbl_text2 = tk.Label(self, text='', font=('Time New Romain', 14))
        self.lbl_text2.grid(row=2, column=5)

        self.pack()

    def on_click(self):
        try:
            cursor.execute('SELECT Предметы.Название ' + \
                           'FROM ((Расписание ' + \
                           'INNER JOIN Предметы ON Расписание.idПредмета=Предметы.idПредметы) ' + \
                           'INNER JOIN Учителя ON Расписание.idУчителя=Учителя.idУчителя) ' + \
                           "where Расписание.№класса='" + str(self.entr.get()) + \
                           "' and Расписание.ДеньНедели='" + str(self.combo.get()) + \
                           "' and Расписание.№урока=" + str(self.entr_num.get()) + ";")
            row = cursor.fetchone()
            self.lbl_text.configure(text=str(row)[2:-3])
            cursor.execute('SELECT Расписание.№кабинета ' + \
                           'FROM ((Расписание ' + \
                           'INNER JOIN Предметы ON Расписание.idПредмета=Предметы.idПредметы) ' + \
                           'INNER JOIN Учителя ON Расписание.idУчителя=Учителя.idУчителя) ' + \
                           "where Расписание.№урока= " + \
                           str(self.entr_num.get()) + " and Расписание.№класса='" + str(self.entr.get()) + \
                           "' and Расписание.ДеньНедели='" + str(self.combo.get()) + "';")
            row = cursor.fetchone()
            self.lbl_text2.configure(text='Кабинет №' + str(row)[1:-2])
        except:
            self.lbl_text.configure(text='Нет урока')


class TabSchedule(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.lbl_class_d = tk.Label(self, text='День недели:', font=('Time New Romain', 12))
        self.lbl_class_d.grid(row=0, column=0)

        self.combo_d = ttk.Combobox(self)
        self.combo_d['values'] = ('Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб')
        self.combo_d.current(1)
        self.combo_d.grid(row=0, column=1)

        self.lbl_class_d = tk.Label(self, text='Класс:', font=('Time New Romain', 12))
        self.lbl_class_d.grid(row=2, column=0)

        self.entr_d = tk.Entry(self)
        self.entr_d.grid(row=2, column=1)

        self.button_d = tk.Button(self, text='Подтвердить', command=self.on_click)
        self.button_d.grid(row=3, column=1)

        self.text_d = tk.Text(self, height=23, width=30)
        self.text_d.grid(row=4, column=6)

        self.pack()

    def on_click(self):
        try:
            cursor.execute('SELECT Расписание.№урока, Предметы.Название, Расписание.№кабинета,' + \
                           "time_format(Расписание.Время, '%k:%i') " + \
                           'FROM ((Расписание ' + \
                           'INNER JOIN Предметы ON Расписание.idПредмета=Предметы.idПредметы) ' + \
                           'INNER JOIN Учителя ON Расписание.idУчителя=Учителя.idУчителя) ' + \
                           "where  Расписание.ДеньНедели = '" + str(self.combo_d.get()) + "' and " + \
                           "Расписание.№класса = '" + str(self.entr_d.get()) + "' order by Расписание.№урока DESC;")
            row = cursor.fetchone()
            while row is not None:
                inp = str(row).replace('(', '')
                inp = inp.replace(')', '')
                inp = inp.replace("'", '')
                self.text_d.insert(1.0, inp + '\n')
                row = cursor.fetchone()
        except:
            self.text_d.configure(text='Нет урока')


class TabChange(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.lbl_chng = tk.Label(self, text='Изменения:', font=('Time New Romain', 12))
        self.lbl_chng.grid(row=0, column=0)

        self.combo_chng = ttk.Combobox(self, width=36)
        self.combo_chng['values'] = ('Внести информацию о новом учителе',
                                     'Удалить запись об ученике',
                                     'Изменить оценку ученику')
        self.combo_chng.current(0)
        self.combo_chng.grid(row=0, column=1)

        self.button_chng = tk.Button(self, text='Подтвердить', command=self.on_click)
        self.button_chng.grid(row=1, column=1)

        self.text_chng = tk.Text(self, height=23, width=50)
        self.text_chng.grid(row=4, column=0, columnspan=3)

        self.pack()

    def on_click(self):
        try:
            command = str(self.text_chng.get('1.0', END)).strip().split(', ')
            if self.combo_chng.get() == 'Внести информацию о новом учителе':
                cursor.execute(
                "insert into Учителя value(" + command[0] + ", '" + command[1] + "', " + command[2] + ");")
                con.commit()
                self.text_chng.insert(2.2, ' информация внесена.')
            elif self.combo_chng.get() == 'Удалить запись об ученике':
                cursor.execute("delete from Ученики where ФИ = '" + command[0] + "';")
                con.commit()
                self.text_chng.insert(2.2, ' ученик удален.')
            elif self.combo_chng.get() == 'Изменить оценку ученику':
                cursor.execute("select idУченики from Ученики where ФИ = '" + command[1] + "';")
                command[1] = str(cursor.fetchone()).replace('(', '').replace(',)', '')
                cursor.execute("select idПредметы from Предметы where Название = '" + command[2] + "';")
                command[2] = str(cursor.fetchone()).replace('(', '').replace(',)', '')
                cursor.execute("update Журнал set Оценка = " + command[0] + " where idУченика = " + command[1]
                               + " and idПредметы =" + command[2] + ";")
                con.commit()
                self.text_chng.insert(2.2, ' успешно.')

        except mysql.connector.Error:
            self.text_chng.insert(2.2, ' ошибка')


class TabReference(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.lbl_reference = tk.Label(self, text='Справка:', font=('Time New Romain', 12))
        self.lbl_reference.grid(row=0, column=0)

        self.combo_reference = ttk.Combobox(self, width=40)
        self.combo_reference['values'] = ('о количестве учеников в данном классе',
                                          'отчет о работе школы')
        self.combo_reference.current(0)
        self.combo_reference.grid(row=0, column=1)

        self.entr_reference = tk.Entry(self)
        self.entr_reference.grid(row=1, column=0)

        self.button_reference = tk.Button(self, text='Подтвердить', command=self.on_click)
        self.button_reference.grid(row=2, column=0)

        self.lbl_txt_reference = tk.Label(self, text='', font=('Time New Romain', 14))
        self.lbl_txt_reference.grid(row=3, column=1)

        self.pack()

    def on_click(self):
        try:
            if self.combo_reference.get() == 'о количестве учеников в данном классе':
                cursor.execute(
                    "SELECT COUNT(№класса) FROM Ученики WHERE №класса='" + str(self.entr_reference.get()) + "';")
                row = cursor.fetchone()
                self.lbl_txt_reference.configure(text="Количество учеников в " + str(self.entr_reference.get()) + \
                                                      " классе: " + str(row)[1:-2])
                pdf_func_num_stud(str(self.entr_reference.get()), str(row)[1:-2])
            elif self.combo_reference.get() == 'отчет о работе школы':
                string = []
                num = []
                num_teach = []
                class_num = []
                num_stud_class = []
                cursor.execute("select idПредметы, Название from Предметы order by idПредметы;")
                row = cursor.fetchone()
                while row is not None:
                    string.append(str(row)[4:-2].replace("'", ''))
                    num.append(str(row)[1])
                    row = cursor.fetchone()
                for i in num:
                    cursor.execute("SELECT COUNT(idУчителя) " + \
                                   "FROM Расписание " + \
                                   "where idПредмета = " + i + ";")
                    row = cursor.fetchone()
                    num_teach.append(str(row)[1])
                cursor.execute("SELECT COUNT(DISTINCT №кабинета) FROM Учителя;")
                row = cursor.fetchone()
                cabinet_num = str(row).replace("(", "").replace(",)", "")
                cursor.execute("SELECT DISTINCT №класса FROM Ученики order by №класса;")
                row = cursor.fetchone()
                while row is not None:
                    class_num.append(str(row).replace("('", '').replace("',)", ""))
                    row = cursor.fetchone()
                for i in class_num:
                    cursor.execute("SELECT COUNT(idУченики) FROM Ученики where №класса = '" + i + "';")
                    row = cursor.fetchone()
                    num_stud_class.append(str(row).replace("(", '').replace(",)", ""))
                cursor.execute("SELECT distinct COUNT(idУченика) FROM Журнал where Оценка = 2;")
                row = cursor.fetchone()
                deuce = str(row).replace('(', '').replace(',)', '')
                cursor.execute("SELECT distinct COUNT(idУченика) FROM Журнал where Оценка <> 5 and Оценка <> 2;")
                row = cursor.fetchone()
                avrg = str(row).replace('(', '').replace(',)', '')
                cursor.execute("SELECT distinct COUNT(idУченика) FROM Журнал where Оценка = 5;")
                row = cursor.fetchone()
                excellent = str(row).replace('(', '').replace(',)', '')
                pdf_func_report(string, num_teach, cabinet_num, class_num, num_stud_class, deuce, avrg, excellent)
        except:
            self.lbl_txt_reference.configure('Ошибка')


class TabTeacher(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.lbl_subj = tk.Label(self, text='Предмет:', font=('Time New Romain', 12))
        self.lbl_subj.grid(row=0, column=0)

        self.entr_subj = tk.Entry(self)
        self.entr_subj.grid(row=0, column=1)

        self.lbl_name = tk.Label(self, text='ФИО учителя:', font=('Time New Romain', 12))
        self.lbl_name.grid(row=1, column=0)

        self.entr_name = tk.Entry(self, width=25)
        self.entr_name.grid(row=1, column=1)

        self.button = tk.Button(self, text='Подтвердить', command=self.on_click)
        self.button.grid(row=2, column=0)

        self.lbl_text = tk.Label(self, text='', font=('Time New Romain', 14))
        self.lbl_text.grid(row=3, column=3)

        self.pack()

    def on_click(self):
        try:
            string = ''
            cursor.execute("SELECT Расписание.№класса " + \
                           "FROM ((Расписание " + \
                           "INNER JOIN Предметы ON Расписание.idПредмета=Предметы.idПредметы) " + \
                           "INNER JOIN Учителя ON Расписание.idУчителя=Учителя.idУчителя) " + \
                           "where Предметы.Название='"+str(self.entr_subj.get())+"' and " +\
                           "Учителя.ФИО='"+str(self.entr_name.get())+"';")
            row = cursor.fetchone()
            while row is not None:
                string += str(row)
                row = cursor.fetchone()
            self.lbl_text.configure(text=string.replace("('", "").replace("',)", " "))
        except:
            self.lbl_text.configure(text='Нет урока')


class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.parent.title('Завуч')

        self.init_ui()

    def init_ui(self):
        self.parent['padx'] = 10
        self.parent['pady'] = 10
        self.notebook = ttk.Notebook(self, width=1000, height=700)

        class_tab = TabClass(self.notebook)
        subj_tab = TabSubj(self.notebook)
        schedule_tab = TabSchedule(self.notebook)
        change_tab = TabChange(self.notebook)
        reference_tab = TabReference(self.notebook)
        teacher_tab = TabTeacher(self.notebook)

        self.notebook.add(class_tab, text="Классы")
        self.notebook.add(subj_tab, text="Предмет")
        self.notebook.add(teacher_tab, text="Учителя")
        self.notebook.add(schedule_tab, text="Расписание")
        self.notebook.add(change_tab, text="Изменения")
        self.notebook.add(reference_tab, text='Справки')
        self.notebook.pack()
        self.pack()


login = Tk()
lf = LoginFrame(login)
login.mainloop()
con = lf.con
cursor = con.cursor()
root = Tk()
root.title('Завуч')
ex = MainWindow(root)
root.geometry("640x400")
root.mainloop()
con.close()
print('Connection close.')
