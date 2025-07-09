# import tkinter as tk
# from tkinter import ttk

# from spicy import misc


# root = tk.Tk()

# canvas = tk.Canvas(root)
# canvas.pack(side="left", fill="both", expand=True)

# scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
# scrollbar.pack(side="right", fill="y")

# canvas.configure(yscrollcommand=scrollbar.set)

# scrollable_frame = ttk.Frame(canvas)
# scrollable_frame.bind(
#    "<Configure>",
#    lambda e: canvas.configure(
#        scrollregion=canvas.bbox("all")
#    )
# )

# canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# for i in range(50):
#    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()

# root.mainloop()
import math
print(math.pi)