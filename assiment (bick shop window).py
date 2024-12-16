# assignment
import sqlite3 
import tkinter as tk
import qrcode
from symbol import parameters
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk


main_window = tk.Tk()
main_window.title("bicycle shop - login/register ")
main_window.geometry("300x300")

def register_user():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    if username and password and email:
        conn = sqlite3.connect('bicycle_shop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customer (username, password, email) VALUES (?, ?, ?)",
                       (username, password, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Registration", "Registration Successful!")
        register_window.destroy()
    else:
        messagebox.showwarning("Input error", "All fields are required!")

def open_register_window():
    global register_window, register_user, username_entry,password_entry,email_entry,main_window

    register_window = tk.Toplevel()
    register_window.title("Register")
    register_window.geometry('400x300')

    tk.Label(register_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(register_window, show='*')
    password_entry.pack(pady=5)

    tk.Label(register_window, text="Email").pack(pady=5)
    email_entry = tk.Entry(register_window)
    email_entry.pack(pady=5)

    tk.Button(register_window, text="Register", command=register_user).pack(pady=10)

def login_user(main_window):
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('bicycle_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Login", "Login Successful!")
        login_window.destroy()
        main_window.destroy()
        open_shop_window()
    else:
        messagebox.showwarning("Login", "Invalid username or password")

def open_login_window(main_window):
    global login_window, username_entry, password_entry

    login_window = tk.Toplevel()
    login_window.title("Login")
    login_window.geometry('300x200')

    tk.Label(login_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=lambda: login_user(main_window)).pack(pady=10)

def open_shop_window():
    shop_window = tk.Tk()
    shop_window.title("bicycle Shop - Available bicycle")
    shop_window.geometry("800x600")

    tk.Label(shop_window, text="Select a bicycle product to purchase:", font=("Helvetica", 16)).pack(pady=10)

    bicycle = [
        {"name": "small bicycle","price" : "50", "picture":"small_bicycle.JPG"},
        {"name": "normal  bicycle","price" : "100", "picture":"normal_bicycle.JPG"},
        {"name" : "off road bicycle","price" : "200", "picture":"mountain_bicycle.JPG"},
        {"name" : "bicycle helmet ", "price" :" 30", "picture":"bic_hat.JPG"},
        {"name" : "Hi_Vis_Vest ", "price" : "30", "picture":"hi_vis_vest.JPG"},
        {"name" : "water bottle ", "price" : "15", "picture":"water_bottle.JPG"},
    ]

    selected_bicycle = tk.StringVar()
    selected_bicycle.set(bicycle[0]["name"])

    frame = tk.Frame(shop_window)
    frame.pack()

    basket = []
    def add_to_basket(bicycle):
        basket.append(bicycle)
        messagebox.showinfo("basket", f"added{bicycle['name']}to basket")

    for index, bicycle in enumerate(bicycle):
        image = Image.open(bicycle["picture"])
        image = image.resize((150, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        frame_bicycle = tk.Frame(frame)
        frame_bicycle.grid(row=index // 3, column=index % 3, padx=10, pady=10)

        label = tk.Label(frame_bicycle, image=photo)
        label.image = photo
        label.pack()

        tk.Radiobutton(frame_bicycle, text=bicycle["name"], variable=selected_bicycle, value=bicycle["name"]).pack()



    tk.Button(shop_window, text="Purchase", command=lambda: purchase_bicycle(selected_bicycle.get(), 1)).pack(pady=20)
# Function to view the basket
def view_basket(basket):
    basket_window = tk.Toplevel()
    basket_window.title("Your Basket")
    basket_window.geometry("400x400")

    tk.Label(basket_window, text="Your Basket", font=("Helvetica", 16)).pack(pady=10)

    total_price = 0
    for bicycle in basket:
        tk.Label(basket_window, text=f"{bicycle['name']} - ${bicycle['price']}").pack()
        total_price += bicycle['price']

    tk.Label(basket_window, text=f"Total: ${total_price}", font=("Helvetica", 14)).pack(pady=10)

    tk.Button(basket_window, text="Purchase", command=lambda: complete_purchase(basket, basket_window)).pack(pady=20)

#Function to complete purchase
def complete_purchase(basket, basket_window):
    basket_window.destroy()  # Close the basket window
    purchase_bicycle(basket, 1)
def purchase_bicycle(selected_bicycle, basket=None):
    purchase_bicycle = tk.Toplevel()
    purchase_bicycle.title("Payment")
    purchase_bicycle.geometry("400x500")
    tk.Label(purchase_bicycle, text="Review Your Order", font=("Helvetica", 16)).pack(pady=10)

    total_price = 0
    for bicycle in basket:
        tk.Label(purchase_bicycle, text=f"{bicycle['name']} - ${bicycle['price']}").pack()
        total_price += bicycle['price']

    tk.Label(purchase_bicycle, text=f"Total: ${total_price}", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(purchase_bicycle, text="Enter Payment Details", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(purchase_bicycle, text="Card Number").pack(pady=5)
    card_number_entry = tk.Entry(purchase_bicycle)
    card_number_entry.pack(pady=5)

    tk.Label(purchase_bicycle, text="Expiration Date (MM/YY)").pack(pady=5)
    expiration_entry = tk.Entry(purchase_bicycle)
    expiration_entry.pack(pady=5)

    tk.Label(purchase_bicycle, text="CVV").pack(pady=5)
    cvv_entry = tk.Entry(purchase_bicycle, show='*')
    cvv_entry.pack(pady=5)

    def confirm_payment():
        card_number = card_number_entry.get()
        expiration_date = expiration_entry.get()
        cvv = cvv_entry.get()

        if card_number and expiration_date and cvv:
            messagebox.showinfo("Payment", "Payment Successful! Thank you for your purchase.")
            purchase_bicycle.destroy()  # Close the payment window
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    tk.Button(purchase_bicycle, text="Confirm Payment", command=confirm_payment).pack(pady=20)

    messagebox.showinfo("Purchase", f"You have selected {selected_bicycle}. Purchase successful!")

    image = Image.open("shop.jpg")
    image = image.resize((250, 150), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)


# qr quode
data = "https://www.google.com/search?q=bicycle&rlz=1C1GCEA_enGB1139GB1140&oq=&gs_lcrp=EgZjaHJvbWUqCQgCEEUYOxjCAzIJCAAQRRg7GMIDMgkIARBFGDsYwgMyCQgCEEUYOxjCAzIJCAMQRRg7GMIDMgkIBBBFGDsYwgMyCQgFEEUYOxjCAzIJCAYQRRg7GMIDMhEIBxAAGAMYQhiPARi0AhjqAtIBCTI1NDJqMGoxNagCCLACAQ&sourceid=chrome&ie=UTF-8"

QRCodefile = "discount.png"

QRimage = qrcode.make(data)

QRimage.save(QRCodefile)

tk.Label(main_window, text="Welcome to the bicycle Shop", font=("Helvetica", 16)).pack(pady=10)

Register_button = tk.Button(main_window, text="Register", width=20, command=open_register_window)
Register_button.pack(pady=10)

Login_button = tk.Button(main_window, text="Login", width=20, command=lambda: open_login_window(main_window))
Login_button.pack(pady=10)

main_window.mainloop()
