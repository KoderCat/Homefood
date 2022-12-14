# Homefood
**Note**: This code runs the Homefood MVP (expect for the chat-community feature), and supports chef and customer profiles.

To run Homefood (compatible with Python 3.x), please follow these steps in sequential order:

(1) Run admin.py to start the server and load default chef, customer and order databases. Please wait till all databases are loaded and connections are established

(2) On a separate terminal, login or sign up as a chef (by running chef.py), customer (by running customer.py), or both from two different terminals.

---------------------------------------------------------------------------------------------------------------------------------------------------

The **admin** program allows the following actions:

(1) Pending chef registrations - Show registrations to be approved, proceed to approve chef applications

(2) Show pending orders - Search order database and show current unfulfilled orders

(3) Show customer database - Show all customer accounts and their informartion in the system

(4) Show chef database - Show all chef accounts and their informartion in the system

(5) Show order database - Show all unfulfilled or fulfilled orders till date

(6) Shut down system - Shut down the entire Homefood app and services

---------------------------------------------------------------------------------------------------------------------------------------------------

The **customer** program allows the following actions:

(1) Login - Login with valid username and password 

(2) Sign up - Sign up with unique username and password (does not need validation from admin)

After login, the following actions are available:

(1) Show menu and order - Set different filters or sorting algorithms and show menu

    (1.1) Recommendations - To be developed: RL based recommendation system
    
    (1.2) Best rated near you - Sorts chefs based on best aggregate ratings of dishes and chef
    
    (1.3) Most ordered near you - Sorts chefs based on total orders from chef
    
    (1.4) Select by cuisines - Filter based on 8 available cuisines or Vegan options, and then sort based on best rated or most ordered
    
    (1.5) Add to cart - Change chef or add new dishes to cart(asks for validation if change of chef is detected)
    
    (1.6) Show cart - View cart details and order amount
    
    (1.7) Proceed to checkout - Confirm order and wait for order to be delivered (until chef registers delivery)
    
                                Once delivered, show option to review chef
                                
                                
                                Review individual dishes and overall chef experience
                                
                                Update and sync the aggregate rating of chef
                                
(2) Show previous orders - View all fulfilled orders in your account with chef name, price and dishes ordered

(3) Show account information - Show account details and refreshed ratings of previously-ordered dishes

(4) Update personal information - Change password or account details

(5) Logout - Go to main customer page

---------------------------------------------------------------------------------------------------------------------------------------------------

The **chef** program allows the following actions:

(1) Login - Login with valid username and password (after chef approval from admin)

(2) Sign up - Submit application after entering details and proposed dishes

After login, the following actions are available:

(1) Show pending deliveries - Show unfulfilled deliveries in your personal chef account from all customers

(2) Register delivery - Update delivery of a fulfilled order through order number

(3) See past deliveries - Show history of all fulfilled deliveries in your account

(4) Show current dish menu and ratings - Show refreshed aggragate rating from all customers for each dish

(5) Show account information - Show account details and refreshed overall aggregate ratings of your profile

(6) Logout - Go to main chef page



