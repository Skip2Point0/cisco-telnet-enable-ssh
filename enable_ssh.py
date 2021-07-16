import telnetlib
import time
# ##################################################### PARAMETERS #####################################################
# Fill out username, password and enable password. If no enable is needed, leave it as is.
# Switches must prompt for username or the script won't complete.
# Rsa Key Modulus length is set to 2048 by default.
# ######################################################################################################################
user = 'cisco'
password = 'password'
enable_password = 'password'
domain = "yourveryownenterprises.org"
host = ['192.168.56.23', '192.168.56.40']
rsa_key_size = '2048'
# ######################################################################################################################
errors = []


def apply_ssh(usr, ps, e_ps, hosts, dm, keysize):
    for line in hosts:
        print("Configuring host " + line)
        line = line.strip()
        try:
            tn = telnetlib.Telnet(line, timeout=10)
            tn.read_until(b"Username: ")
            tn.write(usr.encode('ascii') + b"\n")
            if ps:
                tn.read_until(b"Password: ")
                tn.write(ps.encode('ascii') + b"\n")
            tn.write(b"enable\n")
            tn.write(e_ps.encode('ascii') + b"\n")
            tn.write(b"conf t\n")
            print("Assigning Domain")
            tn.write(b"ip domain-name " + dm.encode('ascii') + b"\n")
            print("Configuring SSH Version 2")
            tn.write(b"ip ssh version 2\n")
            print("Generating RSA Key")
            tn.write(b"cry key generate rsa general\n")
            time.sleep(3)
            print("RSA key" + keysize + "Bytes")
            tn.write(keysize.encode('ascii') + b"\n")
            time.sleep(3)
            print("Setting up VTY lines")
            tn.write(b"line vty 0 14\n")
            tn.write(b"transport input ssh\n")
            tn.write(b"end\n")
            print("Writing Memory")
            tn.write(b"wr mem\n")
            tn.write(b"exit\n")
            print("DONE")
            readoutput = tn.read_all().decode('ascii')
            print(readoutput)
        except:
            errors.append(line)


apply_ssh(user, password, enable_password, host, domain, rsa_key_size)

for error in errors:
    print("Errors were found on this host: " + error)
