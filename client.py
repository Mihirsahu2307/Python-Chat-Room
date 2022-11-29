# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 33

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

username = ""


def add_message(message, name):
    if name in boxes.keys():
        boxes[name].config(state=tk.NORMAL)
        boxes[name].insert(tk.END, message + '\n')
        boxes[name].config(state=tk.DISABLED)


def connect():
    global username
    username = username_box.get()
    print(username)

    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print("Unable to connect to the server")

    try:
        client.sendall(username.encode())
    except:
        print("COULD NOT SEND NAME")

    names_list = []
    while 1:

        message = client.recv(2048).decode('utf-8')  # getting the names list from the server

        if message == '':
            print("No users registered as of now")
        else:
            names_list = message[1:].split('~')

        break

    # chat list configuration

    root.configure(background=MEDIUM_GREY)

    for i in range(6):
        root.grid_rowconfigure(i + 1, weight=1)

    for i in range(len(names_list)):
        name_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
        name_frame.grid(row=i + 1, column=0, sticky=tk.NSEW)

        name_label = tk.Label(name_frame, text=names_list[i], font=FONT, bg=DARK_GREY, fg=WHITE)
        name_label.pack(side=tk.LEFT, padx=10)

        name_button = tk.Button(name_frame, text="Chat", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                                command=lambda person=names_list[i]: chat(person))
        name_button.pack(side=tk.LEFT, padx=15)

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()


def send_message(textbox, person):
    message = person + '~' + textbox.get()
    if textbox.get() != '':
        client.sendall(message.encode())
        textbox.delete(0, len(message))
    else:
        print("Empty message", "Message cannot be empty")


boxes = {}


def chat(person):
    window = tk.Toplevel()
    window.geometry("600x600")
    window.title(person)
    window.resizable(False, False)

    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=4)
    window.grid_rowconfigure(2, weight=1)

    top_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    top_frame.grid(row=0, column=0, sticky=tk.NSEW)

    middle_frame = tk.Frame(window, width=600, height=400, bg=MEDIUM_GREY)
    middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

    bottom_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

    username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
    username_label.pack(side=tk.LEFT, padx=10)

    username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
    username_textbox.pack(side=tk.LEFT)

    username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
    username_button.pack(side=tk.LEFT, padx=15)

    message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
    message_textbox.pack(side=tk.LEFT, padx=10)

    message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                               command=lambda textbox=message_textbox, user=person: send_message(textbox, user))
    message_button.pack(side=tk.LEFT, padx=10)

    message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67,
                                            height=26.5)
    message_box.config(state=tk.DISABLED)
    message_box.pack(side=tk.TOP)

    boxes[person] = message_box

    client.sendall(('?' + person).encode()) # to ask for chat history with a person


# configuring the temporary opening screen

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
main_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
main_frame.grid(row=0, column=0, sticky=tk.NSEW)

username_box = tk.Entry(main_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=30)
username_box.pack(side=tk.LEFT, padx=10)

start_button = tk.Button(main_frame, text="START", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
start_button.pack(side=tk.LEFT, padx=15)


# root.grid_columnconfigure(0,weight=4)
# root.grid_columnconfigure(1,weight=1)


def listen_for_messages_from_server(client):
    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(content, username)

        else:
            messagebox.showerror("Error", "Message recevied from client is empty")


# main function
def main():
    root.mainloop()


if __name__ == '__main__':
    main()
