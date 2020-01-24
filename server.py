import socket, time, persistqueue, os, shutil, collections, threading

quit = False
def delete (q): # время жизни сообщений(высчитываю не совсем корректно но это бетка)
		try:
			time.sleep(0.2) # чтобы меньше лагало
			clock = time.strftime("%d%M%S", time.localtime()) # время сейчас
			clock = int(clock)
			i = q.qsize()
			size = i
			while (i > 0):
				dat, dr, pr, vrem = q.get()
				a = int(clock) - int(vrem) # разница времени сообщения и время сейчас
				if (a > 10): # если больше n секунд, сам тут в ифе выбираешь, то сообщение удаляется из персистентноц очереди
					q.get()
				else: # тут мы пытаемся вернуть сообщение, которое мы попнули в строке 12, приходится проходить всю очередь с начала до конца
					k = q.qsize()
					q.put((dat, dr, pr, vrem))
					while (k > 0):
						dat, dr, pr, vrem = q.get()
						q.put((dat, dr, pr, vrem))
						k = k - 1
					i = 0
				i = i - 1
			l = q.qsize()
			if ((size - l) > 0): # если удалилось хоть одно сообщение, то нарушился мой "приоритет", т.е. число, которое показывает какое сообщение по порядку; и этот порядок надо восстановаить
				k = q.qsize()
				count = 1
				while (k > 0):
					data, adr, pr, vr = q.get()
					q.put((data,adr, count, vr))
					count = count + 1
					k = k - 1
			return 0
		except:
			return 0


def remove(q, priority):
	print(priority) # это серверу, сделал для себя
	code = 1 # новый "приоритет"
	size = q.qsize()
	size = size - 1
	i = priority # место удаляемого сообщения
	i = int(i)
	i = i - 1
	while (i > 0): # проходим по очереди, удаляя первый элемент и вставляя его в конец, меняя его приоритет

		data, ad, pr, vr = q.get()
		q.put((data,ad,code,vr))
		i = i - 1
		size = size - 1
		code = code + 1
	q.get() # дошли до удаляемого элемента и просто попнули его
	while (size > 0): # продолжаем удалять элементы начала и вставлять их в конец, чтобы восстановилась изначальная очередь без удаляемого элемента
		data, ad, pr, vr = q.get()
		q.put((data,ad,code,vr))
		code = code + 1
		size = size - 1

def resend(q, priority): # также как в удалении, только мы возвращаем нужный нам элемент, оставив его в очереди
	print(priority)
	code = 1
	size = q.qsize()
	size = size - 1
	i = priority
	i = int(i)
	i = i - 1
	while (i > 0):
		data, ad, pr, vr = q.get()
		q.put((data,ad,code,vr))
		i = i - 1
		size = size - 1
		code = code + 1
	da, get, mr, gh = q.get()
	q.put((da, get, mr, gh))
	while (size > 0):
		data, ad, pr, vr = q.get()
		q.put((data,ad,code,vr))
		code = code + 1
		size = size - 1
	return da



path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mypah') # настраиваем путь на папку, где хранится персистентная очередь, чтобы можно было удалять эту папку командой


q = persistqueue.SQLiteQueue('mypah', auto_commit=True) # настройка персистентной очереди( в папке он будет хранить все данные даже после конца работы сервера)
p = collections.deque() # дек, он используется для вывода истории сообщений, потому что мы используем очередь и когда запрашиваем вывод всей очереди с поомщью get(pop) он удаляет очередь и в деке будет хранится вся информация 
host = socket.gethostbyname(socket.gethostname()) # в клиенте
port = 9090

clients = [] # список клиентов, нужен для того,чтобы сообщения не приходили клиенту, который отправил их

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))




print("[ Server Started ]")

while not quit:
	try:
		data, addr= s.recvfrom(1024) # всегда пытаемся что-то получить от клиента (data - сообщение, addr - уникальный номер клиента, который генерируется сам)
		delete(q) # если лагает прога, тогда закомменть эту строку, она всегда пытается удалить сообщения(время жизни сообщений)(точнее не всегда, а когда какое-то сообщение приходит на сервер)

		if addr not in clients: # если клиента нет в списке клиентов, то добавим его
			clients.append(addr)

		if ((data.decode("utf-8") != "/his") and (data.decode("utf-8") != "/del") and (data.decode("utf-8") != "/rs")): # обычное сообшение
			priority = q.qsize() + 1 # приоритет, который я делаю не так видимо
			clock = time.strftime("%d%M%S", time.localtime()) # для времени жизни сообщений
			q.put((data, addr, priority, clock)) # помещаем сообщение в персистентную очередь
			

		if (data.decode("utf-8")) == "/his":
			for client in clients: # проходим по клиентам и находим только нашего
				if addr == client:
					s.sendto(("''''''''''''''''''''''''''''''''''''").encode("utf-8"), client) # для красоты			
					i = q.qsize()
					k = i
					while ((i > 0)):
						his, code, pr, clock = q.get() # забираем первое сообщение из очереди
						p.appendleft((his, code, pr, clock)) # вставляем его в дек
						print(his, pr) # принтим серверу
						mb = str(pr) # переводим инт в строку для кодирвоания
						strok = (his.decode("utf-8") + " " + mb) # нужная строка для отправки, тут я уже походу перемудрил(крч не оч красиво вышло( и мб это и не надо было))
						s.sendto(strok.encode("utf-8"), client) # отправляем клиенту сообщение
						i = i - 1
					while ((k > 0)): # тут возвращаем из дека в персистентную очередь
						his, code, pr, clock = p.pop()
						q.put((his, code, pr, clock))
						k = k - 1
					p.clear() # очищаем на всякий))
					s.sendto(("''''''''''''''''''''''''''''''''''''").encode("utf-8"), client) # для красоты!!	
			continue

		if (data.decode("utf-8")) == "/clear":
			shutil.rmtree(path) # удаляем папку с периситентной очередью
			i = q.qsize()
			while (i > 0): # очищаем нашу очередь
				q.get()
				i = i - 1

		if (data.decode("utf-8")) == "/del":
			mes, ad = s.recvfrom(1024) # получаем номер нужного нам сообщения
			remove(q,mes.decode("utf-8")) # удаляем		

		if (data.decode("utf-8")) == "/rs": # тут как в удалении
			mes, ad = s.recvfrom(1024)
			pd = resend(q,mes.decode("utf-8"))
			for client in clients:
				s.sendto("Resended:".encode("utf-8"),client)
				s.sendto(pd,client)
				s.sendto("______________________________________".encode("utf-8"),client)



		itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()) # берем время для того чтобы на сервере отображалось время отправки сообщения

		print("["+addr[0]+"]=["+str(addr[1])+"]=["+itsatime+"]/",end="") # принтим сообщение и время серверу
		print(data.decode("utf-8"))


		for client in clients: # тут отправка всем клиентам кроме того, кто отправил сообщения(тут надо добавить еще в ифы историю удаление и т.д., чтобы у других не отображалось)
			if ((addr != client) and (data.decode("utf-8") != "/rs")):
				s.sendto(data,client)
	except:	# конец серевра(конец работы программы)
		quit = True
		print("\n[ Server Stopped ]")
		s.close()

