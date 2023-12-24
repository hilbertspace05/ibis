import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
from PIL import Image, ImageTk
from database import create_connection, create_table, save_last_viewed_page, get_last_viewed_page

database = "book_database.db"
conn = create_connection(database)
create_table(conn)


class PDFViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Viewer")
        self.geometry("800x600")

        # Adding a menu to open PDF files
        self.menu = tk.Menu(self, bg='darkblue', fg='yellow')
        self.configure(bg='darkblue')
        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(side="left", anchor='s')
        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0, bg='darkblue', fg='yellow')
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_pdf)
        
        self.bind("<Left>", self.prev_page)
        self.bind("<Right>", self.next_page)
        self.bind("<KeyPress-equal>", self.zoom_in)
        self.bind("<KeyPress-minus>", self.zoom_out)
        
        # Zoom factor
        self.zoom_factor = 1.0

        # Zoom buttons
        zin_object = tk.Canvas(button_frame, width=50, height=50, bg='darkblue', highlightthickness=0)
        zin_object.pack(side="top")
        zoom_in_button = zin_object.create_oval(5, 5, 45, 45, fill='darkblue', outline='yellow', width=2)
        zoom_in_button2 = zin_object.create_line(25, 13, 25, 38, fill='yellow', width=3)  # Vertical line
        zoom_in_button3 = zin_object.create_line(13, 25, 38, 25, fill='yellow', width=3)  # Horizontal line
        zin_object.tag_bind(zoom_in_button, '<ButtonPress-1>', lambda x: self.zoom_in_but())
        zin_object.tag_bind(zoom_in_button2, '<ButtonPress-1>', lambda x: self.zoom_in_but())
        zin_object.tag_bind(zoom_in_button3, '<ButtonPress-1>', lambda x: self.zoom_in_but())
        zout_object = tk.Canvas(button_frame, width=50, height=50, bg='darkblue', highlightthickness=0)
        zout_object.pack(side="top")
        zoom_out_button = zout_object.create_oval(5, 5, 45, 45, fill='darkblue', outline='yellow', width=2)
        zoom_out_button2 = zout_object.create_line(13, 25, 38, 25, fill='yellow', width=3)  # Horizontal line
        zout_object.tag_bind(zoom_out_button, '<ButtonPress-1>', lambda x: self.zoom_out_but())
        zout_object.tag_bind(zoom_out_button2, '<ButtonPress-1>', lambda x: self.zoom_out_but())



        # Canvas for PDF display
        self.canvas = tk.Canvas(self, bg="navy")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        
        self.canvas_scrollbar_vertical = tk.Scrollbar(self, orient="vertical", bg='darkblue', troughcolor='darkblue', command=self.canvas.yview)
        self.canvas_scrollbar_vertical.pack(side="right", fill="y")
        
        self.canvas_scrollbar_horizontal = tk.Scrollbar(self, orient="horizontal", bg='darkblue', troughcolor='darkblue', command=self.canvas.xview)
        self.canvas_scrollbar_horizontal.pack(side="bottom", fill="x")

        self.canvas.configure(yscrollcommand=self.canvas_scrollbar_vertical.set)
        self.canvas.configure(xscrollcommand=self.canvas_scrollbar_horizontal.set)
        
        self.bind('<KeyPress>', self.on_key_press)
        self.canvas.focus_set()  # The canvas must have focus to receive key events
        
        self.setup_page_selector()
        

        # Variables for PDF handling
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0
        


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
            
    def setup_page_selector(self):
        self.button_frame_sel = tk.Frame(self, bg='darkblue')
        self.button_frame_sel.pack(side="top")
        self.page_selector_label = tk.Label(self.button_frame_sel, text="Go to page:", bg='darkblue', fg='yellow')
        self.page_selector_label.pack(side="left")

        self.page_selector_entry = tk.Entry(self.button_frame_sel, width=5)
        self.page_selector_entry.pack(side="left")

        self.go_button = tk.Button(self.button_frame_sel, text="Go", bg='darkblue', fg='yellow', command=self.go_to_page)
        self.go_button.pack(side="left")

    def go_to_page(self):
        page_number = int(self.page_selector_entry.get()) - 1  # assuming pages start at 0 internally
        if 0 <= page_number < self.total_pages:
            self.current_page = page_number
            self.display_page(self.current_page)
            self.focus_set()
        else:
            print("Page number out of range")
            self.focus_set()
   	

    def main(self):
        self.mainloop()
        
        
if __name__ == "__main__":
    app = PDFViewer()
    app.mainloop()
