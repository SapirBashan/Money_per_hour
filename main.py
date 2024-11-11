import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

# Settings
hourly_rate = 82.7  # Set your hourly rate in Shekels here

# Variables
start_time = None
custom_start_time_entry = None  # Entry field for custom start time
earnings = 0

# Function to start tracking with optional custom start time
def start_work():
    global start_time
    custom_time = custom_start_time_entry.get()
    if custom_time:
        try:
            start_time = datetime.strptime(custom_time, "%H:%M").replace(
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day
            )
        except ValueError:
            result_label.config(text="Invalid time format! Use HH:MM.")
            return
    else:
        start_time = datetime.now()

    result_label.config(text="Started working...")
    update_earnings()  # Start updating the earnings every second

# Function to end tracking
def end_work():
    global start_time, earnings
    if start_time:
        current_time = datetime.now()
        elapsed_time = current_time - start_time
        hours_worked = elapsed_time.total_seconds() / 3600
        earnings = hours_worked * hourly_rate
    start_time = None  # Reset the start time to stop tracking
    current_time2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result_label.config(text=f"WORK FINISHED!!!\nTime worked: {format_time(elapsed_time)}\nEarnings: ₪{earnings:.2f}\nCurrent time: {current_time2}")

# Function to update earnings every second
def update_earnings():
    global start_time
    if start_time:
        current_time = datetime.now()
        current_time2 = current_time.strftime('%Y-%m-%d %H:%M:%S')
        elapsed_time = current_time - start_time
        hours_worked = elapsed_time.total_seconds() / 3600

        # Define the target time (16:24 in this case) as a datetime object
        target_time = datetime.combine(start_time.date(), datetime.strptime("16:24", "%H:%M").time())

        # Calculate earnings based on when work was done
        if current_time >= target_time:
            # Time worked before 16:24
            before_16_24 = max((target_time - start_time).total_seconds() / 3600, 0)
            # Time worked after 16:24
            after_16_24 = hours_worked - before_16_24
            # Calculate earnings
            earnings = (before_16_24 * hourly_rate) + (after_16_24 * hourly_rate * 1.25)
        else:
            # All time is before 16:24, so regular rate applies
            earnings = hours_worked * hourly_rate

        # Update result label with the current earnings
        result_label.config(text=f"Time worked: {format_time(elapsed_time)}\nEarnings: ₪{earnings:.2f}\nCurrent time: {current_time2}")

        # Schedule the next update after 1 second
        result_label.after(1000, update_earnings)

# Function to format the elapsed time without milliseconds
def format_time(time_delta):
    return str(timedelta(seconds=int(time_delta.total_seconds())))

# Setting up the GUI
root = tk.Tk()
root.title("Daily Earnings Tracker")
root.geometry("420x350")
root.configure(bg='#ECEFF1')

# Apply Material UI-inspired styles
style = ttk.Style(root)
style.theme_use("clam")
style.configure('TButton', font=('Roboto', 12, 'bold'), padding=10)
style.map('TButton', background=[('active', '#1E88E5'), ('!active', '#1976D2')],
          foreground=[('!disabled', 'white')])
style.configure('TLabel', background='#ECEFF1', foreground='#37474F', font=('Roboto', 12))

# Frame for layout management
main_frame = ttk.Frame(root, padding=20, style='TFrame')
main_frame.pack(fill='both', expand=True)

# Configure grid to be symmetrical
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

# Custom start time entry field with placeholder text
custom_start_time_entry = ttk.Entry(main_frame, font=('Roboto', 12), justify='center')
custom_start_time_entry.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky='ew')
placeholder_text = "Enter start time (HH:MM)"
custom_start_time_entry.insert(0, placeholder_text)
custom_start_time_entry.config(foreground='#B0BEC5')

# Clear placeholder text when user starts typing
def clear_placeholder(event):
    if custom_start_time_entry.get() == placeholder_text:
        custom_start_time_entry.delete(0, tk.END)
        custom_start_time_entry.config(foreground='#37474F')

custom_start_time_entry.bind("<FocusIn>", clear_placeholder)

# Buttons with Material styling
start_button = ttk.Button(main_frame, text="Start Work", command=start_work, style='TButton')
start_button.grid(row=1, column=0, padx=10, pady=15, sticky='ew')

end_button = ttk.Button(main_frame, text="End Work", command=end_work, style='TButton')
end_button.grid(row=1, column=1, padx=10, pady=15, sticky='ew')

# Result label
result_label = ttk.Label(main_frame, text="", style='TLabel', justify='center', font=('Roboto', 15))
result_label.grid(row=2, column=0, columnspan=2, pady=20, padx=10)

root.mainloop()
