import telnetlib

# Connect to the Telnet server


def createTelnet(hostName, port=23):
    tn = telnetlib.Telnet(hostName, port)
    return tn


def login(tn, user=b'administrator\r\n', password=b'password\r\n'):

    try:
        # Read until 'Login:' prompt

        output = tn.read_until(b'Login:', timeout=2)

        # Send username

        tn.write(user)

        # Read until 'Password:' prompt

        output = tn.read_until(b'password:', timeout=2)

        # Send password

        tn.write(password)

        # Read until 'Logged in successfully'

        tn.read_until(b'Logged in successfully', timeout=2)

    except Exception as e:

        print(f"Connection failed: {e}")


def cutPower(tn, rebootCmd=b'sw o01 reboot\r\n'):

    rebootCmd = b'sw o01 reboot\r\n'

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
