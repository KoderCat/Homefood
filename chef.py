import customer 
import admin
# import Queue
import os, time, sys

# from shared_memory_dict import SharedMemoryDict 
# smd = SharedMemoryDict(name='Database', size=1024)

PIPE_CUSTOMER_ADMIN = "to_admin"
pipe_cust_admin = os.open(PIPE_CUSTOMER_ADMIN, os.O_RDWR)

if __name__ == "__main__":
	while(True):
		print("\n\nWelcome to Homefood! Please login or sign up.")
		print("Follow the instructions to proceed")
		print("(1) Login")
		print("(2) Sign up")
		choice = input()
		username = None
		password = None
		chef_data = None
		if(choice=="3"):
			print(admin.check())
			# smd[]
		if(choice=="1"):
			username = input("Username: ")
			password = input("Password: ")
			data = 'chef check_login %s %s\n' %(username,password)
			os.write(pipe_cust_admin, data.encode('utf-8'))
			chef_data = admin.chef_login(username, password)
			if (chef_data==None):
				print("Wrong username or password. If you have submitted application, please wait for approval.")
				continue
			print("Welcome back %s. Logging you in.."%username)

		elif(choice=="2"):
			name = input("First name, Last Name: ")
			username = input("Username: ")
			password = input("Password: ")
			
			break_flag = False
			#process dishes
			dishes_input = input("Dishes: \nEnter in form of <dish1 price1>, <dish2 price2>..\n")
			dishes = []
			for dish in dishes_input.split(','):
				dish = dish.split()
				if(len(dish)!=2 or not dish[1].isdigit()):
					print("Wrong input, application failed. Please retry.")
					break_flag = True
					break
				dishes.append((dish[0], int(dish[1])))
			if break_flag:
				continue

			#process niche
			niche_input = input("Niche:\n1. 2. 3. 4. 5. 6. 7. 8. 9. \nEnter niche1 niche2..\n")
			niche = []
			for n in niche_input.split():
				if not (n.isdigit() and int(n)<10):
					print("Wrong input, application failed. Please retry.")
					break_flag = True
					break
				niche.append(int(n))

			if break_flag:
				continue

			profile = input("Profile introduction: ")

			result = admin.chef_register(name, username, password, dishes, niche, profile)
			if (result==False):
				print("Sign up failed. Please try again or login")
				continue
			print("Congrats! Application created successfully. Please wait for approval and login..")
			continue
		else:
			print("Please enter a valid number!")
			continue


		print(chef_data)

		## Main Chef Menu
		while(chef_data!=None):
			print("\n\nMain menu:")
			print("(1) Show pending deliveries")
			print("(2) Register delivery")
			print("(3) See past deliveries")
			print("(4) Show current dish menu")
			print("(5) Add or delete menu item")
			print("(6) Logout")
			choice = input()

			if choice=="1":
				orders = admin.chef_pending_orders(username)
				print(orders)
			elif choice=="2":
				print("\nEnter delivery number")
				order_num = input()
				if not order_num.isdigit():
					print("Wrong input")
					continue
				result = admin.chef_register_delivery(username, int(order_num))
				if result:
					print("Thank you for the delivery!")
				else:
					print("Delivery failed. Wrong input.")
			elif choice=="3":
				orders = admin.chef_past_orders(username)
				print(orders)
			elif choice=="4":
				print(chef_data['dishes'])
			elif choice=="5":
				pass

			elif choice=="6":
				admin.chef_logout(username)
				username = None
				chef_data = None
			else:
				print("Please enter a valid number!")
				continue



