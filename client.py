# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import os
import ntpath


FILE_BUFFER_SIZE = 2048
filepath = 'send_file.txt'
SEPARATOR = '<SEPARATOR>'
ENDTAG = '<ENDTAG>'
is_connected = False # Set to true when connected to server

HOST = '127.0.0.1'
PORT = 33

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


def connect():
    global username
    username = username_box.get()
    print(username)

    try:
        # Connect to the server
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        
        global is_connected
        is_connected = True
    except:
        print("Unable to connect to the server")

    try:
        client.sendall(username.encode())
    except:
        print("COULD NOT SEND NAME")


    names_list = []
    # Getting all names separated by ~ in one buffer
    message = client.recv(4*FILE_BUFFER_SIZE).decode('utf-8')  # getting the names list from the server

    if message == '':
        print("No users registered as of now")
    else:
        names_list = message[1:].split('~')        


    # chat list configuration
    root.configure(background=MEDIUM_GREY)

    # Atmost 5 clients:
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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

username = ""


def add_message(message, name):
    if name in boxes.keys() and tk.Toplevel.winfo_exists(windows[name]):  # checking if the chat window is open
        boxes[name].config(state=tk.NORMAL)
        boxes[name].insert(tk.END, message + '\n')
        boxes[name].config(state=tk.DISABLED)


# Send message or file using the send button
def send_message(textbox, person, upload_button):
    
    if upload_button.cget('text') != 'Upload':
        # Now a file has been selected and it needs to be uploaded
        send_file()
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
def send_file():
    to_user = 'PASS_AS_ARGUMENT'
    # file will be sent as a bytestream starting with a file tag, so that server knows it's a file
    
    filesize = os.path.getsize(filepath)
    
    client.send(f"{ntpath.basename(filepath)}{SEPARATOR}{filesize}{SEPARATOR}{to_user}".encode('utf-8'))
    f = open(filepath, 'rb')
    data = f.read()
    client.sendall(data)
    client.send(ENDTAG.encode('ascii'))
    f.close()
    

boxes = {}
windows = {}


def chat(person):
    # Opens tkinter window to select file for uploading
    def upload_file():
        if not is_connected:
            messagebox.showerror("Host Not Found", "Please connect to a server first")
            return
                
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        if not filename:
            return
        
        upload_button.config(state=tk.DISABLED)
        button_text = ntpath.basename(filename)
        
        global filepath
        filepath = filename
        print(filepath)
        
        if len(button_text) > 6:
            button_text = button_text[:4] + '...'
            
        upload_button.config(text=button_text)
        message_textbox.config(state=tk.DISABLED)
    
    
    windows[person] = tk.Toplevel()
    window = windows[person]
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

    username_label = tk.Label(top_frame, text=person, font=FONT, bg=DARK_GREY, fg=WHITE, state=tk.DISABLED)
    username_label.pack(side=tk.LEFT, padx=10)

    username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
    username_textbox.pack(side=tk.LEFT)

    username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect, state=tk.DISABLED)
    username_button.pack(side=tk.LEFT, padx=15)

    message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=30)
    message_textbox.pack(side=tk.LEFT, padx=10)
    
    upload_button = tk.Button(bottom_frame, text="Upload", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=upload_file)
    upload_button.pack(side=tk.LEFT, padx=10)

    message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE,
                               command=lambda textbox=message_textbox, user=person, upload_button=upload_button: send_message(textbox, user, upload_button))
    message_button.pack(side=tk.LEFT, padx=10)

    message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
    message_box.config(state=tk.DISABLED)
    message_box.pack(side=tk.TOP)

    boxes[person] = message_box

    client.sendall(('?' + person).encode())  # to ask for chat history with a person


def listen_for_messages_from_server(client):
    while 1:

        message = client.recv(FILE_BUFFER_SIZE).decode('utf-8')
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
