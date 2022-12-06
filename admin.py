import customer
import chef
import queue

from time import sleep
from shared_memory_dict import SharedMemoryDict 

print("Initializing databases")
cust_database = SharedMemoryDict(name='cust_database', size=10024)
chef_database = SharedMemoryDict(name='chef_database', size=1024)
order_database = SharedMemoryDict(name='order_database', size=1024)

# order_database = {}

order_database['ORDER_NUM'] = 1
import os, time, sys


chef_d = {}
chef_d['name'] = 'def_chef_1'
chef_d['pwd'] = 'def_chef_1'
chef_d['profile'] = ""
chef_d['dishes'] = [('Korma1', 12, 8, 4.5), ('Roti1', 13, 10, 4.5)]
chef_d['niche'] = [1,2]
chef_d['orders'] = 10
chef_d['rating'] = 4.5
chef_d['status'] = 'approved'
chef_database['def_chef_1'] = chef_d


chef_d = {}
chef_d['name'] = 'def_chef_2'
chef_d['pwd'] = 'def_chef_2'
chef_d['profile'] = ""
chef_d['dishes'] = [('Korma2', 14, 2, 4.6), ('Roti2', 10, 2, 4.6)]
chef_d['niche'] = [2,3]
chef_d['orders'] = 2
chef_d['rating'] = 4.6
chef_d['status'] = 'approved'
chef_database['def_chef_2'] = chef_d

chef_d = None

cust_d = {}
cust_d['name'] = 's'
cust_d['pwd'] = 's'
cust_d['prev_orders'] = []
cust_d['cart'] = {'chef': 'def_chef_1', 'items': [(1, 2, 13, 'Korma1')], 'price': 24}
cust_database['s'] = cust_d




PIPE_CUSTOMER_ADMIN = "to_admin"
BACKUP_FILE = "backup.csv"

if os.path.exists(BACKUP_FILE):
	pass

if not os.path.exists(PIPE_CUSTOMER_ADMIN):
	print("Initializing connections to clients")
	os.mkfifo(PIPE_CUSTOMER_ADMIN)
pipe_admin = os.open(PIPE_CUSTOMER_ADMIN, os.O_RDWR)

def chef_login(username, password):
	if (username in chef_database and chef_database[username]['pwd']==password and chef_database[username]['status']=="approved"):
		return chef_database[username]
	return None

def chef_register(name, username, password, dishes, niche, profile):
	if (username in chef_database):
		return False

	chef_d = dict()
	chef_d['name'] = name
	chef_d['pwd'] = password
	chef_d['profile'] = profile
	chef_d['dishes'] = []
	for dish in dishes:
		chef_d['dishes'].append((dish[0], dish[1], 0, 4.5))
	# chef_d['dishes'] = dish_list
	# # chef_d['dishes'] = dishes
	chef_d['niche'] = niche
	chef_d['orders'] = 0
	chef_d['rating'] = 4.5
	chef_d['status'] = "pending_approval"
	chef_database[username] = chef_d
	return True

def chef_update_rating(chef, rate, item=None):
	chef_d = chef_database[chef]
	if item!=None:
		chef_d['dishes'][item] = (chef_d['dishes'][0], chef_d['dishes'][1], chef_d['dishes'][item][2]+1, (chef_d['dishes'][item][3]*(chef_d['dishes'][item][2]) + rate)/(chef_d['dishes'][item][2]+1))
		# chef_d['dishes'][item][2] += 1
	elif item==None:
		chef_d['rating'] = (chef_d['rating']*(chef_d['orders']-1)+rate)/chef_d['orders']
	chef_database[chef] = chef_d


def chef_pending_orders(username):
	orders = []
	for order_num in order_database.keys():
		if order_num == "ORDER_NUM":
			continue
		order = order_database[order_num]
		if order['chef']==username and order['status']=='undelivered':
			orders.append((order_num, order))
	return orders 

