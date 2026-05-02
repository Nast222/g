import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import random

class RandomTaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.tasks = {
            "Учёба": ["Прочитать статью", "Решить задачу", "Посмотреть лекцию"],
            "Спорт": ["Сделать зарядку", "Пробежать 1 км", "Отжаться 20 раз"],
            "Работа": ["Написать отчёт", "Провести созвон", "Проверить почту"]
        }
        self.history = []
        self.create_widgets()
        self.load_from_json()

    def create_widgets(self):
        # --- Текущая задача ---
        tk.Label(self.root, text="Ваша задача:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        self.current_task_label = tk.Label(self.root, text="Нажмите 'Сгенерировать'", wraplength=300, justify="center")
        self.current_task_label.grid(row=1, column=0, columnspan=2, pady=10)

        # --- Кнопки действий ---
        gen_btn = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task)
        gen_btn.grid(row=2, column=0, columnspan=2, pady=5)

        add_btn = tk.Button(self.root, text="Добавить новую задачу", command=self.add_new_task)
        add_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # --- Фильтр по типу ---
        tk.Label(self.root, text="Фильтр по типу:").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.filter_var = tk.StringVar(value="Все")
        filter_options = ["Все"] + list(self.tasks.keys())
        filter_menu = ttk.OptionMenu(self.root, self.filter_var, *filter_options, command=self.update_history_listbox)
        filter_menu.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        # --- История задач ---
        history_frame = tk.Frame(self.root)
        history_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        tk.Label(history_frame, text="История задач:", font=("Arial", 10, "bold")).pack()
        
        self.history_listbox = tk.Listbox(history_frame, height=10, width=50)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox.config(yscrollcommand=scrollbar.set)

         # --- Кнопки JSON ---
         save_btn = tk.Button(self.root, text="Сохранить в JSON", command=self.save_to_json)
         save_btn.grid(row=6, column=0, padx=5)

         load_btn = tk.Button(self.root, text="Загрузить из JSON", command=self.load_from_json)
         load_btn.grid(row=6, column=1, padx=5)

    def generate_task(self):
         # Проверка наличия задач
         all_tasks = [task for sublist in self.tasks.values() for task in sublist]
         if not all_tasks:
             messagebox.showwarning("Предупреждение", "Список задач пуст. Добавьте новые задачи.")
             return

         # Выбор случайной задачи
         task_type = random.choice(list(self.tasks.keys()))
         task_text = random.choice(self.tasks[task_type])
         
         # Отображение и добавление в историю
         self.current_task_label.config(text=f"Задача: {task_text} ({task_type})")
         
         self.history.append({"task": task_text, "type": task_type})
         self.update_history_listbox()

    def add_new_task(self):
         # Диалог для ввода новой задачи
         task_text = simpledialog.askstring("Новая задача", "Введите текст задачи:")
         
         if not task_text or task_text.strip() == "":
             messagebox.showerror("Ошибка", "Поле задачи не может быть пустым!")
             return
         
         # Выбор типа задачи
         task_type = simpledialog.askstring("Тип задачи", 
                                            f"Введите тип задачи (доступные: {', '.join(self.tasks.keys())}):",
                                            initialvalue=list(self.tasks.keys())[0])
         
         if not task_type or task_type.strip() == "":
             messagebox.showerror("Ошибка", "Поле типа не может быть пустым!")
             return
         
         task_type = task_type.strip()
         
         if task_type not in self.tasks:
             # Если тип не существует — предлагаем создать его
             if messagebox.askyesno("Новый тип", f"Тип '{task_type}' не найден. Создать новый тип?"):
                 self.tasks[task_type] = []
             else:
                 return
                 
         # Добавление задачи в список
         self.tasks[task_type].append(task_text.strip())
         messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена в категорию '{task_type}'.")

    def update_history_listbox(self, *args):
         # Очистка списка истории
         self.history_listbox.delete(0, tk.END)
         
         # Получение фильтра
         current_filter = self.filter_var.get()
         
         for entry in self.history:
             display_text = f"{entry['task']} ({entry['type']})"
             
             if current_filter == "Все" or entry['type'] == current_filter:
                 self.history_listbox.insert(tk.END, display_text)

    def save_to_json(self):
         data = {
             "tasks": self.tasks,
             "history": self.history
         }
         
         with open('tasks.json', 'w', encoding='utf-8') as f:
             json.dump(data, f, ensure_ascii=False, indent=4)
             
         messagebox.showinfo("Успех", "Данные сохранены в tasks.json")

    def load_from_json(self):
         try:
             with open('tasks.json', 'r', encoding='utf-8') as f:
                 data = json.load(f)
                 
             # Загрузка данных
             self.tasks = data.get("tasks", {})
             self.history = data.get("history", [])
             
             # Обновление интерфейса
             self.update_history_listbox()
             
             # Обновление меню фильтра (если появились новые типы)
             filter_options = ["Все"] + list(self.tasks.keys())
             menu = self.filter_var._root().children['!optionmenu']
             menu['menu'].delete(0, 'end')
             
             for option in filter_options:
                 menu['menu'].add_command(label=option,
                                          command=lambda value=option: self.filter_var.set(value))
             
             messagebox.showinfo("Успех", "Данные загружены из tasks.json")
             
         except FileNotFoundError:
             messagebox.showinfo("Информация", "Файл tasks.json не найден. Будет создан при сохранении.")

if __name__ == "__main__":
     root = tk.Tk()
     app = RandomTaskGeneratorApp(root)
     root.mainloop()
