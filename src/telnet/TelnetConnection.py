import telnetlib


class TelnetConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def __init__(self, host_name, port):
        self.host_name = host_name
        self.port = port

    def connect(self):
        try:
            if not self._connection:

                self._connection = telnetlib.Telnet(self.host_name, self.port)
        except Exception as e:
            print('fail on establishing telnet connection')
            raise (__name__, 'fail on establishing telnet connection')

    def login(self, user=b'administrator\r\n', password=b'password\r\n'):

        if self._connection:
            try:
                # Read until 'Login:' prompt
                output = self._connection.read_until(b'Login:', timeout=2)

                # Send username
                self._connection.write(user)

                # Read until 'Password:' prompt
                output = self._connection.read_until(b'password:', timeout=2)

                # Send password
                self._connection.write(password)

                # Read until 'Logged in successfully'
                self._connection.read_until(b'Logged in successfully',
                                            timeout=2)

            except Exception as e:
                print(__name__, f"Telnet connection failed: {e}")
                raise (__name__, f"Telnet connection failed: {e}")

    def cut_power(self, reboot_cmd=b'sw o01 reboot\r\n'):

        if self._connection:
            try:
                # Send the reboot command
                self._connection.write(reboot_cmd)

                # Read and print the output of the reboot command
                output = self._connection.read_until(b'setting', timeout=2)

            except Exception as e:
                print(__name__, f"Telnet Connection failed: {e}")
                raise (__name__, f"Telnet Connection failed: {e}")

    def close(self):

        if self._connection:

            self._connection.close()
            self._connection = None
