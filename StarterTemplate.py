'''
Starter template for programming coursework.

You must build your app by writing code for  the functions listed below.

Code for some of the functions has been provided.

The whole app is a composition of functions.

No GLOBAL variables and button functionality managed by use of lambda functions.

Student Name: ______Aayan Maskey______________

Student ID: ________W2121974______________

'''

import os
import csv
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

def load_pizza_prices(csv_file):
    """
    Reads a CSV file containing pizza names and their corresponding prices, 
    and loads the data into a dictionary.

    Args:
        csv_file (str): The relative or absolute path to the CSV file.

    Returns:
        dict: A dictionary where the keys are pizza names (str) and 
              the values are their prices (float).
    """
    pizza_prices = {}
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    name, price = row
                    pizza_prices[name.strip()] = float(price.strip())
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
    except Exception as e:
        print(f"Error reading pizza prices CSV: {e}")
    return pizza_prices

def save_images(path, image_dict):
    """
    Loads pizza images from a specified folder, resizes them, and stores 
    the images as ImageTk.PhotoImage objects in a dictionary.

    Args:
        path (str): The path to the folder containing the pizza image files.
        image_dict (dict): A dictionary where the keys are image filenames (without 
                           extensions) and the values are the corresponding ImageTk.PhotoImage 
                           objects representing the resized images.

    Notes:
        The images will be resized to a fixed size (e.g., 100x100 pixels). Only image 
        files with valid extensions (e.g., .png, .jpg, .jpeg) are considered.
    """
    VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')
    if not os.path.exists(path):
        print(f"Error: Image folder {path} not found.")
        return
    for file in os.listdir(path):
        if file.lower().endswith(VALID_IMAGE_EXTENSIONS):
            name = os.path.splitext(file)[0]
            try:
                img = Image.open(os.path.join(path, file)).resize((100, 100), Image.LANCZOS)
                image_dict[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image {file}: {e}")

def pizza_images_as_buttons(btn1, btn2, images, pizza_item_details_frame, item_details_frame, order_details_frame, pizza_cart, pizza_prices):
    """
    Displays pizza images as clickable buttons in a 4-column grid. 
    Each button represents a pizza, and when clicked, it loads the selected 
    pizza's image and details into the item_details_frame. This frame allows 
    users to add the pizza to the cart.

    Args:
        btn1 (Button): The "Show Pizzas" button, used to trigger the display of pizza buttons.
        btn2 (Button): The "Clear All Pizzas" button, used to clear all pizza buttons from the grid.
        images (dict): A dictionary containing pizza images, where keys are pizza names and 
                       values are ImageTk.PhotoImage objects.
        pizza_item_details_frame (Frame): The frame where pizza image buttons are displayed in a grid layout.
        item_details_frame (Frame): The frame where details of the selected pizza will be displayed, 
                                    including the "Add to Cart" button.
        order_details_frame (Frame): The frame that shows the contents of the user's cart.
        pizza_cart (dict): A dictionary to store the pizzas added to the cart. The keys are pizza names, 
                           and the values are dictionaries with pizza details (e.g., quantity, price).
        pizza_prices (dict): A dictionary where the keys are pizza names and the values are the corresponding pizza prices.

    Notes:
        - The pizza images are displayed in a 4-column grid layout. Each image is a clickable button.
        - When a pizza button is clicked, its image and details are displayed in the item_details_frame.
        - Users can specify the quantity of the selected pizza and add it to their cart, 
          which will be reflected in the order_details_frame.
    """
    clear_frame(pizza_item_details_frame)
    col = row = 0
    for name, image in images.items():
        if name not in pizza_prices:
            print(f"Warning: No price found for pizza {name}")
            continue
        btn = tk.Button(
            pizza_item_details_frame,
            image=image,
            text=name.capitalize(),
            compound='top',
            command=lambda n=name: load_image_in_frame(
                n, images[n], item_details_frame, order_details_frame, pizza_cart, pizza_prices
            )
        )
        btn.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        col += 1
        if col == 4:
            col = 0
            row += 1
    btn1.config(state='disabled')
    btn2.config(state='normal')

def load_image_in_frame(name, image, item_details_frame, order_details_frame, pizza_cart, pizza_prices):
    """
     Displays the details of the selected pizza in the pizza_detail_frame. 
    This includes the pizza's image, name, price, and a field for selecting 
    the quantity. Users can add the selected pizza to their cart.

    Args:
        name (str): The name of the selected pizza.
        image (PhotoImage): The image of the selected pizza (as a PhotoImage object).
        item_details_frame (Frame): The frame where the details of the selected pizza will be displayed, 
                                    including the image, name, price, quantity selector, and "Add to Cart" button.
        order_details_frame (Frame): The frame where the cart contents are displayed, updated after adding a pizza.
        pizza_cart (dict): A dictionary that stores the items in the user's cart. The keys are pizza names, 
                           and the values are dictionaries containing pizza details (e.g., quantity, price).
        pizza_prices (dict): A dictionary where the keys are pizza names and the values are the corresponding pizza prices.
    """
    clear_frame(item_details_frame)
    # Pizza image
    tk.Label(item_details_frame, image=image, bg='lightblue').grid(row=0, column=0, padx=10, pady=10, rowspan=2)
    # Pizza name and price
    tk.Label(
        item_details_frame,
        text=f"{name.capitalize()} - £{pizza_prices[name]:.2f}",
        font=("Arial", 12),
        bg='lightblue'
    ).grid(row=0, column=1, sticky='w', padx=10)
    # Quantity spinbox
    quantity_spin = tk.Spinbox(item_details_frame, from_=1, to=10, width=5, font=("Arial", 10))
    quantity_spin.grid(row=1, column=1, sticky='w', padx=10)

    def add_to_cart():
        """Add pizza to cart and update order details."""
        try:
            qty = int(quantity_spin.get())
            if qty < 1:
                raise ValueError("Quantity must be at least 1")
            pizza_cart[name] = {
                "quantity": qty,
                "price": pizza_prices[name],
                "image": image
            }
            clear_frame(item_details_frame)
            update_order_details_frame(order_details_frame, pizza_cart)
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid quantity: {e}")

    # Add to Cart button
    add_to_cart_button = ttk.Button(
        item_details_frame,
        text="Add to Cart",
        command=add_to_cart
    )
    add_to_cart_button.grid(row=2, column=1, pady=10, padx=5, sticky='w')
    # Cancel button to clear pizza_detail_frame
    cancel_button = ttk.Button(
        item_details_frame,
        text="Cancel",
        command=lambda: clear_frame(item_details_frame)
    )
    cancel_button.grid(row=2, column=0, pady=10, padx=5, sticky='e')

def update_order_details_frame(order_details_frame, pizza_cart):
    """
    Updates the order_details_frame with the contents of the pizza_cart in a scrollable canvas.
    Displays each pizza's name, quantity, price, and line total, along with the grand total.

    Args:
        order_details_frame (Frame): Frame to display cart items.
        pizza_cart (dict): Dictionary with cart items (pizza name, quantity, price, image).
    """
    clear_frame(order_details_frame)

    # Create a canvas and scrollbar
    canvas = tk.Canvas(order_details_frame, bg='lightgreen')
    scrollbar = ttk.Scrollbar(order_details_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='lightgreen')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    if not pizza_cart:
        tk.Label(
            scrollable_frame,
            text="Your cart is empty",
            font=("Arial", 12),
            bg='lightgreen'
        ).pack(pady=20)
        return

    # Order details
    tk.Label(
        scrollable_frame,
        text="Your order details:",
        font=("Arial", 12, "bold"),
        bg='lightgreen'
    ).grid(row=0, column=0, columnspan=4, padx=10, pady=5)
    row = 1
    total_price = 0.0
    for name, details in pizza_cart.items():
        quantity = details["quantity"]
        price = details["price"]
        line_total = quantity * price
        total_price += line_total
        tk.Label(scrollable_frame, image=details["image"], bg='lightgreen').grid(row=row, column=0, padx=5, pady=2)
        tk.Label(scrollable_frame, text=name.capitalize(), bg='lightgreen').grid(row=row, column=1, sticky='w')
        tk.Label(scrollable_frame, text=f"Qty: {quantity}", bg='lightgreen').grid(row=row, column=2, sticky='w')
        tk.Label(scrollable_frame, text=f"Total: £{line_total:.2f}", bg='lightgreen').grid(row=row, column=3, sticky='w')
        row += 1

    # Grand total
    tk.Label(
        scrollable_frame,
        text=f"Grand Total: £{total_price:.2f}",
        font=("Arial", 14, "bold"),
        bg='lightgreen'
    ).grid(row=row, column=0, columnspan=4, pady=10)
    # Buttons
    ttk.Button(
        scrollable_frame,
        text="Cancel",
        width=12,
        command=lambda: clear_cart(order_details_frame, pizza_cart)
    ).grid(row=row + 1, column=1, pady=10)
    ttk.Button(
        scrollable_frame,
        text="Confirm",
        width=12,
        command=lambda: confirm_order(order_details_frame, pizza_cart)
    ).grid(row=row + 1, column=2, pady=10)

def clear_all_frames(btn1, btn2, pizza_item_details_frame, item_details_frame, order_details_frame, pizza_cart, root):
    """
    Clears all frames except the menu_buttons_frame and sets the window background to red.

    Args:
        btn1 (Button): Show Pizzas button.
        btn2 (Button): Clear All Pizzas button.
        pizza_item_details_frame (Frame): Frame for displaying pizzas.
        item_details_frame (Frame): Frame for displaying pizza details.
        order_details_frame (Frame): Frame for displaying order details.
        pizza_cart (dict): Cart dictionary containing pizzas.
        root (Tk): Main application window.
    """
    clear_frame(pizza_item_details_frame)
    clear_frame(item_details_frame)
    clear_frame(order_details_frame)
    pizza_cart.clear()
    btn1.config(state='normal')
    btn2.config(state='disabled')
    root.configure(background='red')

def clear_frame(frame):
    """
    Clear all widgets from a frame.
    Args:
        frame (Frame): Frame to clear.
    """
    for widget in frame.winfo_children():
        widget.destroy()

def clear_cart(order_details_frame, pizza_cart):
    """
    Clear the cart and display empty cart message.
    Args:
        order_details_frame (Frame): Order details frame.
        pizza_cart (dict): Cart dictionary.
    """
    pizza_cart.clear()
    clear_frame(order_details_frame)
    tk.Label(
        order_details_frame,
        text="Your cart is empty",
        font=("Arial", 12),
        bg='lightgreen'
    ).pack(pady=20)

def confirm_order(order_details_frame, pizza_cart):
    """
    Confirm the order and display success message.
    Args:
        order_details_frame (Frame): Order details frame.
        pizza_cart (dict): Cart dictionary.
    """
    pizza_cart.clear()
    clear_frame(order_details_frame)
    tk.Label(
        order_details_frame,
        text="Order successfully placed!",
        font=("Arial", 12),
        bg='lightgreen'
    ).pack(pady=20)

def add_pizza():
    """Print message for Add New button."""
    print("Add New button activated")

def del_pizza():
    """Print message for Delete button."""
    print("Delete button activated")

def quitApp(myApp):
    """
    Quit the application after user confirmation.
    Args:
        myApp (Tk): Main application window.
    """
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        print("Quit button clicked")
        myApp.destroy()

def configure_style():
    """Configure button styles for consistent look."""
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", font=("Arial", 10))
    style.map("TButton",
              background=[('active', '#ddd'), ('disabled', '#eee')],
              foreground=[('active', '#000'), ('disabled', '#999')])

def create_frames(myApp):
    """
    Create and pack the four main frames with the desired layout.
    Args:
        myApp (Tk): Main application window.
    Returns:
        dict: Dictionary of frames.
    """
    # Top menu bar
    menu_frame = tk.Frame(myApp, bg='lightgray')
    menu_frame.pack(fill='x', padx=5, pady=5)

    # Center layout wrapper
    center_frame = tk.Frame(myApp, bg='red')
    center_frame.pack(fill='both', expand=True, padx=5, pady=5)

    # Pizza frame (left)
    pizza_frame = tk.Frame(center_frame, bg='red')
    pizza_frame.pack(side='left', fill='both', expand=True, padx=5)

    # Cart frame (right, fixed width)
    cart_frame = tk.Frame(center_frame, bg='lightgreen', width=400)
    cart_frame.pack(side='right', fill='y', padx=5)
    cart_frame.pack_propagate(False)

   
    # Inner cart content frame for dynamic content
    cart_content_frame = tk.Frame(cart_frame, bg='black')
    cart_content_frame.pack(fill='both', expand=True)

    # Item details frame (bottom)
    details_frame = tk.Frame(myApp, bg='green', height=150)
    details_frame.pack(fill='x', padx=5, pady=5)
    details_frame.pack_propagate(False)

    return {
        "menu": menu_frame,
        "pizza": pizza_frame,
        "details": details_frame,
        "cart": cart_content_frame
    }

def create_buttons(frame, myApp, allPizzaDict, pizza_item_details_frame, item_details_frame, order_details_frame, pizza_cart, pizza_prices):
    """
    Creates and packs buttons into the menu_buttons_frame.

    Args:
        frame (Frame): Menu buttons frame.
        myApp (Tk): Main application window.
        allPizzaDict (dict): Dictionary of pizza images.
        pizza_item_details_frame (Frame): Frame for displaying pizzas.
        item_details_frame (Frame): Frame for displaying pizza details.
        order_details_frame (Frame): Frame for displaying order details.
        pizza_cart (dict): Cart dictionary containing pizzas.
        pizza_prices (dict): Dictionary of pizza prices.
    """
    show_btn = ttk.Button(frame, text="Show Pizzas")
    clear_btn = ttk.Button(frame, text="Clear All Pizzas", state="disabled")
    show_btn.config(
        command=lambda: pizza_images_as_buttons(
            show_btn, clear_btn, allPizzaDict, pizza_item_details_frame,
            item_details_frame, order_details_frame, pizza_cart, pizza_prices
        )
    )
    clear_btn.config(
        command=lambda: clear_all_frames(
            show_btn, clear_btn, pizza_item_details_frame,
            item_details_frame, order_details_frame, pizza_cart, myApp
        )
    )
    show_btn.pack(side="left", padx=5, pady=5)
    clear_btn.pack(side="left", padx=5, pady=5)
    ttk.Button(frame, text="Add New", command=add_pizza).pack(side="left", padx=5, pady=5)
    ttk.Button(frame, text="Delete", command=del_pizza).pack(side="left", padx=5, pady=5)
    ttk.Button(frame, text="Quit", command=lambda: quitApp(myApp)).pack(side="left", padx=5, pady=5)

def main():
    """Main function to initialize and run the application."""
    myApp = tk.Tk()
    myApp.title("Online Pizza Store by Aayan Maskey(W2121974)")  
    myApp.geometry("1200x800")
    myApp.minsize(800, 600)
    myApp.configure(background="red")

    configure_style()
    frames = create_frames(myApp)
    pathAllPizza = 'allPizza/'
    pizza_prices_csv = "pizza_prices.csv"
    allPizzaDict, pizza_cart = {}, {}
    pizza_prices = load_pizza_prices(pizza_prices_csv)
    save_images(pathAllPizza, allPizzaDict)
    print(f"Number of pizza images loaded: {len(allPizzaDict)}")
    
    create_buttons(
        frames["menu"], myApp, allPizzaDict, frames["pizza"],
        frames["details"], frames["cart"], pizza_cart, pizza_prices
    )
    myApp.mainloop()

main()
