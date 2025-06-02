import tkinter as tk
from tkinter import ttk, messagebox

# Veri yapıları
employees = []
shifts = {}
schedule = {}
days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

# Fonksiyonlar
def add_employee():
    name = emp_name_var.get()
    if name and name not in employees:
        employees.append(name)
        schedule[name] = {}
        update_employee_list()
        update_assign_employee_menu()
        emp_name_var.set("")
    else:
        messagebox.showerror("Hata", "Geçersiz veya tekrar eden isim")

def remove_selected_employee():
    selection = emp_listbox.curselection()
    if selection:
        name = emp_listbox.get(selection[0])
        employees.remove(name)
        schedule.pop(name, None)
        update_employee_list()
        update_assign_employee_menu()
        update_schedule_table()

def update_employee_list():
    emp_listbox.delete(0, tk.END)
    for emp in employees:
        emp_listbox.insert(tk.END, emp)

def update_assign_employee_menu():
    emp_assign_menu['values'] = employees

def add_shift():
    name = shift_name_var.get()
    start = start_time_var.get()
    end = end_time_var.get()
    if name and start and end and name not in shifts:
        shifts[name] = (start, end)
        shift_name_var.set("")
        start_time_var.set("")
        end_time_var.set("")
        update_shift_list()
        update_shift_table()
    else:
        messagebox.showerror("Hata", "Geçersiz giriş veya tekrar eden vardiya")

def update_shift_list():
    shift_menu['menu'].delete(0, 'end')
    for name in shifts:
        shift_menu['menu'].add_command(label=name, command=lambda value=name: shift_var.set(value))
    if shifts:
        first_shift = list(shifts.keys())[0]
        shift_var.set(first_shift)

def assign_shift():
    emp = emp_assign_var.get()
    day = day_var.get()
    shift = shift_var.get()
    if emp in employees and shift in shifts and day in days:
        schedule[emp][day] = shift
        update_schedule_table()
    else:
        messagebox.showerror("Hata", "Geçersiz atama bilgisi")

def update_schedule_table():
    for row in schedule_table.get_children():
        schedule_table.delete(row)
    for emp in employees:
        values = []
        for day in days:
            s = schedule[emp].get(day, "-")
            if s in shifts:
                time = f"{s} ({shifts[s][0]}-{shifts[s][1]})"
            else:
                time = "-"
            values.append(time)
        schedule_table.insert("", tk.END, values=[emp] + values)

def update_shift_table():
    for row in shift_table.get_children():
        shift_table.delete(row)
    for name, (start, end) in shifts.items():
        shift_table.insert("", tk.END, values=(name, start, end))

def delete_selected_shift():
    selection = shift_table.selection()
    if selection:
        shift_name = shift_table.item(selection[0], 'values')[0]
        if shift_name in shifts:
            del shifts[shift_name]
            for emp in schedule:
                for day in list(schedule[emp].keys()):
                    if schedule[emp][day] == shift_name:
                        del schedule[emp][day]
            update_shift_list()
            update_shift_table()
            update_schedule_table()

# Arayüz
root = tk.Tk()
root.title("Vardiya Planlayıcı")

# Çalışan Ekleme
frame1 = ttk.LabelFrame(root, text="Çalışan Yönetimi")
frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
emp_name_var = tk.StringVar()
ttk.Entry(frame1, textvariable=emp_name_var).grid(row=0, column=0)
ttk.Button(frame1, text="Ekle", command=add_employee).grid(row=0, column=1)
emp_listbox = tk.Listbox(frame1, height=5)
emp_listbox.grid(row=1, column=0, columnspan=2, pady=5)
ttk.Button(frame1, text="Seçiliyi Sil", command=remove_selected_employee).grid(row=2, column=0, columnspan=2)

# Vardiya Ekleme ve Listeleme
frame2 = ttk.LabelFrame(root, text="Vardiya Tanımlama")
frame2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
shift_name_var = tk.StringVar()
start_time_var = tk.StringVar()
end_time_var = tk.StringVar()
ttk.Entry(frame2, textvariable=shift_name_var, width=10).grid(row=0, column=0)
ttk.Entry(frame2, textvariable=start_time_var, width=10).grid(row=0, column=1)
ttk.Entry(frame2, textvariable=end_time_var, width=10).grid(row=0, column=2)
ttk.Button(frame2, text="Vardiya Ekle", command=add_shift).grid(row=0, column=3)

shift_table = ttk.Treeview(frame2, columns=("Ad", "Başlangıç", "Bitiş"), show="headings", height=5)
for col in ("Ad", "Başlangıç", "Bitiş"):
    shift_table.heading(col, text=col)
shift_table.grid(row=1, column=0, columnspan=4, pady=5)
ttk.Button(frame2, text="Seçiliyi Sil", command=delete_selected_shift).grid(row=2, column=0, columnspan=4)

# Vardiya Atama
frame3 = ttk.LabelFrame(root, text="Vardiya Atama")
frame3.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
emp_assign_var = tk.StringVar()
emp_assign_menu = ttk.Combobox(frame3, textvariable=emp_assign_var, values=employees, state="readonly")
emp_assign_menu.grid(row=0, column=0)
day_var = tk.StringVar(value=days[0])
ttk.Combobox(frame3, textvariable=day_var, values=days, state="readonly").grid(row=0, column=1)
shift_var = tk.StringVar()
shift_menu = ttk.OptionMenu(frame3, shift_var, "")
shift_menu.grid(row=0, column=2)
ttk.Button(frame3, text="Ata", command=assign_shift).grid(row=0, column=3)

# Haftalık Tablo
frame4 = ttk.LabelFrame(root, text="Haftalık Vardiya Tablosu")
frame4.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
schedule_table = ttk.Treeview(frame4, columns=["Çalışan"] + days, show="headings")
schedule_table.heading("Çalışan", text="Çalışan")
for day in days:
    schedule_table.heading(day, text=day)
schedule_table.pack(fill="both", expand=True)

update_employee_list()
update_shift_list()
update_shift_table()
update_assign_employee_menu()

root.mainloop()
