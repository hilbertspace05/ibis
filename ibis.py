import tkinter as tk
from database import create_connection, create_table, save_last_viewed_page, get_last_viewed_page
from arrows import *
from pdf_operations import PDFOperations
from buttons import create_buttons

database = "book_database.db"
conn = create_connection(database)
create_table(conn)


class PDFViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Viewer")
        self.geometry("800x600")

        
        # Zoom factor
        self.zoom_factor = 1.0
        
        # Adding a menu to open PDF files
        self.menu = tk.Menu(self, bg='darkblue', fg='yellow')
        self.configure(bg='darkblue')
        button_frame = tk.Frame(self, bg='darkblue')
        button_frame.pack(side="left", anchor='sw')
        button_frame2 = tk.Frame(self, bg='darkblue')
        button_frame2.pack(side="right", anchor='se')

        # Canvas for PDF display
        self.canvas = tk.Canvas(self, bg="navy")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.button_frame_sel = tk.Frame(button_frame2, bg='darkblue')
        self.button_frame_sel.pack(side="top", pady=20, anchor="n")
        self.page_selector_label = tk.Label(self.button_frame_sel, text="Go to page:", bg='darkblue', fg='yellow')
        self.page_selector_label.pack(side="left", anchor="ne")
		
        self.page_selector_entry = tk.Entry(self.button_frame_sel, width=5)
        self.page_selector_entry.pack(side="left", anchor="ne")

        self.pdf_operations = PDFOperations(self, self.canvas, self.zoom_factor, self.title, self.page_selector_entry)

        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0, bg='darkblue', fg='yellow')
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.pdf_operations.open_pdf)
        
        self.bind("<Left>", self.pdf_operations.prev_page)
        self.bind("<Right>", self.pdf_operations.next_page)
        self.bind("<KeyPress-equal>", self.pdf_operations.zoom_in)
        self.bind("<KeyPress-minus>", self.pdf_operations.zoom_out)
        
        
		
        self.go_button = tk.Button(self.button_frame_sel, text="Go", bg='darkblue', fg='yellow', command=self.pdf_operations.go_to_page)
        self.go_button.pack(side="left", anchor="ne")

        
        create_buttons(self.pdf_operations, button_frame, button_frame2, up_arrow, left_arrow, down_arrow, right_arrow)
        
        
        self.bind('<KeyPress>', self.pdf_operations.on_key_press)
        self.canvas.focus_set()  # The canvas must have focus to receive key events
        

        # Variables for PDF handling
        self.pdf_document = None
        self.current_page = 0
        self.total_pages = 0

        

   	

    def main(self):
        self.mainloop()
        
        
if __name__ == "__main__":
    app = PDFViewer()
    app.mainloop()
