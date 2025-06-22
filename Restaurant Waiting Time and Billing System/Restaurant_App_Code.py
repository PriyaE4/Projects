from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import pygame
import cv2
import time
import os
import numpy as np

class RestaurantMenuApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Restaurant Menu")
        self.root.state('zoomed')  # Maximize the window
        self.ordered_items = []  # Initialize an empty list for ordered items
        self.customer_orders = []  # Initialize a list to store orders for each customer
        self.customer_count = 1  # Initialize customer count
        self.item_costs = {
            "Plain Dosa": 75,
            "Masala Dosa": 85,
            "Karam Dosa": 95,
            "Idly Sambar": 70,
            "Vada": 59,
            "Puri with egg": 200,
            "Butter Naan": 100,
            "Garlic Naan": 100,
            "Tandoori Roti": 80,
            "Rumali Roti": 90,
            "Veg Biryani": 235,
            "Chicken Biryani": 350,
            "Egg Fried rice": 180,
            "Pulao": 265,
            "Cheese Burger": 148,
            "Veggie Burger": 129,
            "Chicken Burger": 159,
            "Turkey Burger": 170,
            "Hamburger": 155,
            "Margherita": 269,
            "Pepperoni": 379,
            "BBQ Chicken": 449,
            "Veggie Delight": 239,
            "Four Cheese": 595,
            "Caesar Salad": 325,
            "Greek Salad": 259,
            "Garden Salad": 125,
            "Pasta Salad": 259,
            "Fruit Salad": 185,
            "Samosa": 84,
            "Pakora": 80,
            "Fries": 90,
            "Spring Rolls": 305,
            "Nachos": 309,
            "Orange Juice": 50,
            "Apple Juice": 55,
            "Mango Juice": 60,
            "Pineapple Juice": 60,
            "Mixed Fruit Juice": 90,
            "Chocolate": 140,
            "Black Currant": 169,
            "Butter Scotch": 160,
            "Wonder Vanilla": 185,
            "Tea": 50,
            "Coffee": 60,
            "Milk": 45,
            "Buttermilk": 50,
            "Lassi": 90,
            "Garlic bread": 100,
            "Chicken wings": 150,
            "Fish tacos": 250,
            "Avacado toast": 200,
            "Vanilla Icecream": 150,
            "Chocolate Icecream": 170,
            "Rocky road": 300,
            "Mango sorbet": 250,
            "Pistachio": 250,
            "Tomato soup": 160,
            "Corn soup": 150,
            "Chicken soup": 200,
            "Mushroom soup": 200,
            "Methi Chaman": 200,
            "Butter Chicken": 220,
            "Dal Makhani": 319,
            "Panner Butter Masala": 209
            
        }
        
        self.sound_file = "switch-sound.mp3"
        self.video_path = "back video.mp4"   # Load the background video
        self.video_label = Label(self.root)
        self.video_label.pack()
        pygame.mixer.init()    # Initialize the mixer
        self.play_video()       # Start video playback
        self.create_widgets()

    
    def play_video(self):
        cap = cv2.VideoCapture(self.video_path)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Load the logo image
        logo_image = cv2.imread("restaurant_logo11.png", cv2.IMREAD_UNCHANGED)

        # Check if the image was loaded successfully
        if logo_image is None or logo_image.size == 0:
            print("Error loading restaurant_logo11.png")
            self.start_app()
            return

        num_channels = logo_image.shape[2]  # Get the number of channels in the image

        # Get the dimensions of the logo image
        logo_height, logo_width = logo_image.shape[:2]

        # Initialize y with a default value
        y = (screen_height - logo_height) // 2

        # Create a font object
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text = "Ready to Savor a Delicious meal ?"  # Replace with the desired text

        # Get the total number of frames in the video
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Set the desired number of frames to display
        num_frames_to_display = 100  # Adjust this value to control the video duration

        frame_counter = 0
        while frame_counter < num_frames_to_display:
            ret, frame = cap.read()
            if not ret:
                break

            # Resize the frame to fit the entire screen
            frame = cv2.resize(frame, (screen_width, screen_height))

            # Create a blank image with the same dimensions as the frame
            overlay = np.zeros_like(frame)

            # Calculate the position to place the logo at the center
            x = (screen_width - logo_width) // 2

            # Overlay the logo image onto the blank image
            roi = overlay[y:y+logo_height, x:x+logo_width]
            roi[:] = logo_image[:, :, :3]  # Use only the first 3 channels (BGR)

            # Create a separate alpha channel for the overlay
            if num_channels == 3:
                roi = cv2.merge((roi, np.full_like(roi[:, :, 0], 255)))
            else:
                roi = cv2.merge((roi, logo_image[:, :, 3]))

            # Get the size of the text
            text_size, *_ = cv2.getTextSize(text, font, font_scale, font_thickness)
            # Calculate the position to place the text below the logo
            text_x = (screen_width - text_size[0]) // 2
            text_y = y + logo_height + 50  # Increase the gap by adjusting this value (previously 20)

            # Add the text to the overlay image
            cv2.putText(overlay, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)

            # Blend the logo and text with the frame using the alpha channel
            frame = cv2.addWeighted(frame, 1.0, overlay, 1.0, 0)

            # Convert the frame to RGB format for Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            self.root.update()
            time.sleep(0.03)  # Control the playback speed
            frame_counter += 1

        cap.release()
        self.start_app()    
    
    def start_app(self):
          # Clear the video label
        self.video_label.pack_forget()
        self.play_sound()
        self.create_widgets()

    def create_widgets(self):
        # Clear the current content
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Frame for category buttons
        self.button_frame = Frame(self.root, bg="lightgrey")
        self.button_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ns")

        # Create buttons for each category
        categories = [
            ("Soup", self.show_soup),
            ("Starters", self.show_starters),
            ("Salads", self.show_salads),
            ("Tiffins", self.show_tiffins),
            ("Flat Breads", self.show_flatbreads),
            ("Curries", self.show_curries),
            ("Rice", self.show_rice),
            ("Burgers", self.show_burgers),
            ("Pizzas", self.show_pizzas),
            ("Snacks", self.show_snacks),
            ("Juices", self.show_juices),
            ("Milkshake", self.show_milkshake),  
            ("Beverages", self.show_beverages),
            ("Icecreams", self.show_icecreams)
        ]

        for row, (category, command) in enumerate(categories):
            button = Button(self.button_frame, text=category, command=lambda c=command: self.button_click(c), width=20)
            button.grid(row=row, column=0, padx=10, pady=10)

        # Frame for displaying menu items
        self.content_frame = Frame(self.root, bg="white")
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Configure column and row weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Add a canvas and scrollbar
        self.canvas = Canvas(self.content_frame, bg="white")
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add Continue button
        self.continue_button = Button(self.root, text="Continue to Order", command=lambda: self.button_click(self.go_to_next_page), bg="lightgreen", fg="black", width=20)
        self.continue_button.grid(row=1, column=1, padx=10, pady=10)

    def play_sound(self):
        pygame.mixer.music.load(self.sound_file)
        pygame.mixer.music.play(0)

    def button_click(self, command):
        self.play_sound()
        command()

    def show_items(self, items):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for row, item in enumerate(items):
            image_path, name, prep_time, rating, cost = item
            self.add_menu_item(image_path, name, prep_time, rating, cost, row)

            # Reduce the vertical gap between items
            self.scrollable_frame.grid_rowconfigure(row, minsize=5)  # Adjust minsize as needed

    def add_menu_item(self, image_path, name, prep_time, rating, cost, row):
        try:
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            frame = Frame(self.scrollable_frame, bg="white", bd=2, relief="groove")
            frame.grid(row=row, column=0, padx=10, pady=10, sticky="w")

            image_label = Label(frame, image=photo, bg="white")
            image_label.photo = photo  # Keep a reference to avoid garbage collection
            image_label.grid(row=0, column=0, rowspan=3, padx=5, pady=5)

            name_label = Label(frame, text=name, font=("Comic Sans MS", 14), bg="white")
            name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

            rating_label = Label(frame, text=f"Rating: {rating}/5", font=("Comic Sans MS", 10), bg="white")
            rating_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

            cost_label = Label(frame, text=f"Cost: {cost}/-", font=("Comic Sans MS", 10), bg="white")
            cost_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

            time_label = Label(frame, text=f"Preparation Time: {prep_time} mins", font=("Comic Sans MS", 10), bg="white")
            time_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

            var = BooleanVar()
            checkbox = Checkbutton(frame, variable=var, command=lambda: self.checkbox_click(name, prep_time, var.get()))
            checkbox.grid(row=0, column=2, rowspan=3, padx=5, pady=5)

        except Exception as e:
            print(f"Error loading image for {name}: {e}")

    def checkbox_click(self, name, prep_time, checked):
        self.play_sound()
        self.add_to_order(name, prep_time, checked)

    def add_to_order(self, name, prep_time, checked):
        if checked:
            self.ordered_items.append((name, prep_time))
        else:
            self.ordered_items.remove((name, prep_time))

    def show_soup(self):
        self.show_items([
            ("Tomato soup.png", "Tomato soup", 15, 4.6, 160),
            ("Corn soup.png", "Corn soup", 13, 4.9, 150),
            ("Chicken soup.png", "Chicken soup", 18, 4.4, 200),
            ("Mushroom soup.png", "Mushroom soup", 20, 4.8, 200)
        ])

    def show_starters(self):
        self.show_items([
            ("Garlic bread.png","Garlic bread", 10, 4.3, 100),
            ("Chicken wings.png", "Chicken wings", 20, 4.6, 150),
            ("Fish tacos.png", "Fish tacos", 20, 4.6, 250),
            ("Avacado toast.png", "Avacado toast", 20, 4.5, 200)
        ])

    def show_salads(self):
        self.show_items([
            ("Caesar Salad.png", "Caesar Salad", 15, 4.3, 325),
            ("Greek Salad.png", "Greek Salad", 12, 4.2, 259),
            ("Garden Salad.png", "Garden Salad", 10, 4.1, 125),
            ("Pasta Salad.png", "Pasta Salad", 12, 4.5, 259),
            ("Fruit Salad.png", "Fruit Salad", 8, 4.6, 185)
        ])

    def show_tiffins(self):
        self.show_items([
            ("Plain Dosa.png", "Plain Dosa", 20, 4.5, 75),
            ("Masala Dosa.png", "Masala Dosa", 25, 4.8, 85),
            ("Karam Dosa.png", "Karam Dosa", 13, 4.2, 95),
            ("Idly Sambar.png", "Idly Sambar", 15, 4.4, 70),
            ("Vada.png", "Vada", 15, 4.0, 59)
        ])

    def show_flatbreads(self):
        self.show_items([
            ("Butter naan.png", "Butter Naan", 20, 4.5, 100),
            ("Garlic naan.png", "Garlic Naan", 25, 4.7, 100),
            ("Tandoori roti.png", "Tandoori Roti", 10, 4.3, 80),
            ("Rumali roti.png", "Rumali Roti", 7, 4.2, 90)
        ])

    def show_curries(self):
        self.show_items([
            ("methi chaman.png", "Methi Chaman", 30, 4.6, 200),
            ("Butter Chicken.png", "Butter Chicken", 50, 4.7, 220),
            ("Dal Makhani.png", "Dal Makhani", 45, 4.6, 319),
            ("panner butter masala.png", "Panner Butter Masala", 40, 4.8, 209)
        ])

    def show_rice(self):
        self.show_items([
            ("Veg Biryani.png", "Veg Biryani", 35, 4.6, 235),
            ("Chicken Biryani.png", "Chicken Biryani", 40, 4.8, 350),
            ("Egg Fried Rice.png", "Egg Fried rice", 25, 4.5, 180),
            ("Pulao.png", "Pulao", 30, 4.7, 265)
        ])

    def show_burgers(self):
        self.show_items([
            ("Cheese Burger.png", "Cheese Burger", 20, 4.4, 148),
            ("Veggie Burger.png", "Veggie Burger", 18, 4.2, 129),
            ("Chicken Burger.png", "Chicken Burger", 22, 4.6, 159),
            ("Turkey Burger.png", "Turkey Burger", 25, 4.7, 170),
            ("hamburger.png", "Hamburger", 24, 4.8, 155)
        ])

    def show_pizzas(self):
        self.show_items([
            ("Margherita.png", "Margherita", 20, 4.5, 269),
            ("Pepperoni.png", "Pepperoni", 25, 4.8, 379),
            ("BBQ Chicken.png", "BBQ Chicken", 30, 4.7, 449),
            ("Veggie Delight.png", "Veggie Delight", 22, 4.3, 239),
            ("Four Cheese.png", "Four Cheese", 35, 4.9, 595)
        ])

    def show_snacks(self):
        self.show_items([
            ("Samosa.png", "Samosa", 10, 4.3, 84),
            ("Pakora.png", "Pakora", 8, 4.2, 80),
            ("Fries.png", "Fries", 7, 4.4, 90),
            ("Spring Rolls.png", "Spring Rolls", 15, 4.6, 305),
            ("Nachos.png", "Nachos", 10, 4.5, 309)
        ])

    def show_juices(self):
        self.show_items([
            ("Orange Juice.png", "Orange Juice", 5, 4.1, 50),
            ("Apple Juice.png", "Apple Juice", 5, 4.2, 55),
            ("Mango Juice.png", "Mango Juice", 5, 4.3, 60),
            ("Pineapple Juice.png", "Pineapple Juice", 5, 4.3, 60),
            ("Mixed Fruit Juice.png", "Mixed Fruit Juice", 7, 4.5, 90)
        ])

    def show_milkshake(self) :
        self.show_items([
            ("chocolate.png", "Chocolate", 10, 4.7, 140),
            ("black currant.png","Black Currant", 15, 5, 169),
            ("butterscotch.png", "Butter Scotch", 13, 4.1, 160),
            ("wonder vanilla.png", "Wonder Vanilla", 20, 4.8, 185)
        ])

    def show_beverages(self):
        self.show_items([
            ("tea.png", "Tea", 10, 4.9, 50),
            ("coffee.png", "Coffee", 5, 5, 60),
            ("milk.png", "Milk", 2, 4.2, 45),
            ("buttermilk.png", "Buttermilk", 7, 4.6, 50),
            ("lassi.png", "Lassi", 9, 4.9, 90)
        ])

    def show_icecreams(self):
        self.show_items([
            ("Venilla Icescream.png", "Vanilla Icecream", 5, 4.2, 150),
            ("Chocolate Icescream.png", "Chocolate Icecream", 6, 5, 170),
            ("Rocky road.png","Rocky road", 10, 4.8, 300),
            ("Mango sorbet.png","Mango sorbet", 10, 4.5, 250),
            ("Pistachio.png","Pistachio", 20, 4.6, 250)
        ])


    def go_to_next_page(self):
        # Clear the current content
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_order_details()

    def calculate_waiting_time(self):
        prep_times = [int(item[1]) for item in self.ordered_items]
        max_prep_time = max(prep_times) if prep_times else 0
        current_time = datetime.datetime.now()
        total_cost = sum(self.item_costs[item[0]] for item in self.ordered_items)
        return max_prep_time, current_time, total_cost

    def create_order_details(self):
        # Remove the current content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Get the screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Create a new Toplevel window for full-screen display
        full_screen_window = Toplevel(self.root)
        full_screen_window.overrideredirect(True) # Remove window border and title bar
        full_screen_window.geometry(f"{screen_width}x{screen_height}+0+0") # Set the window size to cover the entire screen
        full_screen_window.attributes('-topmost', True) # Keep the window on top of all other windows

        # Set the background color of the full-screen window to white
        full_screen_window.configure(bg='white')

        # Add the background image
        photo = PhotoImage(file='black bg.png')
        clock_label = Label(full_screen_window, image=photo)
        clock_label.photo = photo # Keep a reference to avoid garbage collection
        clock_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create the order frame
        order_frame = Frame(full_screen_window, bg='white')
        order_frame.place(relx=0.5, rely=0.5, anchor='center') # Center the order_frame

        canvas = Canvas(order_frame, bg="white")
        canvas.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(order_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')

        scrollable_frame = Frame(canvas, bg='white')
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        customer_order_details = Label(scrollable_frame, text=f"Ordered Details of Customer {self.customer_count}:", font=("Comic Sans MS", 14, "bold"), bg='white')
        customer_order_details.pack()

        for item, prep_time in self.ordered_items:
            item_cost = self.item_costs.get(item, 0)
            item_label = Label(scrollable_frame, text=f"Preparation Time: {prep_time} mins - Food Item: {item} - Cost: {item_cost}/-", bg='white')
            item_label.pack()

        waiting_time, current_time, total_cost = self.calculate_waiting_time()

        time_label = Label(scrollable_frame, text=f"Waiting Time: {waiting_time} minutes", font=("Comic Sans MS", 14, "bold"), bg='white')
        time_label.pack(pady=10)

        current_time_label = Label(scrollable_frame, text=f"Ordered Time: {current_time.strftime('%I:%M %p')}", font=("Comic Sans MS", 14, "bold"), bg='white')
        current_time_label.pack(pady=10)

        estimated_completion_time = current_time + datetime.timedelta(minutes=waiting_time)
        estimated_time_label = Label(scrollable_frame, text=f"Estimated Completion Time: {estimated_completion_time.strftime('%I:%M %p')}", font=("Comic Sans MS", 14, "bold"), bg='white')
        estimated_time_label.pack(pady=10)

        total_cost_label = Label(scrollable_frame, text=f"Total Cost: {total_cost}/-", font=("Comic Sans MS", 14, "bold"), bg='white')
        total_cost_label.pack(pady=10)

        pay_button = Button(scrollable_frame, text="Pay", command=self.show_qr_code, bg="lavender", fg="black", width=10)
        pay_button.pack(pady=10)

        self.customer_orders.append((self.ordered_items[:], waiting_time, current_time, total_cost))
        self.ordered_items.clear()

    def show_qr_code(self):
        self.play_sound()
        # Clear current content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the background color of the root window to white
        self.root.configure(bg='white')

        # Create a frame to hold the QR code image and other widgets
        qr_frame = Frame(self.root, bg='white')
        qr_frame.pack(padx=10, pady=10)

        # Load the QR code image
        qr_image = Image.open("qr code.png")
        qr_photo = ImageTk.PhotoImage(qr_image)

        # Create a label to display the QR code image
        qr_label = Label(qr_frame, image=qr_photo, bg='white')
        qr_label.image = qr_photo  # Keep a reference to avoid garbage collection
        qr_label.pack()

        # Add the statement under the QR code
        thank_you_label = Label(qr_frame, text="Indulge in Excellence at Aroma Amara. Thank You for Visiting.", font=("Comic Sans MS", 14, "bold"), bg='white', fg='green')
        thank_you_label.pack(pady=10)

        # Create a label to display the payment success message
        payment_success_label = Label(qr_frame, text="", font=("Comic Sans MS", 14, "bold"), bg='white', fg='green')
        payment_success_label.pack(pady=10)

        # Schedule the payment success message to appear after 2 seconds
        self.root.after(2000, lambda: payment_success_label.config(text="Payment has been completed successfully"))

        # Add "Add Another Customer" button
        add_customer_button = Button(qr_frame, text="Add Another Customer", command=self.add_new_customer, bg="paleturquoise", fg="black", width=20)
        add_customer_button.pack(pady=10)

        # Add "Finished for the Day" button
        finished_for_day_button = Button(qr_frame, text="Finished for the Day", command=lambda: [self.button_click(self.show_daily_report), self.play_sound()], bg="lightcoral", fg="white", width=20)
        finished_for_day_button.pack(pady=10)

        # Center the window and adjust the size
        qr_frame.update_idletasks()  # Update the frame to get the correct size
        window_width = qr_frame.winfo_reqwidth()
        window_height = qr_frame.winfo_reqheight()
        position_x = (self.root.winfo_screenwidth() // 2) - (window_width // 2)
        position_y = (self.root.winfo_screenheight() // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Disable resizing
        self.root.resizable(False, False)

    def add_new_customer(self):
        self.customer_count += 1
        self.start_app()

    def show_daily_report(self):
        self.play_sound()
        
        # Clear current content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the main frame
        main_frame = Frame(self.root)
        main_frame.pack(expand=True, fill=BOTH)

        # Load the background image
        bg_image = Image.open("back.png")
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a label with the background image
        bg_label = Label(main_frame, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Calculate the required information
        num_orders = len(self.customer_orders)
        total_payments = sum(order[3] for order in self.customer_orders)

        # Create the report frame
        report_frame = Frame(main_frame, bg='white')
        report_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Create a canvas to hold the content
        canvas = Canvas(report_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Create a scrollbar
        scrollbar = Scrollbar(report_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create a frame inside the canvas to hold the content
        content_frame = Frame(canvas, bg='white')
        canvas.create_window((0, 0), window=content_frame, anchor='nw')

        # Configure scroll behavior
        content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add the content to the content_frame
        num_orders_label = Label(content_frame, text=f"Number of orders: {num_orders}", font=("Comic Sans MS", 14, "bold"), bg='white')
        num_orders_label.pack(pady=5)

        dotted_line_label = Label(content_frame, text="-------------------------------------------", font=("Comic Sans MS", 14), bg='white')
        dotted_line_label.pack(pady=5)

        payment_label = Label(content_frame, text=f"Number of payments: {num_orders}\nTotal Income: {total_payments}/-", font=("Comic Sans MS", 14, "bold"), bg='white')
        payment_label.pack(pady=5)

        dotted_line_label = Label(content_frame, text="-------------------------------------------", font=("Comic Sans MS", 14), bg='white')
        dotted_line_label.pack(pady=5)

        avg_waiting_time_label = Label(content_frame, text="Average Waiting Time of a Customer:", font=("Comic Sans MS", 14, "bold"), bg='white', fg='black')
        avg_waiting_time_label.pack(pady=10)

        self.timer_frame = Frame(content_frame, bg='black')
        self.timer_frame.pack(pady=20)

        self.clock_label = Label(self.timer_frame, font=('Arial', 48), bg='black', fg='white')
        self.clock_label.pack(pady=10)

        self.update_clock()

        dotted_line_label = Label(content_frame, text="-------------------------------------------", font=("Comic Sans MS", 14), bg='white')
        dotted_line_label.pack(pady=5)

        start_new_day_button = Button(content_frame, text="Start New Day", command=self.start_new_day, bg="palegoldenrod", fg="black", width=20)
        start_new_day_button.pack(pady=10)

        exit_button = Button(content_frame, text="Exit", command=self.root.destroy, bg="salmon", fg="white", width=20)
        exit_button.pack(pady=10)

        # Keep a reference to the PhotoImage object to prevent garbage collection
        self.bg_photo = bg_photo

    def update_clock(self):
        # Calculate the average waiting time
        num_orders = len(self.customer_orders)
        total_waiting_times = sum(order[1] for order in self.customer_orders)
        average_waiting_time = total_waiting_times / num_orders if num_orders > 0 else 0

        # Format the average waiting time as HH:MM:SS
        avg_minutes, avg_seconds = divmod(int(average_waiting_time * 60), 60)
        avg_hours, avg_minutes = divmod(avg_minutes, 60)

        # Update the clock label with the average waiting time
        avg_timer_text = "{:02}:{:02}:{:02}".format(avg_hours, avg_minutes, avg_seconds)
        self.clock_label.config(text=avg_timer_text)

    def start_new_day(self):
        self.customer_orders.clear()
        self.customer_count = 1
        self.start_app()


if _name_ == "_main_":
    root = Tk()
    app = RestaurantMenuApp(root)
    app.start_app()
    root.mainloop()
