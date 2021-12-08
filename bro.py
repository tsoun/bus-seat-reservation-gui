import socket as sc
import tkinter as tk
from os.path import dirname, join
import win32clipboard as cb

global hostname, IP_address

current_dir = dirname(__file__)
image_path = join(current_dir, "net.png")

class main_win():
    def __init__(self, master):
        
        self.memory_list = []
        self.all_credentials = []
        self.ticket_index = 0
        self.current_page = 0
        
        self.master = master
        self.master.option_add("*Font", 'arial 10')
        self.master.title('Web Manager 0.1')
        self.master = master
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 300, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
         
        self.Message = tk.Label(master, text='Welcome to Web Manager 0.1 .')
        self.Message.place(relx= 0.32, rely = 0.085, anchor = 'center')
        self.Message.configure(background = 'white')
 
        self.show_ip = tk.Button(master, text = 'Show host IP address.', command = self.print_ip)
        self.show_ip.place(relx= 0.62, rely = 0.175)
        self.show_ip.configure(background = 'white')
                        
        self.ip_entry = tk.Entry(master)
        self.ip_entry.place(relx = 0.1, rely = 0.2)
        self.ip_entry.configure(background = 'white')
        
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.08, rely= 0.175, anchor="s")
        self.master.label.configure(background = 'white')

    def print_ip(self):
        if self.ip_entry.get() == '':
            self.ip_entry.insert(0, IP_address)
        else: 
            pass
        
        self.copy_ip()
    
    def copy_ip(self):
        cb.OpenClipboard()
        cb.EmptyClipboard()
        cb.SetClipboardData(cb.CF_TEXT, self.ip_entry.get())
        cb.CloseClipboard()
        

hostname = sc.gethostname()
IP_address = sc.gethostbyname(hostname)
print(hostname, IP_address)

root = tk.Tk()
window = main_win(root)
root.mainloop()
