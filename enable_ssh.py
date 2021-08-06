import telnetlib
import re
import time
# ##################################################### PARAMETERS #####################################################
# Fill out username, password, enable password, domain name, and vty lines. If no enable is needed, don't make changes
# to line 11.
# Script supports different usernames and passwords across devices. For telnet, it is able to detect whether Username
# has been set, or password only.
# Rsa Key Modulus length is set to 2048 by default. Change on line 13 if different value is required.
# By default host ip addresses are entered under line 16. You can use text file host_ip.txt. Comment line 16, and
# uncomment lines 18-20.
# ######################################################################################################################
user = ['cisco', 'kisco']
password = ['password', 'cisco']
enable_password = ['cisco', 'password']
domain = "yourveryownenterprises.org"
rsa_key_size = '2048'
vty_lines = '0 14'
# ######################################################################################################################
hosts = ['192.168.56.23', '192.168.56.40']
# ######################################################################################################################
# hosts = 'host_ips.txt'
# with open(hosts) as f:
#     hosts = f.read().splitlines()
# ######################################################################################################################
prompt_list = [b'Username: ', b'Password: ']
errors = []


def tellib_find_password(ls, usr, pasw, en_pasw, swh):
    tn = telnetlib.Telnet(swh)
    auth = tn.expect(ls)
    prompt_parser = re.compile(r'Username:|Password:')
    prompt_type = prompt_parser.search(auth[1].group(0).decode('ascii'))
    tn.close()
    if prompt_type[0] == 'Password:':
        for p in pasw:
            tn = telnetlib.Telnet(swh)
            tn.read_until(b"Password: ")
            tn.write(p.encode('ascii') + b"\n")
            try:
                response = tn.read_until(b">", timeout=1)
            except EOFError as e:
                print("Connection closed: %s" % e)
            if b">" in response:
                tn.write(b"enable\n")
                for ep in en_pasw:
                    tn.write(ep.encode('ascii') + b"\n")
                    try:
                        response = tn.read_until(b"#", timeout=1)
                    except EOFError as e:
                        print("Connection closed: %s" % e)
                    if b"#" in response:
                        return tn

    elif prompt_type[0] == 'Username:':
        for u in usr:
            for p in pasw:
                tn = telnetlib.Telnet(swh)
                tn.read_until(b"Username: ")
                tn.write(u.encode('ascii') + b"\n")
                tn.read_until(b"Password: ")
                tn.write(p.encode('ascii') + b"\n")
                try:
                    response = tn.read_until(b">", timeout=1)
                except EOFError as e:
                    print("Connection closed: %s" % e)
                if b">" in response:
                    tn.write(b"enable\n")
                    for ep in en_pasw:
                        tn.write(ep.encode('ascii') + b"\n")
                        try:
                            response = tn.read_until(b"#", timeout=1)
                        except EOFError as e:
                            print("Connection closed: %s" % e)
                        if b"#" in response:
                            return tn


def apply_ssh(usr, ps, e_ps, hsts, dm, keysize, vtylines):
    for host in hsts:
        print("=================================================")
        print("Configuring host " + host)
        print("=================================================")
        host = host.strip()
        try:
            tn = tellib_find_password(prompt_list, usr, ps, e_ps, host)
            tn.write(b"conf t\n")
            print("Assigning Domain")
            tn.write(b"ip domain-name " + dm.encode('ascii') + b"\n")
            print("Configuring SSH Version 2")
            tn.write(b"ip ssh version 2\n")
            print("Generating RSA Key")
            tn.write(b"cry key generate rsa general\n")
            time.sleep(3)
            print("RSA key " + keysize + "Bytes")
            tn.write(keysize.encode('ascii') + b"\n")
            time.sleep(3)
            print("Setting up VTY lines: " + vtylines)
            tn.write(vtylines.encode('ascii') + b"\n")
            tn.write(b"transport input ssh\n")
            tn.write(b"end\n")
            print("Writing Memory")
            tn.write(b"wr mem\n")
            tn.write(b"exit\n")
            print("DONE")
            print("===============")
            # print(tn.read_all().decode('ascii'))
        except:
            errors.append(host)


apply_ssh(user, password, enable_password, hosts, domain, rsa_key_size, vty_lines)

for error in errors:
    print("Errors were found on host: " + error)
