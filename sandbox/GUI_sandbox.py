root = tk.Tk()
root.title("Link Processor")

# Create a text box for entering links
entry = tk.Text(root, height=5, width=50)
entry.pack(pady=10)

# Create a button to trigger link processing
process_button = tk.Button(root, text="Process Links", command=process_links)
process_button.pack()

# Start the Tkinter event loop
root.mainloop()