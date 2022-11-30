# import required modules
import socket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Tk
from tkinter import messagebox
from tkinter import StringVar
from tkinter.filedialog import askopenfilename
import os
import ntpath

client_data = 'client_data'
FILE_BUFFER_SIZE = 2048
filepath = 'send_file.txt'
MSG_DELIMITER = '\!?^'
SEPARATOR = '<SEPARATOR>'
ENDTAG = '<ENDTAG>'
is_connected = False  # Set to true when connected to server

HOST = '127.0.0.1'
PORT = 33

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
GREEN = '#5BFA05'
OFFLINE_BLUE = '#1593D6'
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Connect to the server
    client.connect((HOST, PORT))
    print("Successfully connected to server")
except:
    print("Unable to connect to the server")

num_users = 0
friendlist = {}

emb = unb = pwb = cdb = None
emf = unf = pwf = cdf = None


def send_signals():
    while 1:
        time.sleep(1)
        client.sendall(('$$$').encode())

        try:
            if not tk.Tk.winfo_exists(root):
                return
        except:
            return


def send_email(mode):
    email = emb.get() if mode else emf.get()
    client.sendall(('@' + email).encode())


def register_account():
    email = emb.get()
    user = unb.get()
    password = pwb.get()
    code = cdb.get()
    client.sendall(('!' + email + '~' + user + '~' + password + '~' + code).encode())


def reset_password():
    email = emf.get()
    user = unf.get()
    password = pwf.get()
    code = cdf.get()
    client.sendall(('*' + email + '~' + user + '~' + password + '~' + code).encode())


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
    create_btn.pack(fill=tk.BOTH, expand=True)


