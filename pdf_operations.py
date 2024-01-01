import fitz
from tkinter import filedialog
from PIL import Image, ImageTk
from database import create_connection, create_table, save_last_viewed_page, get_last_viewed_page

database = "book_database.db"
conn = create_connection(database)
create_table(conn)

class PDFOperations:
    def __init__(self, master, canvas, zoom_factor, title, page_selector_entry):
        self.master = master
        self.canvas = canvas
        self.zoom_factor = zoom_factor
        self.title = title
        self.page_selector_entry = page_selector_entry

    def open_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.file_path:
            self.pdf_document = fitz.open(self.file_path)
            self.total_pages = len(self.pdf_document)
            self.current_page = int(get_last_viewed_page(conn, self.file_path))
            self.display_page(self.current_page)

    def display_page(self, page_number):
        page = self.pdf_document.load_page(page_number)
        mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas.delete("all")
        self.canvas.create_image(10, 10, image=self.photo, anchor="nw")
        self.canvas.yview_moveto(0)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Updating the title with page info
        self.title(f"PDF Viewer - Page {self.current_page + 1} of {self.total_pages}")
        
    def prev_page(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)
            save_last_viewed_page(conn, self.file_path, self.current_page)

    def next_page(self, event):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_page(self.current_page)
            save_last_viewed_page(conn, self.file_path, self.current_page)
            
    def zoom_in(self, event):
        if self.pdf_document:
            self.zoom_factor *= 1.25  # Increase zoom
            self.display_page(self.current_page)
    
    def zoom_out(self, event):
        if self.pdf_document:
            self.zoom_factor *= 0.8  # Decrease zoom
            self.display_page(self.current_page)
            
    def zoom_in_but(self):
        if self.pdf_document:
            self.zoom_factor *= 1.25  # Increase zoom
            self.display_page(self.current_page)
    
    def zoom_out_but(self):
        if self.pdf_document:
            self.zoom_factor *= 0.8  # Decrease zoom
            self.display_page(self.current_page)
            
    def on_key_press(self, event):
        if event.keysym == 'Up':
            self.canvas.yview_scroll(-1, 'units')
        elif event.keysym == 'Down':
            self.canvas.yview_scroll(1, 'units')
        elif event.keysym == 'comma':
            self.canvas.xview_scroll(-1, 'units')
        elif event.keysym == 'period':
            self.canvas.xview_scroll(1, 'units')
            
    def scroll_up(self):
        self.canvas.yview_scroll(-1, 'units')
		
    def scroll_down(self):
        self.canvas.yview_scroll(1, 'units')
		
    def scroll_left(self):
        self.canvas.xview_scroll(-1, 'units')
		
    def scroll_right(self):
        self.canvas.xview_scroll(1, 'units')
            

    def go_to_page(self):
        page_number = int(self.page_selector_entry.get()) - 1  # assuming pages start at 0 internally
        if 0 <= page_number < self.total_pages:
            self.current_page = page_number
            self.display_page(self.current_page)
            self.master.focus_set()
        else:
            print("Page number out of range")
            self.master.focus_set()