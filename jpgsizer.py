import os
import tkinter as tk
from tkinter import ttk
from PIL import Image
import ttkbootstrap as ttkb

# This function resizes an image to 500x500 pixels
def resize_image(file_path, size=(500, 500)):
    with Image.open(file_path) as img:
        # Make the image smaller while keeping its shape
        img.thumbnail(size)
        # Create a new white image that's 500x500
        new_img = Image.new("RGB", size, (255, 255, 255))
        # Put the resized image in the center of the white image
        new_img.paste(img, ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2))
        # Save the new image, replacing the old one
        new_img.save(file_path)

# This function finds all the JPG files in a folder and its subfolders
def get_jpg_files(directory):
    jpg_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                jpg_files.append(os.path.join(root, file))
    return jpg_files

# This class creates the main window of our app
class ImageResizeApp(ttkb.Window):
    def __init__(self, theme="flatly"):
        super().__init__(themename=theme)
        self.title("Image Resize Tool")
        self.geometry("800x600")
        
        self.file_vars = {}
        self.create_widgets()

    # This function creates all the parts of our app window
    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a list to show all the JPG files
        columns = ("Select", "File Path")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.tree.heading("Select", text="Select")
        self.tree.column("Select", width=50, anchor="center")
        self.tree.heading("File Path", text="File Path")
        self.tree.column("File Path", width=700)

        # Add a scrollbar to the list
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a frame for our buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        # Add buttons to select all, deselect all, and resize
        ttk.Button(button_frame, text="Select All", command=self.select_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Deselect All", command=self.deselect_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Resize Selected", command=self.resize_selected).pack(side=tk.RIGHT, padx=5)

        # Load all the JPG files into our list
        self.load_files()

    # This function finds all JPG files and adds them to our list
    def load_files(self):
        jpg_files = get_jpg_files(os.getcwd())
        for file_path in jpg_files:
            var = tk.BooleanVar(value=False)
            self.file_vars[file_path] = var
            item = self.tree.insert("", "end", values=("[ ]", file_path))
            self.tree.tag_bind(item, '<ButtonRelease-1>', self.toggle_selection)

    # This function handles clicking on the checkbox
    def toggle_selection(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if column == '#1':  # The checkbox column
            current_value = self.tree.set(item, "Select")
            new_value = "[\u2713]" if current_value == "[ ]" else "[ ]"
            self.tree.set(item, "Select", new_value)
            file_path = self.tree.item(item)['values'][1]
            self.file_vars[file_path].set(new_value == "[\u2713]")

    # This function selects all files in the list
    def select_all(self):
        for item in self.tree.get_children():
            self.tree.set(item, "Select", "[\u2713]")
            file_path = self.tree.item(item)['values'][1]
            self.file_vars[file_path].set(True)

    # This function deselects all files in the list
    def deselect_all(self):
        for item in self.tree.get_children():
            self.tree.set(item, "Select", "[ ]")
            file_path = self.tree.item(item)['values'][1]
            self.file_vars[file_path].set(False)

    # This function resizes all selected images
    def resize_selected(self):
        for file_path, var in self.file_vars.items():
            if var.get():
                print(f"Resizing: {file_path}")
                resize_image(file_path)
        print("Resizing complete!")

# This is where our program starts running
if __name__ == "__main__":
    app = ImageResizeApp()
    app.mainloop()