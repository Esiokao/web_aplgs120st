import subprocess


def change_ipAddr(interface_name, new_ip, netmask="255.0.0.0", gateway=None):
    try:
        command = [
            "netsh", "interface", "ipv4", "set", "address",
            f"name={interface_name}", "source=static", f"addr={new_ip}",
            f"mask={netmask}"
        ]

        if gateway:
            command.append(f"gateway={gateway}")

        subprocess.run(command, check=True, shell=True, stdin=subprocess.PIPE)

        print(f"IP: {new_ip}, interface: {interface_name}")
    except subprocess.CalledProcessError as e:
        print(f"errorMsg: {e}")