def chef_register_delivery(username, order_num):
	if not order_num in order_database.keys():
		print("Wrong order requested")
		return False
	order = order_database[order_num]
	if not order['chef']==username:
		print("Wrong access requested")
		return False 
	if not order['status']=='undelivered':
		print("Order already fulfilled")
		return False
	order['status'] = 'delivered'
	order_database[order_num] = order
	return True

def chef_past_orders(username):
	orders = []
	for order_num in order_database.keys():
		if order_num == "ORDER_NUM":
			continue
		order = order_database[order_num]
		if order['chef']==username and order['status']=='delivered':
			orders.append((order_num, order))
	return orders

def chef_logout(username):
	pass


def get_recommendation(username, cuisine = None):
	print("ML-based recommendation pending. Please select another option.")
	pass

def get_best_rated(username, cuisine = None):
	q = queue.PriorityQueue()
	menu = {}
	for chef_key in chef_database.keys():
		chef = chef_database[chef_key]
		if(cuisine!=None):
			if(cuisine not in chef['niche']):
				continue
		q.put((-chef['rating'], chef_key))
	for i in range(5):
		if(q.empty()):
			break
		chef = q.get()
		menu[chef[1]] = chef_database[chef[1]]['dishes']
	if menu=={}:
		return None
	# print("In admin ", menu)
	return menu


def get_most_ordered(username, cuisine = None):
	q = queue.PriorityQueue()
	menu = {}
	for chef_key in chef_database.keys():
		chef = chef_database[chef_key]
		if(chef['status']=="pending_approval"):
			continue
		if(cuisine!=None):
			if(cuisine not in chef['niche']):
				continue
		q.put((-chef['orders'], chef_key))
	for i in range(5):
		if(q.empty()):
			break
		chef = q.get()
		menu[chef[1]] = chef_database[chef[1]]['dishes']
	if menu=={}:
		return None
	print("In admin ", menu)
	return menu

def get_cuisine(username, cuisine = None):
	menu = {}
	for chef_key in chef_database.keys():
		chef = chef_database[chef_key]
		if(chef['status']=="pending_approval"):
			continue
		if(cuisine!=None):
			if(cuisine not in chef['niche']):
				continue
		menu[chef_key] = chef['dishes']
	if menu=={}:
		return None
	print("In admin ", menu)
	return menu

def cust_login(username, password):
	if (username in cust_database and cust_database[username]['pwd']==password):
		return cust_database[username]
	return None

def cust_register(name, username, password):
	if (username in cust_database):
		return None

	cust_d = {}
	# cust_d['type'] = 'cust'
	cust_d['name'] = name
	cust_d['pwd'] = password
	cust_d['prev_orders'] = []
	cust_d['cart'] = {}
	cust_database[username] = cust_d
	# print(cust_database)
	return cust_database[username]

def cust_update_logout(username, customer_data):
	chef_d = cust_database[username]
	chef_d['cart'] = customer_data['cart']
	cust_database[username]['cart'] = chef_d
	# cust_database[username]['prev_orders'] = customer_data['prev_orders']

def update_cart(username, cart, item):
	if(len(item.split())<3):
		return cart
	chef = item.split()[0]
	dish = item.split()[1]
	qty = item.split()[2]
	if chef in chef_database.keys() and dish.isdigit() and int(dish)<=len(chef_database[chef]['dishes']) and qty.isdigit() and int(qty)<5:
		dish = int(dish)-1
		qty = int(qty)
		if (len(cart) and cart['chef']==chef):
			cart['items'].append((dish, qty, chef_database[chef]['dishes'][dish][1], chef_database[chef]['dishes'][dish][0]))
			cart['price'] += chef_database[chef]['dishes'][dish][1]*qty
		else:
			if(len(cart)):
				print("Do you want to change your chef? It will erase your previous cart.")
				print("(1) Yes\n(2) No")
				choice = input()
				if choice=="1":
					cart = {}
					cart['chef'] = chef
					cart['items'] = [(dish, qty, chef_database[chef]['dishes'][dish][1], chef_database[chef]['dishes'][dish][0])]
					cart['price'] = chef_database[chef]['dishes'][dish][1]*qty
			else:
				cart = {}
				cart['chef'] = chef
				cart['items'] = [(dish, qty, chef_database[chef]['dishes'][dish][1], chef_database[chef]['dishes'][dish][0])]
				cart['price'] = chef_database[chef]['dishes'][dish][1]*qty

	return cart

