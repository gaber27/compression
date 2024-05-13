import tkinter as tk
from tkinter import ttk
from compression_algorithms import compress_and_show, test_all_and_show_best

# Function to compress the entered text using the selected algorithm
def compress_text():
    # Retrieve the entered text from the text entry widget
    text = entry.get("1.0", "end-1c")
    # Retrieve the selected encoding method
    encoding_method = encoding_var.get()
    
    # Check if Golomb encoding is selected
    if encoding_method == "Golomb":
        # Retrieve the entered values of n and m
        n = int(n_entry.get())
        m = int(m_entry.get())
        # Call the compress_and_show function with the entered text, encoding method, n, and m
        results = compress_and_show(text, encoding_method, n=n, m=m)
    else:
        # Call the compress_and_show function with the entered text and encoding method
        results = compress_and_show(text, encoding_method)
        
    # Display the compression results in the result_text widget
    result_text.config(state="normal")
    result_text.delete("1.0", "end")
    result_text.insert("end", results)
    result_text.config(state="disabled")

# Function to test all algorithms and show the best result
def test_all_algorithms():
    # Retrieve the entered text from the text entry widget
    text = entry.get("1.0", "end-1c")
    # Call the test_all_and_show_best function with the entered text
    results = test_all_and_show_best(text)
    # Display the compression results in the result_text widget
    result_text.config(state="normal")
    result_text.delete("1.0", "end")
    result_text.insert("end", results)
    result_text.config(state="disabled")

# Create the main window
root = tk.Tk()
root.title("Data Compression Techniques")

# Use the 'clam' theme for the ttk elements
style = ttk.Style(root)
style.theme_use("clam")

# Create a frame to hold the GUI elements
frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Label for entering text
label_text = ttk.Label(frame, text="Enter Text:", font=("Helvetica", 12))
label_text.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

# Text entry widget for entering text
entry = tk.Text(frame, height=10, width=50)
entry.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

# Label and entry widget for Golomb Integer (n)
label_n = ttk.Label(frame, text="Enter Golomb Integer (n):", font=("Helvetica", 12))
label_n.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
n_entry = ttk.Entry(frame)
n_entry.grid(row=2, column=1, padx=10, pady=5)

# Label and entry widget for Golomb Parameter (M)
label_m = ttk.Label(frame, text="Enter Golomb Parameter (M):", font=("Helvetica", 12))
label_m.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
m_entry = ttk.Entry(frame)
m_entry.grid(row=3, column=1, padx=10, pady=5)

# Radio buttons for selecting encoding methods
encoding_var = tk.StringVar(value='RLE') 
tk.Radiobutton(frame, text="Run-Length Encoding", variable=encoding_var, value="RLE").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
tk.Radiobutton(frame, text="Huffman Encoding", variable=encoding_var, value="Huffman").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
tk.Radiobutton(frame, text="Arithmetic Encoding", variable=encoding_var, value="Arithmetic").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
tk.Radiobutton(frame, text="Golomb Encoding", variable=encoding_var, value="Golomb").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
tk.Radiobutton(frame, text="LZW Encoding", variable=encoding_var, value="LZW").grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)

# Button to compress text
compress_btn = ttk.Button(frame, text="Compress Text", command=compress_text)
compress_btn.grid(row=9, column=0, padx=10, pady=5)

# Button to test all algorithms
test_btn = ttk.Button(frame, text="Test All & Show Best", command=test_all_algorithms)
test_btn.grid(row=9, column=1, padx=10, pady=5)

# Label for displaying results
label_result = ttk.Label(frame, text="Results:", font=("Helvetica", 12))
label_result.grid(row=10, column=0, padx=10, pady=5, sticky=tk.W)

# Text widget for displaying results
result_text = tk.Text(frame, height=15, width=50, wrap='word', state='disabled')
result_text.grid(row=11, column=0, columnspan=3, padx=10, pady=5)

# Scrollbar for the text widget
scroll = tk.Scrollbar(frame, command=result_text.yview, orient='vertical')
result_text.configure(yscrollcommand=scroll.set)
scroll.grid(row=11, column=2, sticky='ns')

# Start the main event loop
root.mainloop()