def forgot():
    global emf, unf, cdf, pwf

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
    emf = email_box

    code_button = tk.Button(email_frame, text="GET UNIQUE CODE", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                            command=lambda email=email_box.get(): send_email(email))
    code_button.pack(side=tk.LEFT, padx=15)

    user_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    user_frame.grid(row=1, column=0, sticky=tk.NSEW)

    user_label = tk.Label(user_frame, text="USERNAME", font=FONT, bg=DARK_GREY, fg=WHITE)
    user_label.pack(side=tk.LEFT, padx=10)

    user_box = tk.Entry(user_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    user_box.pack(side=tk.LEFT, padx=10)
    unf = user_box

    password_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    password_frame.grid(row=2, column=0, sticky=tk.NSEW)

    pass_label = tk.Label(password_frame, text="NEW PASSWORD", font=FONT, bg=DARK_GREY, fg=WHITE)
    pass_label.pack(side=tk.LEFT, padx=10)

    password_box = tk.Entry(password_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    password_box.pack(side=tk.LEFT, padx=10)
    pwf = password_box

    code_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    code_frame.grid(row=3, column=0, sticky=tk.NSEW)

    code_label = tk.Label(code_frame, text="UNIQUE CODE", font=FONT, bg=DARK_GREY, fg=WHITE)
    code_label.pack(side=tk.LEFT, padx=10)

    code_box = tk.Entry(code_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=25)
    code_box.pack(side=tk.LEFT, padx=10)
    cdf = code_box

    reset_frame = tk.Frame(window, width=600, height=100, bg=DARK_GREY)
    reset_frame.grid(row=4, column=0, sticky=tk.NSEW)

    reset_btn = tk.Button(reset_frame, text="RESET PASSWORD", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                          command=reset_password)
    reset_btn.pack(fill=tk.BOTH, expand=True)


def connect():
    global username, is_connected, num_users
    username = username_box.get()
    password = password_box.get()
    is_connected = True

    try:
        client.sendall(('^' + username + '~' + password).encode())
    except:
        print("COULD NOT SEND USERNAME-PASSWORD")

    # client data storage
    global client_data
    client_data = username + '_data'
    if not os.path.exists(client_data):
        os.makedirs(client_data)

    names_list = []
    online_set = set()
    # Getting all names separated by ~ in one buffer
    while 1:
        message = client.recv(FILE_BUFFER_SIZE).decode('utf-8')  # getting the names list from the server

        if message == '':
            print("No users registered as of now")
        else:
            names_list, online_set = message.split('^')
            names_list = names_list.split('~')
            online_set = set(online_set.split('~'))

        break

    # chat list configuration

    for row in grid_rows_to_destroy:
        row.destroy()

    username_box.config(state=tk.DISABLED)
    login_button.config(state=tk.DISABLED)

    root.configure(background=MEDIUM_GREY)

    for i in range(6):
        root.grid_rowconfigure(i + 1, weight=1)

    for i in range(len(names_list)):
        name_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
        name_frame.grid(row=i + 1, column=0, sticky=tk.NSEW)

        name_label = tk.Label(name_frame, text=names_list[i], font=FONT, bg=DARK_GREY,
                              fg=GREEN if names_list[i] in online_set else OFFLINE_BLUE)
        name_label.pack(side=tk.LEFT, padx=10)

        name_button = tk.Button(name_frame, text="Chat", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                                command=lambda person=names_list[i]: chat(person))
        name_button.pack(side=tk.LEFT, padx=15)

        friendlist[names_list[i]] = name_label
        num_users += 1

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()
    threading.Thread(target=send_signals).start()


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
forgot_button.pack(fill=tk.BOTH, expand=True)

create_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
create_frame.grid(row=3, column=0, sticky=tk.NSEW)

create_button = tk.Button(create_frame, text="CREATE AN ACCOUNT", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                          command=create_account)
create_button.pack(fill=tk.BOTH, expand=True)

grid_rows_to_destroy = [password_frame, forgot_frame, create_frame]

username = ""


def add_message(message, name):
    if name in boxes.keys() and tk.Toplevel.winfo_exists(windows[name]):  # checking if the chat window is open
        boxes[name].config(state=tk.NORMAL)
        boxes[name].insert(tk.END, message + '\n')
        boxes[name].config(state=tk.DISABLED)

        
# typing indicator
def toggle_typing_state(name):
    if name in boxes.keys() and tk.Toplevel.winfo_exists(windows[name]):  # checking if the chat window is open
        to_user_textboxes[name].config(state=tk.NORMAL)
        prev_text = to_user_textboxes[name].cget('text')
        new_text = prev_text
        if prev_text.endswith('(...is typing)'):
            new_text = new_text[:-14]
        else:
            new_text += '(...is typing)'
            
        to_user_textboxes[name].config(text = new_text, state=tk.DISABLED)


# Send message or file using the send button
def send_message(textbox, person, upload_button):
    if upload_button.cget('text') != 'Upload':
        # Now a file has been selected and it needs to be uploaded
        send_file(person)
        upload_button.config(text='Upload', state=tk.NORMAL)
        textbox.config(state=tk.NORMAL)
    else:
        message = person + '~' + textbox.get()
        if textbox.get() != '':
            try:
                client.sendall(message.encode())
                textbox.delete(0, len(message))
            except:
                messagebox.showerror("Host Not Found", "Please connect to a server first")
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")


# Send the file contents in binary form
def send_file(person):
    to_user = person
    # file will be sent as a bytestream starting with a file tag, so that server knows it's a file

    filesize = os.path.getsize(filepath)

    client.sendall(f"{ntpath.basename(filepath)}{SEPARATOR}{username}{SEPARATOR}{to_user}".encode('utf-8'))
    f = open(filepath, 'rb')
    data = f.read()
    client.sendall(data)
    client.sendall(ENDTAG.encode('ascii'))
    f.close()


to_user_textboxes = {}
boxes = {}
windows = {}


def chat(person):
    prev_typing_state = False
    current_typing_state = False
    # Opens tkinter window to select file for uploading
    def upload_file():
        if not is_connected:
            messagebox.showerror("Host Not Found", "Please connect to a server first")
            return

        Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

        filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        if not filename:
            return

        # upload_button.config(state=tk.DISABLED)
        button_text = ntpath.basename(filename)

        global filepath
        filepath = filename
        print(filepath)

        if len(button_text) > 6:
            button_text = button_text[:4] + '...'

        upload_button.config(text=button_text)
        message_textbox.config(state=tk.DISABLED)
        
    # Callback to handle typing events
    def typing_indicator_callback(sv):
        nonlocal current_typing_state
        nonlocal prev_typing_state
        
        content = sv.get()
        if content == '':
            current_typing_state = False
        else:
            current_typing_state = True
        
        if current_typing_state != prev_typing_state:
            print('Changed')
            # \! : Typing indicator command
            client.sendall(f"\!{SEPARATOR}{username}{SEPARATOR}{person}".encode('utf-8'))
            # pass # Send typing info to person
        prev_typing_state = current_typing_state

    windows[person] = tk.Toplevel()
    window = windows[person]
    window.geometry("600x600")
    window.title(username + '\'s Chat Window')
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

    username_label = tk.Label(top_frame, text=person, font=FONT, bg=DARK_GREY, fg=WHITE, state=tk.DISABLED)
    username_label.pack(side=tk.LEFT, padx=10)

    sv = StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: typing_indicator_callback(sv))
    message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=30, textvariable=sv)
    message_textbox.pack(side=tk.LEFT, padx=10)
    message_textbox.pack()

    upload_button = tk.Button(bottom_frame, text="Upload", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                              command=upload_file)
    upload_button.pack(side=tk.LEFT, padx=10)

    message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                               command=lambda textbox=message_textbox, user=person,
                                              upload_btn=upload_button: send_message(textbox, user, upload_btn))
    message_button.pack(side=tk.LEFT, padx=10)

    message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67,
                                            height=26.5, )
    message_box.config(state=tk.DISABLED)
    message_box.pack(side=tk.TOP)

    boxes[person] = message_box
    to_user_textboxes[person] = username_label

    client.sendall(('\?' + person).encode())  # to ask for chat and file history with a person


