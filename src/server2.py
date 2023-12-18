import socket
import threading
import time
import tkinter as tk
import psutil
import os


def handle_client(client_socket):
    # Обработка запросов от клиента
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        fstring = "%H:%M:%S"
        if request == '1':
            # Команда 1: Вывести размер файла подкачки в байтах
            swap_size = psutil.swap_memory().total
            response = f"Размер файла подкачки: {swap_size} байт ({swap_size/(2**30):.2f} ГБ). Текущее время: {time.strftime(fstring)}"
        elif request == '2':
            # Команда 2: Вывести количество свободных байтов файла подкачки
            free_swap_bytes = psutil.swap_memory().free
            response = f"Свободные байты файла подкачки: {free_swap_bytes} байт ({free_swap_bytes/(2**30):.2f} ГБ). Текущее время: {time.strftime(fstring)}"
        else:
            response = f"Неверная команда. Текущее время: {time.strftime(fstring)}"

        client_socket.send(response.encode('utf-8'))

    client_socket.close()


def exit_gui(window):
    window.destroy()
    os.kill(os.getpid(), 9)


def start_gui():
    server2_window = tk.Tk()
    server2_window.title("Server 2")
    server2_window.geometry("250x50")
    server2_window.config(bg="black")
    server2_label = tk.Label(server2_window, text="Сервер запущен", font=("Arial", 14))
    server2_label.config(bg="black", fg="green")
    server2_label.pack()


    server2_window.protocol("WM_DELETE_WINDOW", server2_window.iconify)
    # make Esc exit the program
    server2_window.bind('<Escape>', lambda e: exit_gui(server2_window))

    # create a menu bar with an Exit command
    menubar = tk.Menu(server2_window)
    menubar.config(bg="gray")
    menubar.add_command(label="Exit", command=lambda e=server2_window: exit_gui(e))
    server2_window.config(menu=menubar)

    server2_window.mainloop()


def server2():
    global server_status

    server_status = False
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 12346))
        server.listen(5)
    except:
        error_window = tk.Tk()
        error_window.title("Server 2")
        error_window.geometry("250x50")
        error_window.config(bg="black")
        error_label = tk.Label(error_window, text="Порт недоступен.", font=("Arial", 12))
        error_label.config(bg="black", fg="green")
        error_label.pack()
        error_window.mainloop()

    print("Server2 запущен с портом 12346")
    server_status = True

    while True:
        client_socket, addr = server.accept()
        print(f"Клиент {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    global server_status
    server_thread = threading.Thread(target=server2)
    server_thread.start()

    time.sleep(1.5)
    if server_status:
        start_gui()
    else:
        exit()
