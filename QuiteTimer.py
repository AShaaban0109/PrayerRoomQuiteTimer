import tkinter as tk
import datetime
import pandas as pd



df = pd.read_csv('prayer_times.csv')
df = df.drop("Days", axis=1)
# Remove rows with missing values that are present at the bottom
df = df.dropna()

# Create a GUI window
window = tk.Tk()
window.title("Prayer Times")

# Function to update the message
def update_message():
    current_time = datetime.datetime.now().strftime("%H:%M")
    today = datetime.datetime.now().day

    for col in df.columns:
        for row in range(len(df)):
            prayer_time = df.loc[row, col]
            if row +1 == today:
                prayer_datetime = datetime.datetime.strptime(prayer_time, "%H:%M")
                current_datetime = datetime.datetime.strptime(current_time, "%H:%M")
                if prayer_datetime - current_datetime <= datetime.timedelta(minutes=15) and prayer_datetime - current_datetime >= datetime.timedelta(minutes=-15):
                    window.deiconify()  # Restore the window
                    message_var.set(f"Time to keep quiet for {col} prayer!")
                    return
                    
    # If no prayer time, minimize the window
    message_var.set("No prayer time now. You can relax!")
    window.iconify()
    window.after(10000, update_message)  # Check every 10 seconds


# Create a label to display the message
message_var = tk.StringVar()
message_label = tk.Label(window, textvariable=message_var, font=("Helvetica", 16))
message_label.pack(padx=20, pady=20)

# Update the message initially
update_message()

# Run the GUI loop
window.mainloop()
