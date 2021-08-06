# cisco-telnet-enable-ssh

Summary:

Enable SSH version 2.0 on Cisco Catalyst switches via Telnet. Configuration of multiple switches is supported.
Tested primarily in virtual environment, but should run fine for older series. CAT9K was not tested.

Requirements:

1) Interpreter: Python 3.8.0+
2) Python Packages: telnetlib, time, re

How to run:

1) Open enable_ssh.py file with text editor and configure variables in the PARAMETERS section:
   
   A) Script supports different usernames and passwords across devices. For telnet, it is able to detect whether Username
      has been set, or password only.
   
   B) Enable password is not required, if it is not enabled in switch environment. Leave it as is if no enable needed.
   
   C) Rsa Key Modulus length is set to 2048 by default and adjustable via rsa_key_size variable.

   D) VTY Line #s are set under vty_lines variable, Line 18.
   
2) Navigate to script folder. Open terminal and run python3 enable_ssh.py. Once complete, switches should be accessible via SSH. 

Caveat:

1) Depending on the model of the catalyst switch, number of vty lines will differ. Therefore, SSH might not get enabled on all of them.