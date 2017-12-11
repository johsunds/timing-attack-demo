import socket
import sys
import time

password = "thisisaprettylongpassword"

DELAY = 0.0001

#Checks the password one character at a time, returning false as soon a character doesn't match
def check_password(pw):
	if len(pw) != len(password):
		return False
	for i in range(len(password)):
		time.sleep(DELAY)
		if pw[i] != password[i]:
			return False
	return True

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = ('127.0.0.1', int(sys.argv[1]))
	print("Starting server on " + str(addr))
	sock.bind(addr)
	sock.listen(1)
	while True:
		connection, _ = sock.accept()
		try:
			while True:
				data = connection.recv(64)
				if len(data) > 0:
					if check_password(data.strip()):
						connection.send(b'Success!')
						break
					else:
						connection.send(b'Wrong password!')
		except Exception as e:
			print(e)
		finally:
			print("closing")
			connection.close()



if __name__ == '__main__':
	main()