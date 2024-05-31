import telnetlib

hostName = '192.168.0.60'

port = 23

user = b'administrator\r\n'

pw = b'password\r\n'

reboot = b'sw o01 reboot\r\n'

# Connect to the Telnet server

tn = telnetlib.Telnet(hostName, port)


def login():
    global tn
    try:
        # Read until 'Login:' prompt

        output = tn.read_until(b'Login:', timeout=2)

        # Send username

        tn.write(user)

        # Read until 'Password:' prompt

        output = tn.read_until(b'password:', timeout=2)

        # Send password

        tn.write(pw)

        # Read until 'Logged in successfully'

        tn.read_until(b'Logged in successfully', timeout=2)

        # Read until the command prompt, assuming it's '>'
    except Exception as e:

        print(f"Connection failed: {e}")


def disconnect():
    global tn
    try:
        # Send the reboot command

        tn.write(reboot)

        # Read and print the output of the reboot command

        output = tn.read_until(b'setting', timeout=2)

    except Exception as e:

        print(f"Connection failed: {e}")

    finally:

        # Close the Telnet connection
        tn.close()

        print('telnet detached')
