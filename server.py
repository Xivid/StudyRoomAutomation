import socket
import sys
from Tkinter import *

HOST = '127.0.0.1'   # Symbolic name meaning all available interfaces
PORT = 8756 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'
 
s.listen(10)


def update(event):
	global roominfo, count, rooms, roomlist, s, tmp, root
	tmp.focus_set()
	print 'Socket now listening'
	#now keep talking with the client
	#while 1:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	#print 'Connected with ' + addr[0] + ':' + str(addr[1])

	data = conn.recv(1024)
	#print data
	if len(data) < 1 or data[-1] not in '+-' or data[:-1] not in roominfo:
		reply = 'BAD'
	else:
		if data[-1] == '+':
			roominfo[data[:-1]]['count'] += 1
		else:
			roominfo[data[:-1]]['count'] -= 1
		ID = roominfo[data[:-1]]['id']
		roomlist.delete(ID)
		roomlist.insert(ID, rooms[ID] + ' ' * (30 - len(rooms[ID])) + str(roominfo[rooms[ID]]['count']))
		reply = 'OK'

	#if not data:Socket created
		#break

	conn.sendall(reply)
	root.update()
	roomlist.focus_set()



rooms = ["A", "B", "C"]
room_count = len(rooms)
roominfo = {}
for i in rooms:
	roominfo[i] = {'count': 0}

width = 145
height = 20 * room_count + 40

root = Tk()
root.maxsize(width, height)
root.minsize(width, height)
root.geometry("{}x{}+100+50".format(width, height))
root.title("Server")

tmp = Label(root, text = '')
tmp.place(x = width + 500, y = 0)

roomlist = Listbox(root, width = 20, height = 20 * room_count)
roomlist.place(x = 0, y = 0)

for i in range(room_count):
	roomlist.insert(i, rooms[i] + ' ' * (30 - len(rooms[i])) + str(roominfo[rooms[i]]['count']))
	roominfo[rooms[i]]['id'] = i	

roomlist.bind('<FocusIn>', update)
roomlist.focus_set()

root.mainloop()

conn.close()
s.close()
