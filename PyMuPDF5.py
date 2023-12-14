import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
from PIL import Image, ImageTk

class PDFViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Viewer")
        self.geometry("800x600")

        # Adding a menu to open PDF files
        self.menu = tk.Menu(self)
        button_frame = tk.Frame(self)
        button_frame.pack(side="left")
        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_pdf)
        prev_button = tk.Button(button_frame, text="Previous", command=self.prev_page)
        prev_button.pack(side="top")

        next_button = tk.Button(self, text="Next", command=self.next_page)
        next_button.pack(side="right")
        
        # Zoom factor
        self.zoom_factor = 1.0

        # Zoom buttons
        zoom_in_button = tk.Button(button_frame, text="Zoom In", command=self.zoom_in)
        zoom_in_button.pack(side="top")

        zoom_out_button = tk.Button(button_frame, text="Zoom Out", command=self.zoom_out)
        zoom_out_button.pack(side="top")


        # Canvas for PDF display
        self.canvas = tk.Canvas(self, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        # Variables for PDF handling
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_document = fitz.open(file_path)
            self.total_pages = len(self.pdf_document)
            self.current_page = 0
            self.display_page(self.current_page)

    def display_page(self, page_number):
        page = self.pdf_document.load_page(page_number)
        mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas.delete("all")
        self.canvas.create_image(10, 10, image=self.photo, anchor="nw")

        # Updating the title with page info
        self.title(f"PDF Viewer - Page {self.current_page + 1} of {self.total_pages}")
        
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_page(self.current_page)
            
    def zoom_in(self):
        if self.pdf_document:
            self.zoom_factor *= 1.25  # Increase zoom
            self.display_page(self.current_page)

    def zoom_out(self):
        if self.pdf_document:
            self.zoom_factor *= 0.8  # Decrease zoom
            self.display_page(self.current_page)

    def main(self):
        self.mainloop()
        
        
if __name__ == "__main__":
    app = PDFViewer()
    app.mainloop()
