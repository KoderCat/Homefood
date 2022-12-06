import chef
import admin
# import Queue
import os, time, sys

# from shared_memory_dict import SharedMemoryDict 
# smd = SharedMemoryDict(name='Database', size=1024)
# print(smd.keys())

PIPE_CUSTOMER_ADMIN = "to_admin"
pipe_cust_admin = os.open(PIPE_CUSTOMER_ADMIN, os.O_RDWR)


def get_review(username, customer_data, order):
	print()
	chef = order['chef']
	for item in order['items']:
		rate = "6"
		while not(rate.isdigit() and int(rate)<=5):
			print("Please rate the dish %s" %(item[3]))
			rate = input()
		admin.chef_update_rating(chef, int(rate), int(item[0])-1)
	rate = "6"
	while not(rate.isdigit() and int(rate)<=5):
		print("Please rate the overall order")
		rate = input()
	admin.chef_update_rating(chef, int(rate))
	print("Thank you for your time!")


if __name__ == "__main__":
	while(True):
		print("\n\nWelcome to Homefood! Please login or sign up.")
		print("Follow the instructions to proceed")
		print("(1) Login")
		print("(2) Sign up")

		choice = input()
		username = None
		if choice=="3":
			admin.check()
		if(choice=="1"):
			username = input("Username: ")
			password = input("Password: ")
			data = 'cust check_login %s %s\n' %(username,password)
			os.write(pipe_cust_admin, data.encode('utf-8'))
			customer_data = admin.cust_login(username, password)
			if (customer_data==None):
				print("Wrong username or password")
				continue
			print("Welcome back %s. Logging you in.."%username)

		elif(choice=="2"):
			# customer_data = admin.cust_register()
			name = input("First name, Last Name: ")
			username = input("Username: ")
			password = input("Password: ")
			customer_data = admin.cust_register(name, username, password)
			if (customer_data==None):
				print("Sign up failed. Please try again or login")
				continue
			print("Congrats! Account created successfully. Logging you in..")
		else:
			print("Please enter a valid number!")
			continue

		print(customer_data)
		cart = customer_data['cart']
		while(customer_data!=None):
			print("\n\nMain Menu:")
			print("(1) Show menu and order")
			print("(2) Show previous orders")
			print("(3) Update/ change personal information")
			print("(4) Logout")
			choice = input()
			if(choice=="1"):
				## Shows Menus
				while(choice!="6"):
					print("\n(1) Recommendations")
					print("(2) Best-rated near you")
					print("(3) Most ordered near you")
					print("(4) Select by cuisines")
					print("(5) Add to cart")
					print("(6) Show cart")
					print("(7) Proceed to checkout")
					print("(8) Go back")
					menu = None
					show_menu = False
					choice = input()
					if choice=="1":
						menu = admin.get_recommendation(username)
						if menu: show_menu = True
					elif choice=="2":
						menu = admin.get_best_rated(username)
						if menu: show_menu = True
					elif choice == "3":
						menu = admin.get_most_ordered(username)
						if menu: show_menu = True
					elif choice == "4":
						print("\n(1) Chinese")
						print("(2) French")
						print("(3) Indian")
						print("(4) Italian")
						print("(5) Japanese")
						print("(6) Korean")
						print("(7) Mexican")
						print("(8) Thai")
						print("(9) Vegan")
						print("(10) Go back")
						print("NOTE: Enter rec_x, rat_x or ord_x for relavant information")
						choice = input()
						choice_1 = choice.split("_")[0]
						choice_2 = choice.split("_")[-1]
						if(choice_2.isdigit() and int(choice_2)<9):
							choice_2 = int(choice_2)
							if (choice_1=="rec"):
								menu = admin.get_recommendation(username, choice_2)
								if menu: show_menu = True
							elif (choice_1=="rat"):
								menu = admin.get_best_rated(username, choice_2)
								if menu: show_menu = True
							elif(choice_1=="ord"):
								menu = admin.get_most_ordered(username, choice_2)
								if menu: show_menu = True
							else:
								menu = admin.get_cuisine(username, choice_2)
								if menu: show_menu = True
						elif(choice=="10"):
							pass
						else:
							print("Please enter a valid number!")

					elif choice == "5":
						print("\nEnter <Chef> <Dish Number> <Quantity>")
						items = input()
						for item in items.split(","):
							cart = admin.update_cart(username, cart, item)
							customer_data['cart'] = cart
							print("Updated cart: ", cart)
					elif choice == "6":
						print(cart)
					elif choice=="7":

						if (not len(cart)):
							print("Your cart is empty!")
							continue
						if(cart['price']<15):
							print("Minimum order amount should be 15.")
							continue

						print("Confirm order from %s" %(cart['chef']))
						print("(1) Yes\n(2) Cancel")
						confirm = input()
						if not confirm=="1":
							continue
						order, customer_data = admin.new_order(username, cart)
						if order==None:
							print("Order unsuccesful")
							continue
						# customer_data['prev_orders'].append(order)
						print("Please review your order!")
						print("(1) Yes\n(2) No")
						choice = input()
						if(choice=="1"):
							get_review(username, customer_data, order)
						break

					elif choice == "8":
						break
					else:
						print("Please enter valid number!")

					if(show_menu):
						print("MENU FOUND")
						print(menu)
					elif(choice in [["1", "2", "3", "4"]]):
						print("No relevant menu found.")

			elif(choice=="2"):
				if len(customer_data['prev_orders']):
					for order in customer_data['prev_orders']:
						print(order)
				else:
					print("No past orders found.")
					continue

			elif(choice=="3"):
				print("Select information to change")
				print("(1) Name")
				print("(2) Password")
				option = input()
				new_data = input("Input updated information: ")
				if(option!="1" and option!="2"):
					"Please enter a valid number!"
				else:
				
					customer_data = admin.cust_update(username, option, new_data)
					print("Data has been updated.")
			elif(choice=="4"):
				admin.cust_update_logout(username, customer_data)
				customer_data = None
				username = None
				continue
			else:
				print("Please enter a valid number!")
				continue

