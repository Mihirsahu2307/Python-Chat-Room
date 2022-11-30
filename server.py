# Import required modules
import socket
import threading
import os
import random
import emails

registered_names = ["JACK", "TOM", "PAUL"]
passwords = {"JACK": "JACK1", "TOM": "TOM1", "PAUL": "PAUL1"}
online = set()

client_id = {}
history = {}
unique_code = {}
email_of = {}

for i in registered_names:
    history[i] = {}
    for j in registered_names:
        history[i][j] = ''

# Constants:
server_data = 'server_data'
FILE_BUFFER_SIZE = 2048
SEPARATOR = '<SEPARATOR>'
ENDTAG = '<ENDTAG>'

HOST = '127.0.0.1'
LISTENER_LIMIT = 5
PORT = 33


def send_history(client, username, message):
    msg = message[1:] + '~' + history[username][message[1:]]  # embedding the person on the other end of chat
    client.sendall(msg.encode())


def new_user_rituals(user):
    for name in registered_names:
        history[name][user] = ''

    history[user] = {}
    for name in registered_names:
        history[user][name] = ''

    for name in online:
        client_id[name].sendall(('^' + user).encode())

    registered_names.append(user)


def send_code(email):
    email = email[1:]
    global unique_code
    code = random.randint(0, 9999999999999999)
    unique_code[email] = str(code).zfill(16)
    unique_code[email] = "1"
    # emails.send_email(email, unique_code[email])


def create_acct(message):
    email, user, passw, code = message[1:].split('~')
    if email in email_of.values() and 0:
        print("Email already used")
    elif code != unique_code[email]:
        print("Wrong code used")
    else:
        email_of[user] = email
        passwords[user] = passw
        new_user_rituals(user)


def reset_password(message):
    email, user, passw, code = message[1:].split('~')
    if user not in registered_names or email not in email_of.values():
        print("Username or email is not registered")
    elif code != unique_code[email]:
        print("Wrong code used")
    else:
        passwords[user] = passw


# Function to listen for upcoming messages from a client
def listen_for_messages(client):
    username = ''
    while 1:

        message = client.recv(FILE_BUFFER_SIZE).decode('utf-8')  # normal message format: "receiver~message"
        if message != '':
            if message[0] == '?':
                send_history(client, username, message)
            elif SEPARATOR in message:
                print("Received a file")
                # message contains filename and filesize separated by separator
                filename, filesize, to_user = message.split(SEPARATOR, 2)
                filepath = os.path.join(server_data, to_user + filename)

                save_file_to_server(client, filepath)
                # threading.Thread(target=save_file_to_server, args=(client, filepath, )).start()
                send_file_to_user(filepath, to_user)
            elif message[0] == '@':
                send_code(message)
            elif message[0] == '!':  # message format: "!email~username~password~code"
                create_acct(message)
            elif message[0] == '*':  # message format: "*email~username~password~code"
                reset_password(message)
            elif message[0] == '^':  # message format: "^username~password"
                u, p = message[1:].split('~')
                print(message)
                client_handler(client, u, p)
                username = u
            else:
                send_message(username, message)
        else:
            print(f"The message send from client {username} is empty")


# Save given filepath to server data
def save_file_to_server(client, filepath):
    f = open(filepath, 'wb')
    file_bytes = b''
    while 1:
        data = client.recv(FILE_BUFFER_SIZE)
        file_bytes += data
        if file_bytes.endswith(ENDTAG.encode('ascii')):
            break

    f.write(file_bytes[:-len(ENDTAG)])
    f.close()

    print('Saved a file to server')


# Function to send a specific file to 1 user
def send_file_to_user(filepath, to_user, from_user):
    # Send a clickable message to user, clicking which, the user can open the file directly from the server directory
    # Send to to_user, not to all

    pass


# Function to send message to a single client
def send_message(sender, message):
    receiver, message = message.split('~')

    send_msg = '\n' + 'YOU: ' + message
    rec_msg = '\n' + '[' + sender + ']: ' + message

    # global history

    history[sender][receiver] += send_msg
    history[receiver][sender] += rec_msg

    if receiver in online:
        message = sender + '~' + rec_msg
        client_id[receiver].sendall(message.encode())  # message format: "sender~message"

    message = receiver + '~' + send_msg
    client_id[sender].sendall(message.encode())


# Function to handle client
def client_handler(client, username, password):
    if username not in registered_names or passwords[username] != password:
        return

    online.add(username)
    client_id[username] = client
    names_list = ''
    online_list = ''
    for user in registered_names:
        if user != username:
            if names_list != '':
                names_list += '~'
            names_list += user

            if user in online:
                if online_list != '':
                    online_list += '~'
                online_list += '~' + user

    client.sendall((names_list + '^' + online_list).encode())

    for name in registered_names:
        if name != username and name in online:
            client_id[name].sendall(('&'+username).encode())


# Main function
def main():
    # server data storage:
    if not os.path.exists(server_data):
        os.makedirs(server_data)
    for file in list(os.listdir(server_data)):
        os.remove(os.path.join(server_data, file))

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        print(client)

        threading.Thread(target=listen_for_messages, args=(client,)).start()


if __name__ == '__main__':
    main()
