import mysql.connector
from datetime import date
import random
import string
cnx=mysql.connector.connect(host="localhost",username="root",password="root123",database="first1")



# Create a cursor object to execute SQL queries
cursor = cnx.cursor()
ch = int(0)

def authentication(a):
    if a=="A":
        # authenticate admin login
        def adminauthen():
            admin_ID = str(input("Enter admin ID: "))
            admin_password = str(input("Enter admin password: "))
            query = "SELECT * FROM admin WHERE Admin_ID = %s AND Admin_Password = %s"
            cursor.execute(query, (admin_ID, admin_password))
            admin_data = cursor.fetchone()
            if admin_data:
                print("Admin login successfull!")
                global ch
                ch = 1 

            else:
                print("InvalID admin credentials.") 
        adminauthen()

    elif a=="C":
        # authenticate customer login    
        def customerauthen():
            global customer_ID
            customer_ID = str(input("Enter customer ID: "))
            global customer_fname
            customer_fname = str(input("Enter customer first name: "))
            customer_lname = str(input("Enter customer last name: "))
            sql = "SELECT * FROM customer WHERE Customer_ID = %s AND Customer_First_Name = %s AND Customer_Last_Name = %s"
            cursor.execute(sql, (customer_ID, customer_fname, customer_lname))
            customer_data = cursor.fetchone()
            if customer_data:
                print("Customer login successfull")
                global ch
                ch = 1 
            else:
                print("InvalID customer credentials.")
        customerauthen()



# Define a function to retrieve all Products from the database
def get_Products():
    query = "SELECT * FROM Product"
    cursor.execute(query)
    Products = cursor.fetchall()
    for Product in Products:
        print(Product)

# Define a function to add a new Product to the database
def add_Product():
    Product_ID = input("Enter Product ID")
    Product_name = input("Enter Product name: ")
    Product_price = float(input("Enter Product price: "))
    Product_categoryID = int(input("Enter Product's category ID "))
    Product_quantity = int(input("Enter Product quantity"))
    query = "INSERT INTO Product (ID,name1,price,categoryID,quantity) VALUES (%s, %s, %s, %s, %s )"
    # values = (Product_ID, Product_name, Product_price, Product_categoryID, Product_quantity)
    cursor.execute("INSERT INTO product (product.Product_ID,product.Product_Name,product.Product_price,`product`.`Category_ID(fk)`,product.Product_Quantity) VALUES (%s, %s, %s, %s, %s )", (Product_ID, Product_name, Product_price, Product_categoryID, Product_quantity))
    cnx.commit()
    print("Product added successfully!")

# Define a function to update an existing Product in the database
def update_Product():
    Product_ID = input("Enter Product ID")
    Product_name = input("Enter Product name: ")
    Product_price = float(input("Enter Product price: "))
    Product_categoryID = int(input("Enter Product's category ID "))
    Product_quantity = int(input("Enter Product quantity"))
    if (Product_price and Product_quantity) !=0:
        
        query = "UPDATE product SET product.Product_Name=%s, product.Product_price=%s, `product`.`Category_ID(fk)`=%s, product.Product_Quantity=%s WHERE product.Product_ID=%s"
        values = (Product_name, Product_price, Product_categoryID, Product_quantity  ,Product_ID)
        cursor.execute(query, values)
        cnx.commit()
        print("Product updated successfully!")
    else:
        print("Price and quantity can't be zero.")

# Define a function to delete a Product from the database
def delete_Product():
    
    cursor.execute("DELETE FROM product WHERE product.Product_ID = 'fge34' ")

    cnx.commit()
    print("Product deleted successfully!")

def delete_Category():
    
    # cursor.execute("DELETE FROM category WHERE category.Category_ID = '476' ")

    # cnx.commit()
    print("Category deleted successfully!")

def selectvalIDcoupons():
    query = "SELECT * FROM Coupons WHERE Expiration_Date > %s AND is_used = 0 AND Coupon_ID NOT IN (SELECT Coupon_ID FROM Coupons WHERE Expiration_Date < %s)"
    cursor.execute(query, (date.today(), date.today()))
    results = cursor.fetchall()
    for row in results:
        print(row)
    cnx.commit()

def paymentdetails():
    query = "SELECT Payment.Payment_Mode, Payment.payment_Address FROM Payment JOIN `order` ON Payment.Payment_ID = `order`.`Payment_ID(fk)` WHERE `order`.`Order_ID` = 'af1-79f'"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    cnx.commit()

def postpaIDorder():
    query = "SELECT SUM(Total_Cost), delivery_date FROM `order` JOIN Payment p ON p.payment_ID = `order`.`payment_ID(fk)` WHERE payment_mode = 'Cash' GROUP BY delivery_date ORDER BY delivery_date"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    cnx.commit()

