import fitz  # PyMuPDF
import tkinter as tk
from PIL import Image, ImageTk

class PDFViewer(tk.Tk):
    def __init__(self, pdf_path):
        super().__init__()
        self.title("PDF Viewer")
        self.geometry("800x600")

        self.pdf_document = fitz.open(pdf_path)
        self.current_page = 0

        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.show_page()

        self.bind("<Left>", self.previous_page)
        self.bind("<Right>", self.next_page)

    def show_page(self):
        page = self.pdf_document[self.current_page]
        pixmap = page.get_pixmap()
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        photo = ImageTk.PhotoImage(image)

        self.canvas.config(width=pixmap.width, height=pixmap.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

        self.title(f"Page {self.current_page + 1}/{self.pdf_document.page_count}")

    def next_page(self, event):
        if self.current_page < self.pdf_document.page_count - 1:
            self.current_page += 1
            self.show_page()

    def previous_page(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def __del__(self):
        self.pdf_document.close()

if __name__ == "__main__":
    # Replace 'your_pdf_file.pdf' with the path to your PDF file
    pdf_viewer = PDFViewer('book.pdf')
    pdf_viewer.mainloop()
