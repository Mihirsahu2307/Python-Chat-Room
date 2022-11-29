# import required modules
import socket
import threading
import tkinter
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'

file1 = open("just.txt", 'r')
PORT = int(file1.read())
file1.close()

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

try:
    # Connect to the server
    client.connect((HOST, PORT))
    print("Successfully connected to server")
except:
    print("Unable to connect to the server")

username = ""

emb = unb = pwb = cdb = None
emf = unf = pwf = cdf = None


def add_message(message, name):
    if name in boxes.keys() and tk.Toplevel.winfo_exists(windows[name]):
        boxes[name].config(state=tk.NORMAL)
        boxes[name].insert(tk.END, message + '\n')
        boxes[name].config(state=tk.DISABLED)


def send_email(mode):
    email = emb.get() if mode else emf.get()
    client.sendall(('@' + email).encode())


# def register_account(user, password, email, code):
def register_account():
    email = emb.get()
    user = unb.get()
    password = pwb.get()
    code = cdb.get()
    client.sendall(('!' + email + '~' + user + '~' + password + '~' + code).encode())


def reset_password(user, password, email, code):
    pass


def create_account():
    global emb, unb, cdb, pwb
    window = tk.Toplevel()
    window.geometry("600x600")
    window.title("Create An Account")
    window.resizable(False, False)
    window.configure(background=DARK_GREY)

    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(4, weight=1)

    email_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    email_frame.grid(row=0, column=0, sticky=tk.NSEW)

    email_label = tk.Label(email_frame, text="email", font=FONT, bg=DARK_GREY, fg=WHITE)
    email_label.pack(side=tk.LEFT, padx=10)

    email_box = tk.Entry(email_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=20)
    email_box.pack(side=tk.LEFT, padx=10)
    emb = email_box

    code_button = tk.Button(email_frame, text="GET UNIQUE CODE", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                            command=lambda: send_email(1))
    code_button.pack(side=tk.LEFT, padx=15)

    user_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    user_frame.grid(row=1, column=0, sticky=tk.NSEW)

    user_label = tk.Label(user_frame, text="USERNAME", font=FONT, bg=DARK_GREY, fg=WHITE)
    user_label.pack(side=tk.LEFT, padx=10)

    user_box = tk.Entry(user_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    user_box.pack(side=tk.LEFT, padx=10)
    unb = user_box

    password_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    password_frame.grid(row=2, column=0, sticky=tk.NSEW)

    pass_label = tk.Label(password_frame, text="PASSWORD", font=FONT, bg=DARK_GREY, fg=WHITE)
    pass_label.pack(side=tk.LEFT, padx=10)

    password_box = tk.Entry(password_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    password_box.pack(side=tk.LEFT, padx=10)
    pwb = password_box

    code_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    code_frame.grid(row=3, column=0, sticky=tk.NSEW)

    code_label = tk.Label(code_frame, text="UNIQUE CODE", font=FONT, bg=DARK_GREY, fg=WHITE)
    code_label.pack(side=tk.LEFT, padx=10)

    code_box = tk.Entry(code_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    code_box.pack(side=tk.LEFT, padx=10)
    cdb = code_box

    create_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    create_frame.grid(row=4, column=0, sticky=tk.NSEW)

    create_btn = tk.Button(create_frame, text="CREATE NEW ACCOUNT", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                           command=register_account)
    create_btn.pack(fill=tkinter.BOTH, expand=True)


def forgot():
    window = tk.Toplevel()
    window.geometry("600x600")
    window.title("Forgot Password")
    window.resizable(False, False)
    window.configure(background=DARK_GREY)

    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(4, weight=1)

    email_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    email_frame.grid(row=0, column=0, sticky=tk.NSEW)

    email_label = tk.Label(email_frame, text="email", font=FONT, bg=DARK_GREY, fg=WHITE)
    email_label.pack(side=tk.LEFT, padx=10)

    email_box = tk.Entry(email_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=20)
    email_box.pack(side=tk.LEFT, padx=10)

    code_button = tk.Button(email_frame, text="GET UNIQUE CODE", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                            command=lambda email=email_box.get(): send_email(email))
    code_button.pack(side=tk.LEFT, padx=15)

    user_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    user_frame.grid(row=1, column=0, sticky=tk.NSEW)

    user_label = tk.Label(user_frame, text="USERNAME", font=FONT, bg=DARK_GREY, fg=WHITE)
    user_label.pack(side=tk.LEFT, padx=10)

    user_box = tk.Entry(user_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    user_box.pack(side=tk.LEFT, padx=10)

    password_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    password_frame.grid(row=2, column=0, sticky=tk.NSEW)

    pass_label = tk.Label(password_frame, text="NEW PASSWORD", font=FONT, bg=DARK_GREY, fg=WHITE)
    pass_label.pack(side=tk.LEFT, padx=10)

    password_box = tk.Entry(password_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    password_box.pack(side=tk.LEFT, padx=10)

    code_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    code_frame.grid(row=3, column=0, sticky=tk.NSEW)

    code_label = tk.Label(code_frame, text="UNIQUE CODE", font=FONT, bg=DARK_GREY, fg=WHITE)
    code_label.pack(side=tk.LEFT, padx=10)

    code_box = tk.Entry(code_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    code_box.pack(side=tk.LEFT, padx=10)

    reset_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    reset_frame.grid(row=4, column=0, sticky=tk.NSEW)

    reset_btn = tk.Button(reset_frame, text="RESET PASSWORD", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                          command=lambda u=user_box.get(), p=password_box.get(), e=email_box.get(),
                                         c=code_box.get(): reset_password(u, p, e, c))
    reset_btn.pack(fill=tkinter.BOTH, expand=True)


def connect():
    global username
    print("HEY")
    username = username_box.get()
    password = password_box.get()
    print(username)

    # try:
    #     # Connect to the server
    #     client.connect((HOST, PORT))
    #     print("Successfully connected to server")
    # except:
    #     print("Unable to connect to the server")

    # print("BRO1")
    # try:
    #     client.sendall(username.encode())
    # except:
    #     print("COULD NOT SEND NAME")
    # print("BRO2")
    #
    # client.sendall('~'.encode())
    #
    # try:
    #     client.sendall(password.encode())
    # except:
    #     print("COULD NOT SEND PASSWORD")

    try:
        client.sendall(('^' + username + '~' + password).encode())
    except:
        print("COULD NOT SEND USERNAME-PASSWORD")

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
windows = {}


def chat(person):
    windows[person] = tk.Toplevel()
    window = windows[person]
    window.geometry("600x600")
    window.title(username + " to " + person)
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

    username_label = tk.Label(top_frame, text=person, font=FONT, bg=DARK_GREY, fg=WHITE)
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

    client.sendall(('?' + person).encode())  # to ask for chat history with a person


# configuring the temporary opening screen

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

main_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
main_frame.grid(row=0, column=0, sticky=tk.NSEW)

user_label = tk.Label(main_frame, text="USERNAME", font=FONT, bg=DARK_GREY, fg=WHITE)
user_label.pack(side=tk.LEFT, padx=10)

username_box = tk.Entry(main_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
username_box.pack(side=tk.LEFT, padx=10)

password_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
password_frame.grid(row=1, column=0, sticky=tk.NSEW)

pass_label = tk.Label(password_frame, text="PASSWORD", font=FONT, bg=DARK_GREY, fg=WHITE)
pass_label.pack(side=tk.LEFT, padx=10)

password_box = tk.Entry(password_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
password_box.pack(side=tk.LEFT, padx=10)

login_button = tk.Button(main_frame, text="LOGIN", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
login_button.pack(side=tk.LEFT, padx=15)

forgot_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
forgot_frame.grid(row=2, column=0, sticky=tk.NSEW)

forgot_button = tk.Button(forgot_frame, text="FORGOT PASSWORD", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                          command=forgot)
forgot_button.pack(fill=tkinter.BOTH, expand=True)

create_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
create_frame.grid(row=3, column=0, sticky=tk.NSEW)

create_button = tk.Button(create_frame, text="CREATE AN ACCOUNT", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                          command=create_account)
create_button.pack(fill=tkinter.BOTH, expand=True)


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