def totalcartcost():
    query = "SELECT SUM(Cart_Cost) FROM cart WHERE Cart_ID = 'abz-31ii2'"
    cursor.execute(query)
    result = cursor.fetchone()
    print(result[0])
    cnx.commit()

def cancelorder():
    update_query = "UPDATE Customer SET `Order_ID(fk)` = NULL WHERE `Order_ID(fk)` = 'ai4-45y';"
    cursor.execute(update_query)
    print("Order deleted successfully!")

def deleteorder():
    delete_query = "DELETE FROM `Order` WHERE `Payment_ID(fk)` IN (SELECT Payment_ID FROM Payment WHERE Payment_ID = '57r-3y');"
    cursor.execute(delete_query)
    print("Order deleted successfully!")


def selectcancelledorder():
    select_query = "SELECT * FROM `Order` WHERE `Payment_ID(fk)` = '57r-3y';"
    cursor.execute(select_query)
    cancelled_order = cursor.fetchall()
    print(cancelled_order)

def ProductsincartID():
    select_query = "SELECT Product.Product_name, cart.quantity FROM Product JOIN cart ON Product.Product_ID = cart.`Product_ID(fk)` WHERE cart.Cart_ID = 'abz-31ii2';"
    cursor.execute(select_query)
    Products_in_cart = cursor.fetchall()
    print(Products_in_cart)

def constraints():
    try:
    # phone number can't be greater than 10 digits
        cursor.execute("""INSERT into Customer(Customer_ID, Customer_First_Name, Customer_Last_Name, Customer_User_Name, Customer_Email, Customer_Phone_Number, Customer_Address, Customer_Status, `Cart_ID(fk)`) 
                        values ('aay-03','Sarvagya', 'Kaushik','SarvK','abc@gma.com','12345678910','patiala','Normal','abh-51cn3')""")
    except mysql.connector.errors.DataError as e:
        print(f"Constraint error: {e}")

    try:
    # price can't be zero and quantity can be zero
        cursor.execute("insert into Product(Product_ID, Product_name, Product_Price, `Category_ID(fk)`, Product_Quantity) values ('000-88-829', 'Charger',0, 46, 0)")
    except mysql.connector.errors.DataError as e:
        print(f"Constraint error: {e}")


    cnx.commit()

def olapqueries():
    # Query 1 What are the total sales for each product category?
    query = """
        SELECT category.Category_Name, SUM(product.Product_price * cart.Quantity) as total_sales
        FROM category
        JOIN product ON category.Category_ID = product.`Category_ID(fk)`
        JOIN cart ON product.Product_ID = cart.`Product_ID(fk)`
        GROUP BY category.Category_Name;
        """
    cursor.execute(query)
    for (name, total_sales) in cursor:
        print("{}: {}".format(name, total_sales))
    print("\n")
    


    # Query 2 Which customers have the highest order value?
    query = """
    SELECT customer.Customer_first_name, customer.Customer_last_name, SUM(cart.Cart_cost) as total_order_value
    FROM customer
    JOIN cart ON customer.`Cart_ID(fk)` = cart.Cart_ID
    GROUP BY customer.Customer_ID
    ORDER BY total_order_value DESC;
    """
    cursor.execute(query)
    for (first_name, last_name, total_order_value) in cursor:
        print("{} {}: {}".format(first_name, last_name, total_order_value))
    print("\n")
    

    # Query 3 Which products have the highest discount usage?
    query = """
    SELECT product.Product_name, coupons.Discount, coupons.is_used
    FROM product
    JOIN cart ON product.Product_ID = cart.`Product_ID(fk)`
    JOIN coupons ON cart.`Coupon_ID(fk)` = Coupons.Coupon_ID
    ORDER BY coupons.is_used DESC;
    """
    cursor.execute(query)
    for (name, discount, no_used) in cursor:
        print("{}: {} ({} used)".format(name, discount, no_used))
    print("\n")

    # # Query 4
    
    # What is the average revenue generated by each product?



    cursor.execute("""
    SELECT product.Product_Name, AVG(product.Product_Price * Cart.Quantity) AS Avg_Revenue
    FROM product
    INNER JOIN cart ON product.Product_ID = cart.`Product_ID(fk)`
    GROUP BY product.Product_Name;
    """)
    result = cursor.fetchall()
    for row in result:
        print(row)

 


    

    # # Query 5
    #  total revenue generated by each category of products
    cursor.execute("""
        SELECT category.Category_Name, SUM(product.Product_Price * cart.Quantity) AS Total_Revenue
        FROM product
        INNER JOIN cart ON product.Product_ID = cart.`Product_ID(fk)`
        INNER JOIN category ON product.`Category_ID(fk)` = category.Category_ID
        GROUP BY category.Category_Name;
        """)
    result = cursor.fetchall()
    for row in result:
        print(row)

