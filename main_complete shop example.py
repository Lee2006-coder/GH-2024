import tkinter as tk
import sqlite3
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk  # Requires 'pillow' package

# Main window for the register and login buttons
main_window = tk.Tk()
main_window.title("Shoe Shop - Login/Register")
main_window.geometry("400x400")  # Set window size


# Function to register a user
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    if username and password and email:
        conn = sqlite3.connect('shoes_shop.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                       (username, password, email))
        conn.commit()
        conn.close()
        messagebox.showinfo("Registration", "Registration Successful!")
        register_window.destroy()  # Close the register window
    else:
        messagebox.showwarning("Input error", "All fields are required!")


# Function to open the register window
def open_register_window():
    global register_window, username_entry, password_entry, email_entry

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


# Function to log in a user
def login_user(main_window):
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('shoes_shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Login", "Login Successful!")
        login_window.destroy()  # Close the login window
        main_window.destroy()   # Close the main window
        open_shop_window()      # Open the shop window
    else:
        messagebox.showwarning("Login", "Invalid username or password")



# Function to open the login window
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


# Function to open the shop window
def open_shop_window():
    shop_window = tk.Tk()  # Create a new main window for the shop
    shop_window.title("Shoe Shop - Available Shoes")
    shop_window.geometry("800x600")  # Adjust size to fit images

    tk.Label(shop_window, text="Select a shoe to purchase:", font=("Helvetica", 16)).pack(pady=10)

    # List of shoes and their image file names
    shoes = [
        {"name": "Sneakers", "image": "sneakers.jpg"},
        {"name": "Boots", "image": "boots.jpg"},
        {"name": "Sandals", "image": "sandals.jpg"},
        {"name": "Heels", "image": "heels.jpg"},
        {"name": "Loafers", "image": "loafers.jpg"},
        {"name": "Flip-Flops", "image": "flipflops.jpg"}
    ]

    selected_shoe = tk.StringVar()
    selected_shoe.set(shoes[0]["name"])  # Set default selection

    # Create a frame to hold the shoe selection
    frame = tk.Frame(shop_window)
    frame.pack()

    # Iterate over the shoes and create widgets
    for index, shoe in enumerate(shoes):
        # Load and resize image
        image = Image.open(shoe["image"])
        image = image.resize((150, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Create a frame for each shoe and place it in a grid
        frame_shoe = tk.Frame(frame)
        frame_shoe.grid(row=index // 3, column=index % 3, padx=10, pady=10)  # Arrange in a 3-column grid

        label = tk.Label(frame_shoe, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

        tk.Radiobutton(frame_shoe, text=shoe["name"], variable=selected_shoe, value=shoe["name"]).pack()

    # Purchase button
    tk.Button(shop_window, text="Purchase", command=lambda: purchase_shoe(selected_shoe.get())).pack(pady=20)


# Function to handle shoe purchase
def purchase_shoe(selected_shoe):
    messagebox.showinfo("Purchase", f"You have selected {selected_shoe}. Purchase successful!")



 #Insert the Image of the shop
#image = Image.open("shop.jpg")
#image = image.resize((250, 150), Image.LANCZOS)
#photo = ImageTk.PhotoImage(image)

#image_label = tk.Label(main_window, image=photo)
#image_label.pack(pady=10)

tk.Label(main_window, text="Welcome to the Shoe Shop", font=("Helvetica", 16)).pack(pady=10)

Register_button = tk.Button(main_window, text="Register", width=15, command=open_register_window)
Register_button.pack(pady=10)

Login_button = tk.Button(main_window, text="Login", width=15, command=lambda: open_login_window(main_window))
Login_button.pack(pady=10)

main_window.mainloop()
