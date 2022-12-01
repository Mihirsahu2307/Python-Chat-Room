import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(email, code):
    FROM_ADDR = "ChangeMe"
    FROM_PASSWD = "ChangeMe"

    Subject = "OTP for Chat App"
    Body = 'Here is the OTP for your login on Python chat app: ' + code
    send(FROM_ADDR, FROM_PASSWD, email, Subject, Body)


def send(fromaddr, frompasswd, toaddr, msg_subject, msg_body):
    try:
        msg = MIMEMultipart()
    except:
        print("[-] Error in Creating Message Object")
        return

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = msg_subject

    body = msg_body

    msg.attach(MIMEText(body, 'plain'))

    try:
        # s = smtplib.SMTP('smtp.gmail.com', 587)
        s = smtplib.SMTP('stud.iitp.ac.in', 587)  # Host used is for stud.iitp.ac.in accounts
        print("[+] SMTP Session Created")
    except:
        print("[-] Error in creating SMTP session")
        return

    s.starttls()

    try:
        s.login(fromaddr, frompasswd)
        print("[+] Login Successful")
    except:
        print("[-] Login Failed")

    text = msg.as_string()

    try:
        s.sendmail(fromaddr, toaddr, text)
        print("[+] Mail Sent successfully")
    except:
        print('[-] Mail not sent')

    s.quit()
