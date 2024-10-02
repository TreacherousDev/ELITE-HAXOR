import tkinter as tk
from tkinter import ttk
import time
import threading

# Time-consuming task
def long_running_task(on_finish):
    for _ in range(10):  # Simulate a task that takes some time
        time.sleep(0.5)  # Simulate time-consuming operation
    on_finish()  # Call the function to close the loading screen when done

def create_loading_screen(root):
    # Create a top-level window for the loading screen
    loading_screen = tk.Toplevel(root)
    loading_screen.title("Loading...")
    loading_screen.geometry("300x100")
    loading_screen.resizable(False, False)

    # Create a label and progress bar in the loading screen
    label = tk.Label(loading_screen, text="Please wait, loading...", font=("Helvetica", 12))
    label.pack(pady=10)

    progress = ttk.Progressbar(loading_screen, mode="indeterminate")
    progress.pack(pady=10, padx=20, fill=tk.X)
    progress.start(10)  # Start the indeterminate progress bar animation

    return loading_screen

def start_task_with_loading_screen(root):
    # Show the loading screen
    loading_screen = create_loading_screen(root)

    # Function to close the loading screen
    def on_task_complete():
        loading_screen.destroy()

    # Run the long-running task in a separate thread
    threading.Thread(target=long_running_task, args=(on_task_complete,), daemon=True).start()

def main():
    root = tk.Tk()
    root.title("Main Application")
    root.geometry("400x300")
    
    # Button to start task with loading screen
    start_button = tk.Button(root, text="Start Task", font=("Helvetica", 12),
                             command=lambda: start_task_with_loading_screen(root))
    start_button.pack(pady=50)

    root.mainloop()

main()

