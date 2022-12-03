# server.py
import socket
import subprocess
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 1337))
s.listen(5)

conn, _ = s.accept()

fp = conn.makefile('wb', buffering=0)

proc1 = subprocess.Popen(['ls'], stdin=conn.makefile('rb', buffering=0), stdout=fp)
proc1.wait()
