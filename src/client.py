import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import socket


class ClientApp:
    def __init__(self):
        self.current_server = None
        self.client_socket = None
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.config(bg="black")

        self.server_choice_var = tk.StringVar()
        self.server_choice_var.set("")
        self.result_text = tk.Text(self.root, height=5, width=60, font=("Ariel", 12), fg="green")
        self.result_text.config(bg="black", highlightbackground="gray")
        self.result_text.pack()
        self.create_gui()

    def create_gui(self):
        server_label = tk.Label(self.root, text="Выберите сервер:")
        server_label.config(bg="black", fg="green", font=("Arial", 14))
        server_label.pack()

        server1_button = tk.Button(self.root, text="Сервер 1", command=lambda: self.connect_server(15000, 1))
        server1_button.config(bg="black", fg="green", font=("Arial", 12), activebackground="gray", highlightbackground="green")
        server1_button.pack()

        server2_button = tk.Button(self.root, text="Сервер 2", command=lambda: self.connect_server(16000, 2))
        server2_button.config(bg="black", fg="green", font=("Arial", 12), activebackground="gray", highlightbackground="green")
        server2_button.pack()

        # Listbox для сервера 1
        command_label1 = tk.Label(self.root, text="Выберите команду Сервера 1:")
        command_label1.config(bg="black", fg="green", font=("Arial", 12))
        command_label1.pack(pady=10)
        command_listbox_server1 = tk.Listbox(self.root, width=25, height=5)
        command_listbox_server1.widgetName = "listbox1"
        command_listbox_server1.config(bg="gray")
        command_listbox_server1.pack()

        # Listbox для сервера 2
        command_label2 = tk.Label(self.root, text="Выберите команду Сервера 2:")
        command_label2.config(bg="black", fg="green", font=("Arial", 12))
        command_label2.pack(pady=10)
        command_listbox_server2 = tk.Listbox(self.root, width=25, height=5)
        command_listbox_server2.widgetName = "listbox2"
        command_listbox_server2.config(bg="gray")
        command_listbox_server2.pack()

        # Добавление команд в списки
        commands_server1 = [
            "1. Вывести информацию",
            "2. Изменить название окна"
        ]

        commands_server2 = [
            "1. Размер swap",
            "2. Свободная память swap"
        ]

        for command in commands_server1:
            command_listbox_server1.insert(tk.END, command)

        for command in commands_server2:
            command_listbox_server2.insert(tk.END, command)

        execute_button = tk.Button(self.root, text="Выполнить",
                                   command=lambda: self.execute_command(
                                       command_listbox_server1 if self.current_server == 1
                                       else command_listbox_server2))
        execute_button.config(bg="black", fg="green", font=("Arial", 12), activebackground="gray", highlightbackground="green")
        execute_button.pack(pady=10)

    def connect_server(self, port, server):
        try:
            self.server_choice_var.set(f"Подключено к серверу {port}")
            self.current_server = server

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', port))

            self.client_socket = client_socket
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Подключено к 'Сервер {server}'")
        except:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"'Сервер {server}' не доступен.")

    def execute_command(self, selected_command_listbox):
        if not self.client_socket:
            messagebox.showinfo("Ошибка", "Не выбран сервер. Подключитесь к серверу сначала.")
            return

        selected_index = selected_command_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Ошибка", "Неверная команда.")
            return

        if selected_command_listbox.widgetName == "listbox1":
            if (int(selected_command_listbox.get(selected_index[0]).split('.')[0]) == 1):
                command_number = (selected_command_listbox.get(selected_index[0]).split('.')[0])
            elif (int(selected_command_listbox.get(selected_index[0]).split('.')[0]) == 2):
                new_title = askstring("Input", f"Enter new title for server window.")
                command_number = (selected_command_listbox.get(selected_index[0]).split('.')[0]
                                  + f".{new_title}")
        else:
            command_number = selected_command_listbox.get(selected_index[0]).split('.')[0]

        self.client_socket.send(command_number.encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')

        if response == "req1":
            window_info = f"{self.root.winfo_width()}.{self.root.winfo_height()}"
            self.client_socket.send(window_info.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')

        self.result_text.delete(2.0, tk.END)
        self.result_text.insert(tk.END, f"\n{response}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    client_app = ClientApp()
    client_app.run()
