import os
import socket
import threading
import time
import tkinter as tk


def handle_client(client_socket):
    global window_width, window_height, server1_window
    # Обработка запросов от клиента
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        fstring = "%H:%M:%S"
        if request.split(".")[0] == '1':
            # Команда 1: Вывести ширину и высоту рамки окна
            server_request = "req1"
            client_socket.send(server_request.encode('utf-8'))
            window_size = client_socket.recv(1024).decode('utf-8')
            window_width = window_size.split(".")[0]
            window_height = window_size.split(".")[1]

            response = f"Ширина окна: {window_width}, Высота окна: {window_height}. Текущее время: {time.strftime(fstring)}"
        elif request.startswith('2'):
            # Команда 2: Изменить название окна
            new_title = request.split(".")[1]
            try:
                server1_window.title(new_title)
                response = f"Название окна успешно изменено. Текущее время: {time.strftime(fstring)}"
            except:
                response = f"Ошибка при смене имени окна. Текущее время: {time.strftime(fstring)}"

        else:
            response = "Неверная команда"

        client_socket.send(response.encode('utf-8'))

    client_socket.close()


def exit_gui(window):
    window.destroy()
    os.kill(os.getpid(), 9)


def start_gui():
    global server1_window, connected_clients

    server1_window = tk.Tk()
    server1_window.title("Server 1")
    server1_window.geometry("250x50")
    server1_window.config(bg="black")
    server1_label = tk.Label(server1_window, text=f"Сервер запущен", font=("Arial", 14))
    server1_label.config(bg="black", fg="green")
    server1_label.pack()

    server1_window.protocol("WM_DELETE_WINDOW", server1_window.iconify)
    # make Esc exit the program
    server1_window.bind('<Escape>', lambda e: exit_gui(server1_window))

    # create a menu bar with an Exit command
    menubar = tk.Menu(server1_window)
    menubar.config(bg="gray")
    menubar.add_command(label="Exit", command=lambda e=server1_window: exit_gui(e))
    server1_window.config(menu=menubar)

    server1_window.mainloop()


def server1():
    global server_status

    server_status = False
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('localhost', 12345))
        server.listen(5)
    except:
        error_window = tk.Tk()
        error_window.title("Server 1")
        error_window.geometry("250x50")
        error_window.config(bg="black")
        error_label = tk.Label(error_window, text="Порт недоступен.", font=("Arial", 12))
        error_label.config(bg="black", fg="green")
        error_label.pack()
        error_window.mainloop()

    print("Server1 запущен с портом 12345")
    server_status = True

    while True:
        client_socket, addr = server.accept()
        print(f"Клиент {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    global server_status

    server_thread = threading.Thread(target=server1)
    server_thread.start()

    time.sleep(1.5)
    if server_status:
        start_gui()
    else:
        exit()