def new_order(username, cart):

	##update dish orders
	ORDER_NUM = order_database['ORDER_NUM']
	chef_d = chef_database[cart['chef']]
	if(chef_d['status']=="pending_approval"):
		print("Chef not approved yet!")
		return None, cust_database[username]
	chef_d['orders'] += 1
	chef_database[cart['chef']] = chef_d

	order_d = {}
	order_d['username'] = username
	order_d['items'] = cart['items']
	order_d['chef'] = cart['chef'] 
	order_d['price'] = cart['price']
	order_d['status'] = "undelivered"
	order_database[ORDER_NUM] = order_d
	status = "undelivered"
	while(status=="undelivered"):
		print("\nWaiting for order delivery..")
		status = order_database[ORDER_NUM]['status']
		print(status)
		print(order_database[ORDER_NUM])
		print(order_database)

		sleep(2)
		# print("Order delivered! Enjoy!")

	order_d['status'] = "delivered"
	order_database[ORDER_NUM] = order_d
	print("\nOrder delivered! Enjoy")
	order_database['ORDER_NUM'] = ORDER_NUM + 1
	cust_d = cust_database[username]
	cust_d['prev_orders'].append(order_d)
	cust_d['cart'] = {}
	cust_database[username] = cust_d
	return order_database[ORDER_NUM], cust_d

def cust_update(username, option, new_data):
	cust = cust_database[username]
	if(option=='1'):
		cust['name'] = new_data
	elif(option=='2'):
		cust['pwd'] = new_data
	cust_database[username] = cust
	return cust_database[username]

def check():
	print(cust_database)
	print(chef_database)
	print(order_database)

def show_pending_chef_registrations():
	for chef_username in chef_database.keys():
		chef = chef_database[chef_username]
		if chef['status'] == "pending_approval":
			print(chef)
	return

def approve_chef_registration(username):
	if not username in chef_database.keys():
		return False
	if not chef_database[username]['status']=="pending_approval":
		return False
	chef_d = chef_database[username]
	chef_d['status'] = "approved"
	chef_database[username] = chef_d
	return True

def show_pending_orders():
	for order_num in order_database.keys():
		if(order_num=="ORDER_NUM"):
			continue
		order = order_database[order_num]
		if(order['status']=="undelivered"):
			print(order)

if __name__=="__main__":
	## wait for shared memories to refresh
	sleep(1)
	print("Setup ready!")
	while(True):
		# command = os.read(pipe_admin, os.O_RDWR)
		# command = command.decode("utf-8")
		# if(len(command)):
		# 	print(command)

		# print("length", len(cust_database))
		# print()
		print("\n\nMain Menu:")
		print("(1) Pending chef registrations")
		print("(2) Show pending orders")
		print("(3) Show customer database")
		print("(4) Show chef database")
		print("(5) Show order database")
		print("(6) Shut down system")
		choice = input()

		if choice=="1":
			show_pending_chef_registrations()
			print("\nDo you want to approve applications?")
			print("(1) Yes\n(2) No")
			choice = input()
			while choice=="1":
				chef_username = input("Enter chef username to approve: ")
				result = approve_chef_registration(chef_username)
				if(result):
					print("Successfully approved chef")
				else:
					print("Approval error. Recheck username.")
				print("Do you want to approve other chefs?\n(1) Yes\n(2) No")
				choice = input()
		elif choice=="2":
			show_pending_orders()
		elif choice=="3":
			print(cust_database)
		elif choice=="4":
			print(chef_database)
		elif choice=="5":
			print(order_database) 
		elif choice=="6":
			print("\nShutting down system.")
			exit(0)
		else:
			print("Wrong input!")
		# print("\n")

