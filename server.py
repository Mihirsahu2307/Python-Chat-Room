# Import required modules
import random
import socket
import threading
import emails

HOST = '127.0.0.1'
LISTENER_LIMIT = 5

file1 = open("just.txt", 'r')
PORT = int(file1.read()) + 1
file1.close()

file2 = open("just.txt", 'w')
file2.write(str(PORT))
file2.close()

registered_names = ["JACK", "TOM", "PAUL"]
passwords = {"JACK": "JACK1", "TOM": "TOM1", "PAUL": "PAUL1"}
online = set()
client_id = {}
unique_code = {}
email_of = {}

history = {}

for i in registered_names:
    history[i] = {}
    for j in registered_names:
        history[i][j] = ''


def send_history(client, username, message):
    msg = message[1:] + '~' + history[username][message[1:]]  # embedding the person on the other end of chat
    client.sendall(msg.encode())


def new_user_rituals(user):
    for name in registered_names:
        history[name][user] = ''

    history[user] = {}
    for name in registered_names:
        history[user][name] = ''

    registered_names.append(user)


def send_code(email):
    email = email[1:]
    global unique_code
    code = random.randint(0, 9999999999999999)
    unique_code[email] = str(code).zfill(16)
    # unique_code[email] = "1"
    emails.send_email(email, unique_code[email])


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

        message = client.recv(2048).decode('utf-8')  # normal message format: "receiver~message"
        print(message)
        if message != '':
            if message[0] == '?':
                send_history(client, username, message)
            elif message[0] == '@':
                send_code(message)
            elif message[0] == '!':  # message format: "!email~username~password~code"
                create_acct(message)
            elif message[0] == '*':  # message format: "*email~username~password~code"
                reset_password(message)
            elif message[0] == '^':  # message format: "^username~password"
                u, p = message[1:].split('~')
                client_handler(client, u, p)
                username = u
            else:
                send_message(username, message)
        else:
            print(f"The message send from client {username} is empty")


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
    # Server will listen for client message that will
    # Contain the username

    # flag = 0
    # print("HEY")
    #
    # while flag == 0 or (username not in registered_names or passwords[username] != password):
    #     print("NICE")
    #
    #     while 1:
    #
    #         username, password = client.recv(2048).decode('utf-8').split('~')
    #         flag = 1
    #         if username != '':
    #             online.add(username)
    #             client_id[username] = client
    #
    #             # enter code here to update other clients that this particular one is online
    #             break
    #         else:
    #             print("Client username is empty")
    #
    #     print(username, password)
    #
    # print("USERNAME AND PASSWORD RECEIVED")

    if username not in registered_names or passwords[username] != password:
        return

    online.add(username)
    client_id[username] = client
    names_list = ''
    online_list = ''
    for user in registered_names:
        if user != username:
            names_list += '~' + user

            if user in online:
                online_list += '^' + user

    client.sendall(names_list.encode())
    # client.sendall(online_list.encode())

    # threading.Thread(target=listen_for_messages, args=(client, username,)).start()


# Main function
def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
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

        threading.Thread(target=listen_for_messages, args=(client,)).start()


if __name__ == '__main__':
    main()