def save_file(filepath, message_second_part):
    f = open(filepath, 'wb')

    file_byte_info = message_second_part.split(MSG_DELIMITER)

    # print("In save_file: " + file_byte_info[1])
    file_bytes = b''
    if len(file_byte_info) > 1:
        file_bytes += (file_byte_info[1].encode('ascii'))

    while 1:
        if file_bytes.endswith(ENDTAG.encode('ascii')):
            break
        data = client.recv(FILE_BUFFER_SIZE)
        file_bytes += data
        # print("For user: " + username + ", data:")
        # print(file_bytes)

    f.write(file_bytes[:-len(ENDTAG)])
    f.close()

    print('Saved a file to cient data')


def new_user_rituals(user):
    global num_users
    num_users += 1
    name_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
    name_frame.grid(row=num_users, column=0, sticky=tk.NSEW)

    name_label = tk.Label(name_frame, text=user, font=FONT, bg=DARK_GREY, fg=WHITE)
    name_label.pack(side=tk.LEFT, padx=10)

    name_button = tk.Button(name_frame, text="Chat", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                            command=lambda person=user: chat(user))
    name_button.pack(side=tk.LEFT, padx=15)


def new_online_rituals(user):
    friendlist[user].config(fg=GREEN)


def new_offline_rituals(user):
    friendlist[user].config(fg=OFFLINE_BLUE)


# listen for messages from other clients sent via the server
def listen_for_messages_from_server(client):
    while 1:

        # message = recv_one_message(client)
        try:
            message = client.recv(FILE_BUFFER_SIZE).decode('utf-8')
        except:
            continue
        # print("In Body: ")
        # print(message)
        if message != '':
            if message[:2] == '\!':
                # This message will directly go to the to_user client, so no need to read the contents
                _, from_user = message.split('\!')                
                toggle_typing_state(from_user)
            elif SEPARATOR in message:
                print("Received a file")
                # message contains filename and filesize separated by separator
                filename, from_user, to_user = message.split(SEPARATOR, 2)

                global client_data
                filepath = os.path.join(client_data, "From_" + from_user + '__' + filename)

                print("FileName: " + filename + ", Path: " + filepath + ", to_user: " + to_user)
                save_file(filepath, to_user)
            elif message[0] == '^':
                new_user_rituals(message[1:])
            elif message[0] == '&':
                new_online_rituals(message[1:])
            # elif message =='###':
            #     pass
            elif message[0] == '|':
                new_offline_rituals(message[1:])
            else:
                try:
                    username = message.split("~")[0]
                    content = message.split('~')[1]
                except:
                    continue

                add_message(content, username)
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")


# main function
def main():
    root.mainloop()


if __name__ == '__main__':
    main()