def add_to_cart():

    print("Press 1 for adding products to cart and 0 when you are about to complete (the product to be added is the last one. )")
    n = int(1)

    # Generate a random cart_id
    cart_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    while(n!=0):
        n= int(input())
        # product_name = input("Enter product name: ") 
        
        quantity = int(input("Enter quantity: "))
    

        # Check if the product exists and has sufficient quantity
        cursor.execute("SELECT product.Product_Quantity, product.Product_ID FROM product WHERE product.Product_name = 'Poppy Seed' ") 
        result = cursor.fetchone()
        if result is None:

            print("Invalid product ID, Try again")
            return
        elif result[0] < quantity:
            print("Insufficient quantity, Try again.")
            return
        product_id = result[1]
        query = "SELECT customer.Customer_Status FROM customer WHERE customer.Customer_ID = %s AND customer.Customer_First_Name = %s AND customer.Customer_Status IN ('Prime', 'Elite')"
        values = (customer_ID, customer_fname)
        cursor.execute(query, values)

        # fetch all the results and print them
        results = cursor.fetchall()
        if results:
                print("YOU are eligible for applying coupon.")
                n1 =int(input("Enter 0 if you don't want and 1 if you want to apply coupon."))
                if n1==1:
                    coupon_ID = int(input("Give the coupon ID: "))
                else:
                    coupon_ID = 0
                    
        else:
            print("SORRY, as per your current status you are not eligible for coupons.")
            coupon_ID = None
        
        cursor.execute("SELECT product.Product_Price, product.Product_Quantity FROM product WHERE product.Product_Name = 'Poppy Seed' ")
        result1 = cursor.fetchall()
        product_price = result1[0]
        # product_quantity = result1[1]

        # Calculate the cart cost
        cart_cost = product_price * quantity

       

        # Insert the new row into the cart table
        cursor.execute("INSERT INTO cart (cart.Cart_ID, cart.Cart_Cost, cart.`Product_ID(fk)`, `cart`.`Coupon_ID(fk)`, cart.Quantity) VALUES (%s, %s, %s, %s, %s)", (cart_id, cart_cost, product_id, coupon_ID, quantity))

        print("Product added to cart successfully.")
        # Update the product table with the new quantity
        # new_quantity = product_quantity - quantity
        # query = "UPDATE product SET product.Product_Price = %s, product.Product_Quantity = %s WHERE product.Product_ID = %s"
        # values = (product_price, new_quantity, product_id)
        # cursor.execute(query, values)

        # Close the cursor and connection
        cursor.close()
        cnx.commit()



# Define a function to display the main menu
def display_menu(a):
    
    
    if a=="A":
        print("1. View Products")
        print("2. Add a Product")
        print("3. Update a Product")
        print("4. Delete a Product")
        print("5. Delete a Category")
        print("6. Select Products of a category")
        print("8. Payment details based on order id")
        print("9. PostpaID orders filtered by date")
        print("12. Delete from Order table based on Payment_ID and mark Order as cancelled")
        print("13. Select the cancelled order")
        print("14. Select Products and quantity from Product and Cart tables based on cart_ID")
        print("15. Constraints in our database")
        print("16. OLAP queries")
        print("18. Exit" )
    elif a=="C":
        print("1. View Products")
        print("7. Select valID coupons")
        print("10. Total Cart Cost of a Customer")
        print("11. Cancel order")
        print("17. Build cart by adding products" )
        print("18. Exit" )


    

# Define a function to handle user input
def get_user_input():
    choice = input("Enter your choice: ")
    if choice == "1":
        get_Products()
    elif choice == "2":
        add_Product()
    elif choice == "3":
        update_Product()
    elif choice == "4":
        delete_Product()
    elif choice == "5":
        delete_Category()
    elif choice =="6":
        paymentdetails()
    elif choice =="7":
        selectvalIDcoupons()
    elif choice =="8":
        paymentdetails()
    elif choice =="9":
        postpaIDorder()
    elif choice =="10":
        totalcartcost()
    elif choice =="11":
        cancelorder()
    elif choice =="12":
        deleteorder()
    elif choice =="13":
        selectcancelledorder()
    elif choice =="14":
        ProductsincartID()
    elif choice =="15":
        constraints()
    elif choice =="16":
        olapqueries()
    elif choice =="17":
        add_to_cart()
    elif choice == "18":
        exit()
    else:
        print("InvalID choice. Please try again.")


while(ch==0):
    a=input("First choose whether want to enter as Admin (type A) or Customer (type C)")
    if a=="A" or "C":
            authentication(a)
            # print(ch)
    else:
            print("Invalid Choice. Please try again")

# Display the main menu and handle user input
while True:
    display_menu(a)
    get_user_input()
