####
# Grocery Billing System with SQLite3 Database
# Name: NIMISHA GOYAL
# Enrollment number:2502140050

import sqlite3

# ---------------- Database Setup ----------------
def connect_db():
    conn = sqlite3.connect("grocery.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            code TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            quantity INTEGER
        )
    """)
    conn.commit()
    return conn

conn = connect_db()
cursor = conn.cursor()

# ---------------- Password Protection ----------------
PASSWORD = "admin123"

# ---------------- Functions ----------------

def login():
    print("\n===== Welcome to Grocery Billing System =====")
    attempts = 3
    while attempts > 0:
        pwd = input("Enter password: ")
        if pwd == PASSWORD:
            print("Login Successful!")
            menu()
            return
        else:
            attempts -= 1
            print(f"Wrong password! Attempts left: {attempts}")
    print("Too many failed attempts. Exiting...")

def add_product():
    code = input("Enter product code: ")
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    qty = int(input("Enter quantity: "))
    cursor.execute("INSERT OR REPLACE INTO products VALUES (?,?,?,?)",
                   (code, name, price, qty))
    conn.commit()
    print("Product added to database!\n")

def modify_product():
    code = input("Enter product code to modify: ")
    cursor.execute("SELECT * FROM products WHERE code=?", (code,))
    product = cursor.fetchone()
    if not product:
        print("Product not found!\n")
        return
    print("\nLeave field blank if you don’t want to change it.")
    new_name = input(f"Enter new name ({product[1]}): ").strip()
    new_price = input(f"Enter new price ({product[2]}): ").strip()
    new_qty = input(f"Enter new quantity ({product[3]}): ").strip()
    # Keep old values if blank
    new_name = new_name if new_name else product[1]
    new_price = float(new_price) if new_price else product[2]
    new_qty = int(new_qty) if new_qty else product[3]

    cursor.execute("""
        UPDATE products 
        SET name=?, price=?, quantity=? 
        WHERE code=?
    """, (new_name, new_price, new_qty, code))

    conn.commit()
    print("Product updated successfully!\n")

def delete_product():
    code = input("Enter product code to delete: ")
    cursor.execute("SELECT * FROM products WHERE code=?", (code,))
    product = cursor.fetchone()
    if not product:
        print("Product not found!\n")
        return
    confirm = input("Are you sure you want to delete this product? (y/n): ")
    if confirm.lower() == 'y':
        cursor.execute("DELETE FROM products WHERE code=?", (code,))
        conn.commit()
        print("Product deleted successfully!\n")
    else:
        print("Deletion cancelled.\n")

def view_products():
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    print("\n--- Product List ---")
    for r in rows:
        print(r)
    print()

def search_product():
    code = input("Enter product code to search: ")
    cursor.execute("SELECT * FROM products WHERE code=?", (code,))
    result = cursor.fetchone()
    if result:
        print("Product Found:", result)
    else:
        print("Product not found!")
    print()

def generate_bill():
    total = 0
    bill_items = []
    while True:
        code = input("Enter product code (or 'done' to finish): ")
        if code.lower() == "done":
            break
        cursor.execute("SELECT * FROM products WHERE code=?", (code,))
        item = cursor.fetchone()
        if item:
            print(f"{item[1]} - Rs.{item[2]}")
            qty = int(input("Enter quantity: "))
            if qty <= item[3]:
                amount= item[2] * qty
                total += amount
                cursor.execute("UPDATE products SET quantity = quantity - ? WHERE code=?", (qty, code))
                conn.commit()
                bill_items.append([item[0], item[1], qty, amount])
                print("{:<10} {:<15} {:<10} {:<10}".format(item[0], item[1], qty, amount))
            else:
                print("Insufficient stock!")
        else:
            print("Invalid product code!")
    print("\n================= BILL =================")
    print("{:<10} {:<15} {:<10} {:<10}".format("Code", "Name", "Qty", "Amount"))
    print("----------------------------------------")
    for row in bill_items:
        print("{:<10} {:<15} {:<10} {:<10}".format(row[0], row[1], row[2], row[3]))
    print("----------------------------------------")
    print(f"Total Bill Amount: Rs.{total}")
    print("========================================\n")

def menu():
    while True:
        print("===== MENU =====")
        print("1. Add Product")
        print("2. Modify Product")
        print("3. Delete Product")
        print("4. View Products")
        print("5. Search Product")
        print("6. Generate Bill")
        print("7. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            add_product()
        elif ch == "2":
            modify_product()
        elif ch == "3":
            delete_product()
        elif ch == "4":
            view_products()
        elif ch == "5":
            search_product()
        elif ch == "6":
            generate_bill()
        elif ch == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")

# ---------------- Main Program Execution ----------------
login()
