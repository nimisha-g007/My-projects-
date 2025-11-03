# Grocery Billing System - Mini Project
# Name: NIMISHA GOYAL
# Enrollment number:2502140050
# Course:B.Tech - First Year

# ---------------- Password Protection ----------------
PASSWORD = "admin123"  # Default password

# ---------------- Data Structures ----------------
products = {}  # Stores product details as {code: (name, price, quantity)}

# ---------------- Functions ----------------

def login():
    print("\n===== Welcome to Grocery Billing System =====")
    attempts = 3
    while attempts > 0:
        password = input("Enter password: ")
        if password == PASSWORD:
            print("Login successful!\n")
            main_menu()
            return
        else:
            attempts -= 1
            print(f"Incorrect password! Attempts left: {attempts}\n")
    print("Too many failed attempts. Exiting program.")


def add_product():
    code = input("Enter product code: ")
    if code in products:
        print("Product code already exists!\n")
        return

    name = input("Enter product name: ")
    price_input = input("Enter price: ")
    qty_input = input("Enter quantity: ")

    if price_input.replace('.', '', 1).isdigit() and qty_input.isdigit():
        price = float(price_input)
        qty = int(qty_input)
        if price > 0:
            products[code] = (name, price, qty)
            print(f"Product '{name}' added successfully with price ₹{price} and quantity {qty}!\n")
        else:
            print("Price must be a positive number. Product not added.\n")
    else:
        print("Invalid input! Price must be a number and quantity must be an integer.\n")


def modify_product():
    found = False
    code_to_modify = input("Enter product code to modify: ")

    for code, (name, price, qty) in products.items():
        if code == code_to_modify:
            found = True
            print(f"Current details: Name={name}, Price={price}, Quantity={qty}")

            new_name = input("Enter new name (leave blank to keep same): ") or name
            new_price_input = input("Enter new price (leave blank to keep same): ")
            new_qty_input = input("Enter new quantity (leave blank to keep same): ")

            if new_price_input == '' and new_qty_input == '':
                products[code] = (new_name, price, qty)
                print("Product updated successfully!\n")
            elif new_price_input.replace('.', '', 1).isdigit() and (new_qty_input == '' or new_qty_input.isdigit()):
                new_price = float(new_price_input) if new_price_input else price
                new_qty = int(new_qty_input) if new_qty_input else qty
                products[code] = (new_name, new_price, new_qty)
                print("Product updated successfully!\n")
            else:
                print("Invalid input!\n")
            break

    if not found:
        print("Product not found!\n")


def delete_product():
    code = input("Enter product code to delete: ")
    if code in products:
        removed = products.pop(code)
        print(f"Product '{removed[0]}' deleted successfully!\n")
    else:
        print("Product not found!\n")


def view_products():
    if not products:
        print("No products available.\n")
        return
    print("\n--- Product List ---")
    print(f"{'Code':<10}{'Name':<20}{'Price':<10}{'Qty':<10}")
    print("-" * 45)
    for code, (name, price, qty) in products.items():
        print(f"{code:<10}{name:<20}{price:<10}{qty:<10}")
    print()


def search_product():
    keyword = input("Enter product name or code to search: ").lower()
    found = False
    for code, (name, price, qty) in products.items():
        if keyword in code.lower() or keyword in name.lower():
            print(f"Found: Code={code}, Name={name}, Price={price}, Qty={qty}")
            found = True
    if not found:
        print("No matching product found.\n")


def generate_bill():
    bill = []
    total_amount = 0
    print("\n--- Generate Bill ---")

    while True:
        code = input("Enter product code (or 'done' to finish): ").lower()
        if code == 'done':
            break
        elif code not in products:
            print("Invalid product code!\n")
            continue
        name, price, qty = products[code]
        qty_input = input(f"Enter quantity for {name}: ")

        if qty_input.isdigit():
            qty_buy = int(qty_input)
            if qty_buy > qty:
                print("Not enough stock!\n")
                break
            else:
                total = price * qty_buy
                total_amount += total
                products[code] = (name, price, qty - qty_buy)
                bill.append((name, price, qty_buy, total))
                print(f"Added {qty_buy} x {name} to bill.\n")

                print("\n======= Final Bill =======")
                print(f"{'Name':<15}{'Price':<10}{'Qty':<10}{'Total':<10}")
                print("-" * 40)
                for name, price, qty, total in bill:
                    print(f"{name:<15}{price:<10}{qty:<10}{total:<10}")
                    print("-" * 40)
                    print(f"Grand Total: ₹{total_amount:.2f}\n")

        else:
            print("Invalid quantity!\n")


def main_menu():
    while True:
        print("""\n========= MAIN MENU =========
1.Add Product
2.Modify Product
3.Delete Product
4.View Products
5.Search Product
6.Generate Bill
7.Exit
=============================""")

        choice = input("Enter your choice (1-7): ")
        if choice == '1':
            add_product()
        elif choice == '2':
            modify_product()
        elif choice == '3':
            delete_product()
        elif choice == '4':
            view_products()
        elif choice == '5':
            search_product()
        elif choice == '6':
            generate_bill()
        elif choice == '7':
            print("Exiting program... Thank you!")
            break
        else:
            print("Invalid choice! Please select between 1-7.\n")

# ---------------- Main Program Execution ----------------
login()
