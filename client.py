import socket, threading, time, string #библиотеки



shutdown = False
join = False

def receving (name, sock): # функция,которая отдельным потоком получает сообщения с сервера
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024) # принимаем значения из сокета (1024 это вроде количество битов)
				print(data.decode("utf-8")) # декодирует из (битого типа или какго-то дургого) в обычную строку

				# End

				time.sleep(0.2) # чтобы не запутался поток(ну там порядок сообщений)
		except:
			pass
host = socket.gethostbyname(socket.gethostname()) # это наш айпи
port = 0

server = ("",9090)

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # это настройка сокета на тсп и другие умные умные слова (по логике тут настройка стоит, что можно даже с разных компов запускать клиенты и все будет работать)
s.bind((host,port)) # передаем ему айпи
s.setblocking(0) # не уверен, что это нужно, но она предотвращает возможные ошибки
	
alias = input("Name: ") # запрашиваем имя

rT = threading.Thread(target = receving, args = ("RecvThread",s)) # настраиваем поток на нашу функцию
rT.start() # запуск

while shutdown == False:
	if join == False:
		s.sendto(("["+alias + "] => join chat ").encode("utf-8"), server) # если чел только зашел то серверу отправляем ник и что он заджойнился (кодируем) ОБЯЗАТЕЛЬНО так как другие типы данных не отправляет
		join = True 
	else:
		try:
			message = input() # считываем сообщение
			if message == "/his": # если запрос на историю сообщений
				s.sendto((message).encode("utf-8"),server)
			elif message == "/clear": # очистка данных из персистентной очереди т.е удаление всей истории
				s.sendto((message).encode("utf-8"),server)
			elif message == "/del": # клиент запрашивает удаление, дальше через энтр надо ввести цифру (тут я и использовал приоритет очередей, но видимо этот приоритет не для этого)
				k = input()
				s.sendto((message).encode("utf-8"),server)
				s.sendto((k).encode("utf-8"),server)

			elif message == "/rs": # ресенд т.е. переотправка сообщения как и в удалении нужно потом через энтр ввести цифру и он перешлет это сообщение всем
				k = input()
				s.sendto((message).encode("utf-8"),server)
				s.sendto((k).encode("utf-8"),server)

			elif message != "": # дальше если не пустое сообщение т.е. любое сообщение
				s.sendto(("["+alias + "] :: "+message).encode("utf-8"),server)

			time.sleep(0.2)
		except:
			s.sendto(("["+alias + "] <= left chat ").encode("utf-8"),server) # выход из чата т.е. конец работы нашей клиентской программы.
			shutdown = True

rT.join() # закрываем поток и сокет
s.close()