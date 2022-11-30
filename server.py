# Import required modules
import socket
import threading
import os
import ntpath
import time
import random

registered_names = ["JACK", "TOM", "PAUL"]
passwords = {"JACK": "JACK1", "TOM": "TOM1", "PAUL": "PAUL1"}
online = set()
still_conn = {}

client_id = {}
history = {}
unique_code = {}
email_of = {}
file_cache = {}

for i in registered_names:
    history[i] = {}
    file_cache[i] = {}
    still_conn[i] = 0
    for j in registered_names:
        history[i][j] = ''
        file_cache[i][j] = []  # Files will be stored as dictionaries using keys: 'Name' and 'Path'

# Constants:
server_data = 'server_data'
FILE_BUFFER_SIZE = 2048
MSG_DELIMITER = '\!?^'
SEPARATOR = '<SEPARATOR>'
ENDTAG = '<ENDTAG>'

HOST = '127.0.0.1'
LISTENER_LIMIT = 5
PORT = 33


def is_working():
    while 1:
        to_remove = []
        for user in online:
            if not still_conn[user]:
                to_remove.append(user)

        print(online)
        print(to_remove)
        print("conn", still_conn)

        for user in to_remove:
            online.remove(user)

        for user in online:
            for rem in to_remove:
                client_id[user].sendall(('|' + rem).encode())

        for user in registered_names:
            still_conn[user] = 0

        print("conn", still_conn)
        time.sleep(5)


threading.Thread(target=is_working).start()


def send_history(client, from_user, message):
    # Chat history:
    msg = message[2:] + '~' + history[from_user][message[2:]]  # embedding the person on the other end of chat
    client.sendall(msg.encode())

    print(from_user, message[2:])
    print(file_cache[message[2:]][from_user])
    # File history:
    for file in file_cache[message[2:]][from_user]:
        print(file['Name'], file['Path'])
        filename = file['Name']
        filepath = file['Path']
        to_user = message[2:]

        client.sendall(f"{ntpath.basename(filename)}{SEPARATOR}{from_user}{SEPARATOR}{to_user}{MSG_DELIMITER}".encode())

        f = open(filepath, 'rb')
        data = f.read()
        client.sendall(data)
        client.sendall(ENDTAG.encode('ascii'))
        f.close()


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
    while 1:

        message = client.recv(FILE_BUFFER_SIZE).decode('utf-8')  # normal message format: "receiver~message"
        if message != '':
            if message[:2] == '\?':
                send_history(client, username, message)
            elif message[:2] == '\!':
                _, from_user, to_user = message.split(SEPARATOR)
                msg = '\!' + from_user
                client_id[to_user].sendall(msg.encode('utf-8'))
            elif SEPARATOR in message:
                print("Received a file")
                # message contains filename and filesize separated by separator
                filename, from_user, to_user = message.split(SEPARATOR, 2)
                filepath = os.path.join(server_data, from_user + '@' + to_user + '@' + filename)

                save_file_to_server(client, filepath, to_user)
                send_file_to_user(filepath, filename, to_user, from_user)
            elif message[0] == '@':
                send_code(message)
            elif message[0] == '!':  # message format: "!email~username~password~code"
                create_acct(message)
            elif message[0] == '*':  # message format: "*email~username~password~code"
                reset_password(message)
            elif message[0] == '^':  # message format: "^username~password"
                u, p = message[1:].split('~')
                # print(message)
                client_handler(client, u, p)
                username = u
            elif message == '$$$':
                still_conn[username] = 1
            else:
                send_message(username, message)
        else:
            print(f"The message send from client {username} is empty")


# Save given filepath to server data
# Multiple TCP packets can be received using the same recv command, so the packets are delimited using a custom delimiter
# The message_second_part variable may contain info from the second intented TCP packet, separated via the delimiter
def save_file_to_server(client, filepath, message_second_part):
    f = open(filepath, 'wb')

    file_byte_info = message_second_part.split(MSG_DELIMITER)

    file_bytes = b''
    if len(file_byte_info) > 1:
        file_bytes += (file_byte_info[1].encode('ascii'))

    while 1:
        if file_bytes.endswith(ENDTAG.encode('ascii')):
            break
        data = client.recv(FILE_BUFFER_SIZE)
        file_bytes += data

    f.write(file_bytes[:-len(ENDTAG)])
    f.close()

    print('Saved a file to server')


# Function to send a specific file to 1 user
def send_file_to_user(filepath, filename, to_user, from_user):
    # Send a clickable message to user, clicking which, the user can open the file directly from the server directory
    # Send to to_user, not to all
    send_msg = '\n' + 'YOU: Sent file - ' + ntpath.basename(filename)
    rec_msg = '\n' + '[' + from_user + ']: You received a file -' + ntpath.basename(filename)

    # global history
    history[from_user][to_user] += send_msg
    history[to_user][from_user] += rec_msg

    # File_cache
    this_file = {
        'Name': ntpath.basename(filename),
        'Path': filepath
    }
    file_cache[from_user][to_user].append(this_file)

    print(from_user, to_user)
    print(file_cache[from_user][to_user])

    # Notify user that a file was sent:
    if to_user in online:
        # Msg transfer:
        message = from_user + '~' + rec_msg
        # send_one_message(client_id[to_user], message.encode())
        client_id[to_user].sendall(message.encode())  # message format: "sender~message"

        # File transfer:

        # send_one_message(client_id[to_user], f"{ntpath.basename(filename)}{SEPARATOR}{from_user}{SEPARATOR}{to_user}".encode())
        client_id[to_user].sendall(
            f"{ntpath.basename(filename)}{SEPARATOR}{from_user}{SEPARATOR}{to_user}{MSG_DELIMITER}".encode())

        f = open(filepath, 'rb')
        data = f.read()

        # send_one_message(client_id[to_user], data)
        client_id[to_user].sendall(data)

        # send_one_message(client_id[to_user], ENDTAG.encode('ascii'))
        client_id[to_user].sendall(ENDTAG.encode('ascii'))
        f.close()

    # for from_user, only chat gets updated
    message = to_user + '~' + send_msg
    client_id[from_user].sendall(message.encode())


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
    still_conn[username] = 1
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
            client_id[name].sendall(('&' + username).encode())


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
