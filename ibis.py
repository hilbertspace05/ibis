import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
from PIL import Image, ImageTk
from database import create_connection, create_table, save_last_viewed_page, get_last_viewed_page
from arrows import *

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
        button_frame2 = tk.Frame(self, bg='darkblue')
        button_frame2.pack(side="right", anchor='se')
        #button_frame3 = tk.Frame(self, bg='darkblue')
        #button_frame3.pack(side="right", pady=50, anchor='se')
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
        
        self.button_frame_sel = tk.Frame(button_frame2, bg='darkblue')
        self.button_frame_sel.pack(side="top", pady=20, anchor="n")
        self.page_selector_label = tk.Label(self.button_frame_sel, text="Go to page:", bg='darkblue', fg='yellow')
        self.page_selector_label.pack(side="left", anchor="ne")
		
        self.page_selector_entry = tk.Entry(self.button_frame_sel, width=5)
        self.page_selector_entry.pack(side="left", anchor="ne")
		
        self.go_button = tk.Button(self.button_frame_sel, text="Go", bg='darkblue', fg='yellow', command=self.go_to_page)
        self.go_button.pack(side="left", anchor="ne")

        # zoom buttons
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
        
        
        # moving pdf buttons
        up_object = tk.Canvas(button_frame2, width=50, height=50, bg='darkblue', highlightthickness=0)
        up_object.pack(side="top")
        uparrowp, upts, upte = up_arrow()
        up_button = up_object.create_oval(5, 5, 45, 45, fill='darkblue', outline='yellow', width=2)
        up_button2 = up_object.create_polygon(uparrowp, fill='yellow')
        up_button3 =up_object.create_line(upts, upte, fill='yellow', width=2)
        up_object.tag_bind(up_button, '<ButtonPress-1>', lambda x: self.scroll_up())
        up_object.tag_bind(up_button2, '<ButtonPress-1>', lambda x: self.scroll_up())
        up_object.tag_bind(up_button3, '<ButtonPress-1>', lambda x: self.scroll_up())
        left_object = tk.Canvas(button_frame2, width=50, height=50, bg='darkblue', highlightthickness=0)
        left_object.pack(side="left")
        leftarrowp, leftts, leftte = left_arrow()
        left_button = left_object.create_oval(5, 5, 45, 45, fill='darkblue', outline='yellow', width=2)
        left_button2 = left_object.create_polygon(leftarrowp, fill='yellow')
        left_button3 = left_object.create_line(leftts, leftte, fill='yellow', width=2)
        left_object.tag_bind(left_button, '<ButtonPress-1>', lambda x: self.scroll_left())
        left_object.tag_bind(left_button2, '<ButtonPress-1>', lambda x: self.scroll_left())
        left_object.tag_bind(left_button3, '<ButtonPress-1>', lambda x: self.scroll_left())
        down_object = tk.Canvas(button_frame2, width=50, height=50, bg='darkblue', highlightthickness=0)
        down_object.pack(side="left")
        downarrowp, downts, downte = down_arrow()
        down_button = down_object.create_oval(5, 5, 45, 45, fill='darkblue', outline='yellow', width=2)
        down_button2 = down_object.create_polygon(downarrowp, fill='yellow')
        down_button3 = down_object.create_line(downts, downte, fill='yellow', width=2)
        down_object.tag_bind(down_button, '<ButtonPress-1>', lambda x: self.scroll_down())
        down_object.tag_bind(down_button2, '<ButtonPress-1>', lambda x: self.scroll_down())
        down_object.tag_bind(down_button3, '<ButtonPress-1>', lambda x: self.scroll_down())
        right_object = tk.Canvas(button_frame2, width=50, height=50, bg='darkblue', highlightthickness=0)
        right_object.pack(side="right")
        rightarrowp, rightts, rightte = right_arrow()
        right_button = right_object.create_oval(5, 5, 45, 45, fill='darkblue', outline='yellow', width=2)
        right_button2 = right_object.create_polygon(rightarrowp, fill='yellow')
        right_button3 = right_object.create_line(rightts, rightte, fill='yellow', width=2)
        right_object.tag_bind(right_button, '<ButtonPress-1>', lambda x: self.scroll_right())
        right_object.tag_bind(right_button2, '<ButtonPress-1>', lambda x: self.scroll_right())
        right_object.tag_bind(right_button3, '<ButtonPress-1>', lambda x: self.scroll_right())



        # Canvas for PDF display
        self.canvas = tk.Canvas(self, bg="navy")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        
        self.bind('<KeyPress>', self.on_key_press)
        self.canvas.focus_set()  # The canvas must have focus to receive key events
        
        #self.setup_page_selector()
        

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
            
    def scroll_up(self):
        self.canvas.yview_scroll(-1, 'units')
		
    def scroll_down(self):
        self.canvas.yview_scroll(1, 'units')
		
    def scroll_left(self):
        self.canvas.xview_scroll(-1, 'units')
		
    def scroll_right(self):
        self.canvas.xview_scroll(1, 'units')
            
    #def setup_page_selector(self):
    #    self.button_frame_sel = tk.Frame(button_frame2, bg='darkblue')
    #    self.button_frame_sel.pack(side="top", anchor="n")
    #    self.page_selector_label = tk.Label(button_frame_sel, text="Go to page:", bg='darkblue', fg='yellow')
    #    self.page_selector_label.pack(side="left", anchor="ne")
	#	
    #    self.page_selector_entry = tk.Entry(button_frame_sel, width=5)
    #    self.page_selector_entry.pack(side="left", anchor="ne")
	#	
    #    self.go_button = tk.Button(button_frame_sel, text="Go", bg='darkblue', fg='yellow', command=self.go_to_page)
    #    self.go_button.pack(side="left", anchor="ne")

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
