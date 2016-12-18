# pyscaner
a network scaner based on python!

##Introduction
This is a simple python project for practice.
It contains a ping tool with RAW socket, a TCP network scaner.
I didn't use much standard modules, instead, I tried to implement the basic functions myself.  
You will find python basic skills are used in this project.
If you are new to python, I will suggest you to fork it and add new features to it.

Next I will use multi-thread to speed up. Also will trying to OOP

##usage:
$sudo pyscaner.py <target> [port]

##Example:
- $sudo	./pyscaner.py 192.168.0.1/24 22-443
- $sudo ./pyscaner.py 192.168.0.1-192.168.0.99 80
- $sudo ./pyscaner.py 192.168.0.99
- note: without port specified, it will scanning the well-known ports predefined

