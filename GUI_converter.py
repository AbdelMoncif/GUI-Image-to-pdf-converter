import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image,ImageTk
import PIL
import os
from tkinterdnd2 import tkdnd
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD
from ttkthemes import themed_style

class FileInputApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to Pdf converter")
        self.root.geometry("500x500")
        self.valid_formats = [".png",".jpg",".jpeg",".jpg", ".jpeg" ,".png" ,".bmp" ,".tiff" ,".gif" ]
        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack(pady=10)
        self.dropped = False

        s = ttk.Style()
        self.dnd_label = tk.Label(root, text="Drag and drop images here", bg="lightgray", width=50, height=10)
        self.dnd_label.pack(pady=10)

        self.browse_button = ttk.Button(root, text="Select your image", command=self.browse_file, width=25)
        self.browse_button.pack(pady=5)

        self.perform_button = ttk.Button(root, text="Convert image to pdf", command=self.perform_action, width=25)
        self.perform_button.pack(pady=20)

        self.images_list = []

        # Register the label as a drop target
        self.dnd_label.drop_target_register(DND_FILES)
        self.dnd_label.dnd_bind('<<Drop>>', self.on_drop)

        self.selected_file = None


    #function defining the on drop feature
    def on_drop(self, event):
        clean_list =list(self.root.tk.splitlist(event.data))
        for elem in clean_list:
            if Path(elem).suffix not in self.valid_formats:
                clean_list.remove(elem)
        files = clean_list
        self.images_list += files
        self.file_label.config(text=f"Selected file")
    #function defining the file browsing feature
    def browse_file(self):
        self.selected_files = list(filedialog.askopenfilenames(title="Select a file",
                                                        filetypes=(("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"), ("All files", "*.*"))))
        for elem in self.selected_files:
            if Path(elem).suffix not in self.valid_formats:
                self.selected_files.remove(elem)
        self.images_list += list(self.selected_files)
        if self.selected_files:
            self.file_label.config(text=f"Selected file: {self.selected_files}")

        else:
            self.file_label.config(text="No file selected")

    def perform_action(self):
        try:
            save_path = None
            i=0
            for file in self.images_list:
                if i == len(self.images_list):
                    break
                self.selected_file = file
                self.selected_file_name = os.path.basename(self.selected_file)
                if save_path is None:
                    image_1 = Image.open(self.selected_file)
                    im_1 = image_1.convert('RGB')
                    save_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    title="Save PDF as",
                    initialfile = f'{self.selected_file_name.split(".")[0]}.pdf')
                    self.selected_file_name = os.path.basename(self.selected_file)
                    im_1.save(save_path)
                    i+=1
                    save_path = save_path.replace(f'{(os.path.basename(file).split(".")[0])}.pdf',"")

                else:
                    try:
                        image_1 = Image.open(self.selected_file)
                        im_1 = image_1.convert('RGB')
                        save_path += f'{self.selected_file_name.split(".")[0]}.pdf'
                        self.file_label.config(text=f"File saved in: {save_path}")
                        im_1.save(save_path)
                        i+=1
                        self.file_label.config(text=f"File saved in: {save_path}")
                        save_path = save_path.replace(f'{self.selected_file_name.split(".")[0]}.pdf', "")
                    except TypeError:
                        pass

            self.images_list = []
        except PIL.UnidentifiedImageError:
            messagebox.showwarning("Warning", "Please select an image file")


if __name__ == "__main__":
    root = TkinterDnD.Tk()

    app = FileInputApp(root)
    root.mainloop()
