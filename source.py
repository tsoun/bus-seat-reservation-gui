import bbmod
import tkcalendar
import datetime
import time
import tkinter as tk
import xlwings
import qrcode
import os
import threading
import pythoncom
from random import random, randint
from PIL import Image, ImageTk
from tkinter import messagebox
from os.path import dirname, join
current_dir = dirname(__file__)
image_path = join(current_dir, "ktel_picture.png")

bus = bbmod.bus()
memory_list = []
did_action_run = False

class window_1():
    def __init__(self, master): #welcome window
        #first things first
        self.memory_list = []
        self.all_credentials = []
        self.ticket_index = 0
        self.current_page = 0
        
        #το παράθυρο
        self.master = master
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master = master
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
         
        #ένα Message
        self.Message = tk.Label(master, text='Καλώς ήρθατε στο σύστημα\
        \nκρατήσεων θέσεων λεωφορείου της «ΚΤΕΛ Αχαΐας ΑΕ».')
        self.Message.place(relx= 0.5, rely = 0.6, anchor = 'center')
        self.Message.configure(background = 'white')
 
        #η εικόνα
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.5, rely= 0.5, anchor="s")
        self.master.label.configure(background = 'white')
 
        #κουμπί εισόδου
        self.login_button = tk.Button(master, text = 'Είσοδος στο σύστημα', command = self.next_page)
        self.login_button.place(relx= 0.5, rely = 0.8, anchor = 'center')
        self.login_button.configure(background = 'white')
                                     
        #κουμπί βοήθειας
        self.help_button = tk.Button(master, text = 'Βοήθεια', command = open_help_win)
        self.help_button.place(relx= 0.9, rely = 0.05, anchor = 'center')
        self.help_button.configure(background = 'white')
        
    def page_1(self): #select start and destination
        #first things first
        self.current_page = 1
        
        #το παράθυρο
        self.masterback.pack_forget()
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master.configure(background = 'white')
        #self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
         
        #η εικόνα
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.25, rely= 0.365, anchor="s")
        self.master.label.configure(background = 'white')
        
        #ένα Message
        self.Message = tk.Label(self.master, text='Από:')
        self.Message.place(relx= 0.1, rely = 0.4, anchor = 'center')
        self.Message.configure(background = 'white')
        
        #ένα Message
        self.Message = tk.Label(self.master, text='Προς:')
        self.Message.place(relx= 0.1, rely = 0.5, anchor = 'center')
        self.Message.configure(background = 'white')
        
        #dropdown μενού 1
        self.variable = tk.StringVar(self.master)
        self.variable.set("Πάτρα")                       # default τιμή
        w = tk.OptionMenu(self.master, self.variable, *bus.destinations)
        w.place(relx = 0.2, rely = 0.4, anchor = 'w', width = 200)
        
        #dropdown μενού 2
        self.variable2 = tk.StringVar(self.master)
        w2 = tk.OptionMenu(self.master, self.variable2, *bus.destinations)
        w2.place(relx = 0.2, rely = 0.5, anchor = 'w', width = 200)
                                
        #κουμπί βοήθειας
        self.help_button = tk.Button(self.master, text = 'Βοήθεια', command = open_help_win)
        self.help_button.place(relx = 0.9, rely = 0.05, anchor = 'center')
        self.help_button.configure(background = 'white')
 
        #κουμπί επόμενο
        self.next_button = tk.Button(self.master, text = 'Επόμενο', command = self.end_of_page_1)
        self.next_button.place(relx = 0.85, rely = 0.9, anchor = 'center')
        self.next_button.configure(background = 'white')

    def end_of_page_1(self, *args):
        self.start = self.variable.get()
        self.end = self.variable2.get()
        self.warning_for_patras = tk.Label(self.master, text='Από τη συγκεκριμένη εφαρμογή, μπορείτε να κλείσετε εισιτήρια μόνο για διαδρομές που περιλαμβάνουν την πόλη της Πάτρας. Για τη διαδρομή που επιλέξατε, θα πρέπει να απευθυνθείτε σε άλλη εταιρεία ΚΤΕΛ. \nΕπιλέξτε την Πάτρα ως αφετηρία ή προορισμό για να συνεχίσετε.', wraplength = 400, justify='left', fg='white', bg='white')
        self.warning_for_patras.place(relx = 0.065, rely = 0.6)
        if self.start != 'Πάτρα' and self.end != 'Πάτρα':
            self.warning_for_patras.configure(fg='red')
        else:
            self.warning_for_dests = tk.Label(self.master, text='Παρακαλώ επιλέξτε αφετηρία και προορισμό.', fg='white', bg='white')
            self.warning_for_dests.place(relx = 0.065, rely = 0.6)
            if self.start == '' or self.end == '':
                self.warning_for_dests.configure(fg='red')
            else:   
                self.warning_for_diff_dests = tk.Label(self.master, text='Λανθασμένες επιλογές πόλεων.', fg='white', bg='white')
                self.warning_for_diff_dests.place(relx = 0.065, rely = 0.6)
                if self.start == self.end:
                    self.warning_for_diff_dests.configure(fg='red')
                else:
                    self.next_page()            
            
    def page_2(self): #select time and date
        #first things first
        self.current_page = 2

        #το παράθυρο
        self.masterback.pack_forget()
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
                       
        #η εικόνα
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.25, rely= 0.365, anchor="s")
        self.master.label.configure(background = 'white')
                          
        #κουμπί βοήθειας
        self.help_button = tk.Button(self.master, text = 'Βοήθεια', command = open_help_win)
        self.help_button.place(relx = 0.9, rely = 0.05, anchor = 'center')
        self.help_button.configure(background = 'white')

        #Static text 1
        self.Message = tk.Label(self.master, text='Εισιτήρια από:')
        self.Message.place(relx= 0.3, rely = 0.4, anchor = 'center')
        self.Message.configure(background = 'white')
        
        #Dynamic text 1 (start)
        self.variable = tk.StringVar(self.master)
        self.variable.set(self.start)
        self.w1 = tk.Label(self.master, textvariable=self.variable, font = 'bold')
        self.w1.place(relx = 0.3, rely = 0.45, anchor = 'center')
        self.w1.configure(background = 'white')

        #Static text 2
        self.Message = tk.Label(self.master, text='προς:')
        self.Message.place(relx= 0.7, rely = 0.4, anchor = 'center')
        self.Message.configure(background = 'white')
        
        #Dynamic text 2 (end)
        self.variable = tk.StringVar(self.master)
        self.variable.set(self.end)
        self.w1 = tk.Label(self.master, textvariable=self.variable, font = 'bold')
        self.w1.place(relx = 0.7, rely = 0.45, anchor = 'center')
        self.w1.configure(background = 'white')

        #Drop-down calendar
        self.Message = tk.Label(self.master, text='Ημερομηνία:')
        self.Message.place(relx = 0.14, rely = 0.6, anchor = 'center')
        self.Message.configure(background = 'white')
        self.cal = tkcalendar.DateEntry(self.master, width=12, background='darkblue', foreground='white', borderwidth=2, locale='el_GR', date_pattern='dd/mm/yyyy')
        self.cal.place(relx = 0.5, rely = 0.6, anchor = 'center')

        #Drop-down clock
        self.Message = tk.Label(self.master, text='Ώρα:')
        self.Message.place(relx = 0.1, rely = 0.7, anchor = 'center')
        self.Message.configure(background = 'white')
        self.timeselected = tk.StringVar(self.master)
        self.timeselected.set(" ")
        timemenu = tk.OptionMenu(self.master, self.timeselected, *self.times_list())
        timemenu.place(relx = 0.385, rely = 0.7, anchor = 'w', width = 115)

        #ένα Message
        self.Message = tk.Label(self.master, text='Επιλέξτε ημερομηνία και ώρα αναχώρησης:')
        self.Message.place(relx = 0.3, rely = 0.3, anchor = 'center')
        self.Message.configure(background = 'white')
 
        #κουμπί επόμενο
        self.next_button = tk.Button(self.master, text = 'Επόμενο', command = self.end_of_page_2_part_1)
        self.next_button.place(relx = 0.85, rely = 0.9, anchor = 'center')
        self.next_button.configure(background = 'white')
 
        #κουμπί προηγούμενο
        self.prev_button = tk.Button(self.master, text = 'Προηγούμενο', command = self.prev_page)
        self.prev_button.place(relx = 0.15, rely = 0.9, anchor = 'center')
        self.prev_button.configure(background = 'white')

    def end_of_page_2_part_1(self): # check of entries
        self.given_time = self.timeselected.get()
        self.given_date = self.cal.get_date()
        self.warning_for_time = tk.Label(self.master, text='Παρακαλώ επιλέξτε ώρα αναχώρησης.', fg='white', bg='white')
        self.warning_for_time.place(relx = .28, rely = 0.8)
        today = datetime.date.today()
        if self.given_time == ' ':
            self.warning_for_time.configure(fg='red')
        else:
            self.warning_for_date = tk.Label(self.master, text='Παρακαλώ επιλέξτε μελλοντική ημερομηνία.', fg='white', bg='white')
            self.warning_for_date.place(relx = .28, rely = 0.8)
            self.print_time = int(str(self.given_time.split(':')[0])+str(self.given_time.split(':')[1]))
            now_time = int(str(datetime.datetime.now())[11:13]+str(datetime.datetime.now())[14:16])
            if self.given_date < today:
                self.warning_for_date.configure(fg='red')
            elif self.given_date == today:    
                if self.print_time < now_time:
                    self.warning_for_date.configure(fg='red')
                else:
                    self.end_of_page_2_part_2()
            else:
                self.end_of_page_2_part_2()

    def end_of_page_2_part_2(self): # availability setting
        global memory_list
        no_previous_entries = True
        if len(memory_list) != 0:
            for i in range(len(memory_list)):
                if memory_list[i][0] == self.start and memory_list[i][1] == self.end and memory_list[i][2] == self.given_date and memory_list[i][3] == self.given_time:
                    self.availability = memory_list[i][4]
                    no_previous_entries = False
                    break
        today = datetime.date.today()
        print_date_today = str(today)[8:]+'/'+str(today)[5:7]+'/'+str(today)[:4]
        if no_previous_entries:
            self.availability = bus.showAvailability()
        # Για δρομολόγια μετά από 6 μήνες από σήμερα, όλες οι θέσεις θα είναι ανοιχτές.
        if self.given_date > datetime.date(int(print_date_today[6:]), int(print_date_today[3:5])+6, int(print_date_today[:2])):
            self.availability = [True for x in range(49)]
        sublist = [self.start, self.end, self.given_date, self.given_time, self.availability]
        if (sublist not in memory_list):
            memory_list.append(sublist)
        self.warning_for_availability = tk.Label(self.master, text = 'Για το συγκεκριμένο δρομολόγιο, όλες οι θέσεις είναι κατειλημμένες. Παρακαλώ επιλέξτε διαφορετική ημερομηνία ή/και ώρα.', wraplength=400, justify='center', fg='white', bg='white')
        self.warning_for_availability.place(relx = 0.15, rely = 0.75)
        if (True not in self.availability):
            self.warning_for_availability.configure(fg='red')
        else:
            self.next_page()
         
    def page_3(self): # master credentials
        #first things first
        self.current_page = 3

        #το παράθυρο
        self.masterback.pack_forget()
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
                                        
        #η εικόνα
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.25, rely= 0.365, anchor="s")
        self.master.label.configure(background = 'white')
        
        #Μεγάλα γράμματα
        self.Header = tk.Label(self.master, text='Στοιχεία Κράτησης', font = 'Helvetica 20 bold')
        self.Header.place(relx= 0.5, rely = 0.3, anchor = 'center')
        self.Header.configure(background = 'white')
                
        #όνομα
        self.L3_1 = tk.Label(self.master, text='Όνομα: ')
        self.L3_1.place(relx= 0.5, rely = 0.4, anchor = 'center')
        self.L3_1.configure(background = 'white')

        #entry ονόματος
        self.entry_master_name = tk.Entry(self.master)
        self.entry_master_name.place(relx = 0.5, rely = 0.45, anchor = 'center')
                
        #επώνυμο
        self.L3_2 = tk.Label(self.master, text='Επώνυμο: ')
        self.L3_2.place(relx= 0.5, rely = 0.5, anchor = 'center')
        self.L3_2.configure(background = 'white')
        
        #entry επωνύμου
        self.entry_master_surname = tk.Entry(self.master)
        self.entry_master_surname.place(relx = 0.5, rely = 0.55, anchor = 'center')
        
        #κουμπί βοήθειας
        self.help_button = tk.Button(self.master, text = 'Βοήθεια', command = open_help_win)
        self.help_button.place(relx = 0.9, rely = 0.05, anchor = 'center')
        self.help_button.configure(background = 'white')

        #Drop-down πλήθος εισιτηρίων
        self.Message = tk.Label(self.master, text='Θέσεις:')
        self.Message.place(relx = 0.3, rely = 0.65, anchor = 'center')
        self.Message.configure(background = 'white')
        self.persselected = tk.StringVar(self.master)
        self.persselected.set(1)
        persmenu = tk.OptionMenu(self.master, self.persselected, *[1,2,3,4])
        persmenu.place(relx = 0.385, rely = 0.65, anchor = 'w', width = 75)
        
        #κουμπί προηγούμενο
        self.prev_button = tk.Button(self.master, text = 'Προηγούμενο', command = self.prev_page)
        self.prev_button.place(relx = 0.15, rely = 0.9, anchor = 'center')
        self.prev_button.configure(background = 'white')

        #κουμπί επόμενο
        self.next_button = tk.Button(self.master, text = 'Επόμενο', command = self.end_of_page_3)
        self.next_button.place(relx = 0.85, rely = 0.9, anchor = 'center')
        self.next_button.configure(background = 'white')

    def end_of_page_3(self):
        self.tickets_wanted = int(self.persselected.get())
        self.given_master_name = self.entry_master_name.get().strip(' ').capitalize()
        self.given_master_surname = self.entry_master_surname.get().strip(' ').capitalize()
        self.warning_for_master_name = tk.Label(self.master, text='Παρακαλώ εισάγετε σωστά τα στοιχεία σας.', fg='white', bg='white')
        self.warning_for_master_name.place(relx = .28, rely = 0.7)
        if self.given_master_name == '' or self.given_master_surname == '':
            self.warning_for_master_name.configure(fg='red')
        else:
            self.ticket_index += 1
            self.next_page()

    def page_ticket(self):
        #first things first
        self.current_page = 4

        #το παράθυρο
        self.masterback.pack_forget()
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
                                        
        #η εικόνα
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.25, rely= 0.365, anchor="s")
        self.master.label.configure(background = 'white')

        #Μεγάλα γράμματα
        self.Header = tk.Label(self.master, text='Στοιχεία Εισιτηρίου #'+str(self.ticket_index), font = 'Helvetica 20 bold')
        self.Header.place(relx= 0.5, rely = 0.3, anchor = 'center')
        self.Header.configure(background = 'white')

        #όνομα
        self.L1 = tk.Label(self.master, text='Όνομα: ')
        self.L1.place(relx= 0.5, rely = 0.4, anchor = 'center')
        self.L1.configure(background = 'white')

        #entry ονόματος
        self.entry_name = tk.Entry(self.master)
        if self.ticket_index == 1:
            self.entry_name.insert(0, self.given_master_name)
        self.entry_name.place(relx = 0.5, rely = 0.45, anchor = 'center')
                
        #επώνυμο
        self.L2 = tk.Label(self.master, text='Επώνυμο: ')
        self.L2.place(relx= 0.5, rely = 0.5, anchor = 'center')
        self.L2.configure(background = 'white')
        
        #entry επωνύμου
        self.entry_surname = tk.Entry(self.master)
        if self.ticket_index == 1:
            self.entry_surname.insert(0, self.given_master_surname)
        self.entry_surname.place(relx = 0.5, rely = 0.55, anchor = 'center')

        #Drop-down types
        self.Message = tk.Label(self.master, text='Είδος κομίστρου:')
        self.Message.place(relx = 0.3, rely = 0.65, anchor = 'center')
        self.Message.configure(background = 'white')
        self.typeselected = tk.StringVar(self.master)
        self.typeselected.set("Ολόκληρο")
        typemenu = tk.OptionMenu(self.master, self.typeselected, *self.types_list())
        typemenu.place(relx = 0.45, rely = 0.65, anchor = 'w', width = 200)

        #έγγραφο
        self.L3 = tk.Label(self.master, text='Αριθμός αστυνομικής ταυτότητας / Αριθμός εκπτωτικής κάρτας \n (μόνο αν δικαιούστε μειωμένο κόμιστρο):')
        self.L3.place(relx= 0.5, rely = 0.75, anchor = 'center')
        self.L3.configure(background = 'white')

        #entry εγγράφου
        self.entry_code = tk.Entry(self.master)
        self.entry_code.place(relx = 0.5, rely = 0.8, anchor = 'center')

        #κουμπί βοήθειας
        self.help_button = tk.Button(self.master, text = 'Βοήθεια', command = open_help_win)
        self.help_button.place(relx = 0.9, rely = 0.05, anchor = 'center')
        self.help_button.configure(background = 'white')
 
        #κουμπί επόμενο
        self.next_button = tk.Button(self.master, text = 'Επόμενο', command = self.end_of_page_ticket)
        self.next_button.place(relx = 0.85, rely = 0.9, anchor = 'center')
        self.next_button.configure(background = 'white')
 
        #κουμπί προηγούμενο
        self.prev_button = tk.Button(self.master, text = 'Προηγούμενο', command = self.prev_page)
        self.prev_button.place(relx = 0.15, rely = 0.9, anchor = 'center')
        self.prev_button.configure(background = 'white')

    def end_of_page_ticket(self):
        self.given_name = self.entry_name.get().strip(' ').capitalize()
        self.given_surname = self.entry_surname.get().strip(' ').capitalize()
        self.warning_for_name = tk.Label(self.master, text='Παρακαλώ εισάγετε σωστά τα στοιχεία σας.', fg='white', bg='white')
        self.warning_for_name.place(relx = .25, rely = 0.85)
        if self.given_name == '' or self.given_surname == '':
            self.warning_for_name.configure(fg='red')
        else:
            self.warning_for_name.configure(fg='white')
            if self.typeselected.get() != 'Ολόκληρο' and self.typeselected.get() != 'Παιδικό 50%':
                self.given_code = self.entry_code.get()
                self.warning_for_code = tk.Label(self.master, text='Απαιτείται αριθμός εκπτωτικής κάρτας.', fg='white', bg='white')
                self.warning_for_code.place(relx = .25, rely = 0.85)
                if self.given_code == '':
                    self.warning_for_code.configure(fg='red')
                    del self.given_code
                else:
                    self.collect_credentials()
                    try:
                        del self.given_code
                    except AttributeError: pass
                    self.next_page()
            else:
                self.collect_credentials()
                try:
                    del self.given_code
                except AttributeError: pass
                self.next_page()

    def page_seat_booking(self):
        #first things first
        global did_action_run
        did_action_run = False
        self.current_page = 5

        #το παράθυρο
        self.masterback.pack_forget()
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 800)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
                                        
        #η εικόνα
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.25, rely= 0.365, anchor="s")
        self.master.label.configure(background = 'white')

        #η κάτοψη
        temp_overview = Image.open('seating-plan_translated.png')
        temp_overview = temp_overview.resize((780,300))
        overview = ImageTk.PhotoImage(temp_overview)
        self.master.label1 = tk.Label(self.master, image = overview)
        self.master.label1.image = overview
        self.master.label1.place(relx = 0.5, rely= 0.85, anchor="s")
        self.master.label1.configure(background = 'white')
     
        #κουμπιά
        self.v = tk.StringVar()
        self.v.set(None)
        val = 1
        list_index = 0
        for i in range(0, 5):
            for k in range(0, 2):
                self.seat = tk.Radiobutton(self.master.label1, padx = 0, pady = 0, bg='white', variable=self.v, value=val, command = self.action)
                self.seat.place(relx = 0.15+0.065*i, rely = 0.15+0.163*k)
                val += 1
                if self.availability[list_index] == False:
                    self.seat.configure(bg = 'red', state = 'disabled')
                list_index += 1
        for i in range(0, 6):
            for k in range(0, 2):
                self.seat = tk.Radiobutton(self.master.label1, padx = 0, pady = 0, bg='white', variable=self.v, value=val, command = self.action)
                self.seat.place(relx = 0.59+0.065*i, rely = 0.15+0.163*k)
                val += 1
                if self.availability[list_index] == False:
                    self.seat.configure(bg = 'red', state = 'disabled')
                list_index += 1
        self.seat = tk.Radiobutton(self.master.label1, padx = 0, pady = 0, bg='white', variable=self.v, value=val, command = self.action)
        self.seat.place(relx = 0.913, rely = 0.47)
        val += 1
        if self.availability[list_index] == False:
            self.seat.configure(bg = 'red', state = 'disabled')
        list_index += 1
        for i in range(0, 5):
            for k in range(0, 2):
                self.seat = tk.Radiobutton(self.master.label1, padx = 0, pady = 0, bg='white', variable=self.v, value=val, command = self.action)
                self.seat.place(relx = 0.15+0.065*i, rely = 0.6+0.163*k)
                val += 1
                if self.availability[list_index] == False:
                    self.seat.configure(bg = 'red', state = 'disabled')
                list_index += 1
        for i in range(0, 5):
            for k in range(0, 2):
                self.seat = tk.Radiobutton(self.master.label1, padx = 0, pady = 0, bg='white', variable=self.v, value=val, command = self.action)
                self.seat.place(relx = 0.468+0.065*i, rely = 0.6+0.163*k)
                val += 1
                if self.availability[list_index] == False:
                    self.seat.configure(bg = 'red', state = 'disabled')
                list_index += 1
        for i in range(0, 3):
            for k in range(0, 2):
                self.seat = tk.Radiobutton(self.master.label1, padx = 0, pady = 0, bg='white', variable=self.v, value=val, command = self.action)
                self.seat.place(relx = 0.786+0.065*i, rely = 0.6+0.163*k)
                val += 1
                if self.availability[list_index] == False:
                    self.seat.configure(bg = 'red', state = 'disabled')
                list_index += 1
                    
        #κουμπί βοήθειας
        self.help_button = tk.Button(self.master, text = 'Βοήθεια', command = open_help_win)
        self.help_button.place(relx = 0.9, rely = 0.05, anchor = 'center')
        self.help_button.configure(background = 'white')
 
        #κουμπί επόμενο
        self.next_button = tk.Button(self.master, text = 'Επόμενο', command = self.end_of_page_seat_booking)
        self.next_button.place(relx = 0.85, rely = 0.9, anchor = 'center')
        self.next_button.configure(background = 'white')
 
        #κουμπί προηγούμενο
        self.prev_button = tk.Button(self.master, text = 'Προηγούμενο', command = self.prev_page)
        self.prev_button.place(relx = 0.15, rely = 0.9, anchor = 'center')
        self.prev_button.configure(background = 'white')

    def end_of_page_seat_booking(self):
        global value1, did_action_run
        self.bookingmessage = tk.Label(self.master, text = 'Παρακαλώ επιλέξτε μία ελεύθερη θέση.', bg = 'white', fg = 'white')
        self.bookingmessage.place(relx = 0.4, rely = 0.85)
        if did_action_run == False:
            self.bookingmessage.configure(fg = 'red')
        else:
            did_action_run = False
            desired_seat = self.matching[int(value1)]
            self.all_credentials[-1].append(desired_seat)
            self.availability[int(value1)-1] = False
            self.next_page()

    def action(self):
        global value1, did_action_run
        did_action_run = False
        try:
            self.bookingmessage.configure(fg = 'white')
        except AttributeError: pass
        self.matching = {1:4, 2:3, 3:8, 4:7, 5:12, 6:11, 7:16, 8:15, 9:20, 10:19, 11:28, 12:27, 13:32, 14:31, 15:36, 16:35, 17:40, 18:39, 19:44, 20:43, 21:48, 22:47, \
                    23:49, 24:2, 25:1, 26:6, 27:5, 28:10, 29:9, 30:14, 31:13, 32:18, 33:17, 34:22, 35:21, 36:24, 37:23, 38:26, 39:25, 40:30, 41:29, 42:34, 43:33, \
                    44:38, 45:37, 46:42, 47:41, 48:46, 49:45}
        value1 = self.v.get()
        try:
            self.actionmessage.configure(fg = 'white')
        except AttributeError: pass
        self.actionvar = tk.StringVar()
        self.actionvar.set('Επιλέξατε τη θέση: '+str(self.matching[int(value1)]))
        self.actionmessage = tk.Label(self.master, textvariable=self.actionvar, font = 'Helvetica 14')
        self.actionmessage.place(relx = 0.5, rely = 0.85, anchor = 'center')
        self.actionmessage.configure(background = 'white')
        did_action_run = True

    def times_list(self):
        times = []
        for hour in range(8, 23):
            for minute in [00, 30]:
                times.append('{:02d}:{:02d}'.format(hour,minute))
        return times

    def types_list(self):
        types = ['Ολόκληρο', 'Φοιτητικό 25%', 'Φοιτητικό 50%', 'Παιδικό 50%', 'Τρίτεκνοι 25%', 'Πολύτεκνοι 50%', 'ΑΜΕΑ 50%', 'Στρατιωτική Θητεία 25%', 'Στρατιωτικό Μόνιμοι 15%']
        return types

    def collect_credentials(self):
        sublist = []
        sublist = [self.given_name, self.given_surname, self.typeselected.get()]
        try:
            sublist.append(self.given_code)
            del self.given_code
        except AttributeError:
            sublist.append(None)
        self.all_credentials.append(sublist)

    def page_confirmation(self):
        #first things first
        self.current_page = 6

        #το παράθυρο
        self.masterback.pack_forget()
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 700)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
                                        
        #η εικόνα
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.25, rely= 0.365, anchor="s")
        self.master.label.configure(background = 'white')

        #Μεγάλα γράμματα
        self.Header = tk.Label(self.master, text='Επιβεβαίωση Κράτησης', font = 'Helvetica 18 bold')
        self.Header.place(relx= 0.5, rely = 0.3, anchor = 'center')
        self.Header.configure(background = 'white')

        #prices
        for i in bus.prices:
            if i != 'Πάτρα' and (self.start == i or self.end == i):
                full_price = bus.prices[i]
        
        #κείμενο επιβεβαίωσης
        self.print_date = str(self.given_date)[8:]+'/'+str(self.given_date)[5:7]+'/'+str(self.given_date)[:4]
        conf_text = ''
        conf_text += 'Εισιτήρια από: '+ self.start + ' προς: ' + self.end
        conf_text += '\n'
        conf_text += 'Ημερομηνία: ' + self.print_date + '\n'
        conf_text += 'Ώρα: ' + str(self.given_time) + '\n'
        price = 0
        for i in range(len(self.all_credentials)):
            conf_text += 'Εισιτήριο '+str(i+1)+': '
            conf_text += str(self.all_credentials[i][0]) + ' ' + str(self.all_credentials[i][1]) + '\t\t' + str(self.all_credentials[i][2]) + '\t\tΘέση ' + str(self.all_credentials[i][4])
            conf_text += '\n'
            if ('15%' in self.all_credentials[i][2]):
                price += full_price-(0.15*full_price)
            elif ('25%' in self.all_credentials[i][2]):
                price += full_price-(0.25*full_price)
            elif ('50%' in self.all_credentials[i][2]):
                price += full_price-(0.5*full_price)
            else:
                price += full_price
        conf_text += '\n'
        conf_text += 'Σύνολο: '+str('{:.2f}'.format(price))+'€'
            
        self.message = tk.Label(self.master, text = conf_text, wraplength = 500, justify = 'left')
        self.message.place(relx = 0.05, rely = 0.4)
        self.message.configure(background = 'white')
        
        #κουμπί βοήθειας
        self.help_button = tk.Button(self.master, text = 'Βοήθεια', command = open_help_win)
        self.help_button.place(relx = 0.9, rely = 0.05, anchor = 'center')
        self.help_button.configure(background = 'white')
 
        #κουμπί επόμενο
        self.next_button = tk.Button(self.master, text = 'Τελική Υποβολή', command = self.create_ticket_id)
        self.next_button.place(relx = 0.9, rely = 0.9, anchor = 'center')
        self.next_button.configure(background = 'white')
 
        #κουμπί προηγούμενο
        self.prev_button = tk.Button(self.master, text = 'Προηγούμενο', command = self.prev_page)
        self.prev_button.place(relx = 0.15, rely = 0.9, anchor = 'center')
        self.prev_button.configure(background = 'white')

    def create_ticket_id(self):
        self.ticket_id = ''
        # Επεξήγηση μορφής κωδικού εισιτηρίου:
        # Τα ψηφία 1-2 αντιστοιχούν στην αφετηρία.
        val = 1
        while True:
            if self.start == bus.destinations[val-1]:
                self.ticket_id += '{:02d}'.format(val)
                break
            val += 1
        # Ομοίως, τα ψηφία 3-4 αντιστοιχούν στον προορισμό.
        val = 1
        while True:
            if self.end == bus.destinations[val-1]:
                self.ticket_id += '{:02d}'.format(val)
                break
            val += 1
        # Τα ψηφία 5-12 αντιστοιχούν στην ημερομηνία με μορφή yyyymmdd.
        self.ticket_id = self.ticket_id + str(self.given_date)[:4] + str(self.given_date)[5:7] + str(self.given_date)[8:]
        # Τα ψηφία 13-16 αντιστοιχούν στην ώρα σε μορφή hhmm.
        self.ticket_id = self.ticket_id + str(self.print_time)[:2] + str(self.print_time)[2:4]
        # Το ψηφίο 17 αντιστοιχεί στον τύπο εισιτηρίου.
        for i in range(self.tickets_wanted):
            val = 1
            while True:
                if self.all_credentials[i][2] == self.types_list()[val-1]:
                    self.ticket_id += str(val)
                    break
                val += 1
        # Τα ψηφία 18-19 αντιστοιχούν στον αριθμό θέσης.
            self.ticket_id += '{:02d}'.format(self.all_credentials[i][4])
        # Τα ψηφία 20-25 είναι μοναδικά και δημιουργούνται τυχαία για κάθε εισιτήριο, προκειμένου να εξασφαλιστεί ότι κάποιος δεν θα εξαπατήσει το πρόγραμμα, προσπαθώντας να κλείσει μία κατειλημμένη θέση.
            for k in range(6):
                a = randint(0, 9)
                self.ticket_id += str(a)
        # Τέλος δημιουργίας κωδικού εισιτηρίου.
        # Καταχώρηση κωδικού εισιτηρίου στην all_credentials για κάθε ένα εισιτήριο.
            self.all_credentials[i].append(self.ticket_id)
            self.ticket_id = self.ticket_id[:16]
        self.animation()

    def publish_tickets(self):
        a = str(datetime.datetime.now())
        date, time = a.split(' ')[0], a.split(' ')[1].split('.')[0]
        current_date = date.split('-')[0]+date.split('-')[1]+date.split('-')[2]
        current_time = time.split(':')[0]+time.split(':')[1]+time.split(':')[2]
        pythoncom.CoInitialize()
        self.app = xlwings.App(visible = False)
        self.app.wb = xlwings.Book('template.xlsx')
        for i in range(self.tickets_wanted-1):
            sheet = self.app.wb.sheets[0]
            sheet.api.Copy(Before = sheet.api)
        for i in range(self.tickets_wanted):
            sheet = self.app.wb.sheets[i]
            sheet.range('D9').value = self.all_credentials[i][0]
            sheet.range('D10').value = self.all_credentials[i][1]
            sheet.range('D12').value = self.all_credentials[i][2]
            if self.all_credentials[i][3] == None:
                sheet.range('D13').value = 'N/A'
            else:
                sheet.range('D13').value = self.all_credentials[i][3]
            sheet.range('D16').value = self.start
            sheet.range('F16').value = self.end
            sheet.range('D18').value = self.print_date
            sheet.range('D19').value = self.given_time
            sheet.range('D21').value = self.all_credentials[i][4]
            sheet.range('D23').value = self.all_credentials[i][5]
        self.name = os.path.expanduser('~')+'\\Documents\\ktel_tickets'+current_date+current_time+'.pdf'
        self.app.wb.api.ExportAsFixedFormat(0, self.name)
        self.app.wb.close()
        self.app.kill()
        
        os.startfile(self.name)
        
##        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
##        qr_file = open(current_dir+'\\temp_ticket_files\\ktel_tickets.pdf', 'r')
##        qr.add_data(file = current_dir+'\\temp_ticket_files\\ktel_tickets.pdf')
##        temp_qr_code = qr.make_image()
##        temp_qr_code.save(current_dir+'\\temp_ticket_files\\qr.png')
        self.page_7()

    def page_7(self):
        #first things first
        global current_dir
        self.current_page = 7

        #το παράθυρο
        self.masterback.pack_forget()
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 500, width = 500)
        self.masterback.pack()
        self.masterback.configure(background = 'white')
                                        
        #η εικόνα
        img = tk.PhotoImage(file = image_path)
        self.master.label= tk.Label(self.master, image = img)
        self.master.label.image = img
        self.master.label.place(relx = 0.25, rely= 0.365, anchor="s")
        self.master.label.configure(background = 'white')

        #Μεγάλα γράμματα
        self.Header = tk.Label(self.master, text='Λήψη εισιτηρίων', font = 'Helvetica 18 bold')
        self.Header.place(relx= 0.5, rely = 0.3, anchor = 'center')
        self.Header.configure(background = 'white')

##        #QR Code
##        temp_photo = Image.open(current_dir+'\\temp_ticket_files\\qr.png')
##        temp_photo = temp_photo.resize((200,200))
##        self.qr_code = ImageTk.PhotoImage(temp_photo)
##        self.master.label1 = tk.Label(self.master, image = self.qr_code)
##        self.master.label1.image = self.qr_code
##        self.master.label1.place(relx = 0.5, rely = 0.6, anchor = 'center')
##        self.master.label1.configure(background = 'white')

        #μήνυμα
        self.message = tk.Label(self.master, text='Τα εισιτήριά σας είναι έτοιμα και βρίσκονται αποθηκευμένα στον φάκελο Documents του υπολογιστή σας.\n\nΕυχαριστούμε\
 πολύ για την προτίμηση!', font = 'Helvetica 13', wraplength = 400, justify = 'left')
        self.message.place(relx = 0.5, rely = 0.5, anchor = 'center')
        self.message.configure(background = 'white')
                
        #κουμπί βοήθειας
        self.help_button = tk.Button(self.master, text = 'Βοήθεια', command = open_help_win)
        self.help_button.place(relx = 0.9, rely = 0.05, anchor = 'center')
        self.help_button.configure(background = 'white')
 
        #κουμπί τέλος
        self.end_button = tk.Button(self.master, text = 'Τέλος', command = self.dont_restart)
        self.end_button.place(relx = 0.9, rely = 0.9, anchor = 'center')
        self.end_button.configure(background = 'white')
        
        #κουμπί επανέναρξη
        self.restart_button = tk.Button(self.master, text = 'Επανέναρξη', command = self.restart)
        self.restart_button.place(relx = 0.15, rely = 0.9, anchor = 'center')
        self.restart_button.configure(background = 'white')
        
    def next_page(self):
        if self.current_page == 0: self.page_1()
        elif self.current_page == 1: self.page_2()
        elif self.current_page == 2: self.page_3()
        elif self.current_page == 3: self.page_ticket()
        elif self.current_page == 4:
            self.page_seat_booking()
        elif self.current_page == 5:
            if self.ticket_index < self.tickets_wanted:
                self.ticket_index += 1
                self.page_ticket()
            else: self.page_confirmation()
        
    def prev_page(self):
        global value1
        if self.current_page == 2: self.page_1()
        elif self.current_page == 3: self.page_2()
        elif self.current_page == 4:
            if self.ticket_index == 1:
                self.ticket_index -= 1
                self.page_3()
            else:
                self.ticket_index -= 1
                if len(self.all_credentials) > 0:
                    self.all_credentials[-1].pop(-1)
                for key,value in self.matching.items():
                    if value == int(value1):
                        unwanted_seat = value
                self.availability[unwanted_seat-1] = True
                self.page_seat_booking()
        elif self.current_page == 5:
            if self.ticket_index == 1:
                self.all_credentials.pop(-1)
                self.page_ticket()
            else:
                self.all_credentials.pop(-1)
                self.page_ticket()
        elif self.current_page == 6:
            self.all_credentials[-1].pop(-1)
            self.page_seat_booking()

    def dont_restart(self):
        global restart_flag
        restart_flag = False
        self.master.destroy()

    def restart(self):
        global restart_flag
        restart_flag = True
        self.master.destroy()
        
    def start_loading(self, n=0):
        self.gif = self.giflist[n%len(self.giflist)]
        self.canvas.create_image(self.gif.width()//2, self.gif.height()//2, image=self.gif)
        self.timer_id = self.master.after(100, self.start_loading, n+1)

    def stop_loading(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.canvas.destroy()
            
    def animation(self):
        global current_dir
        #το παράθυρο
        self.masterback.pack_forget()
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
        self.masterback = tk.Frame(height = 300, width = 300)
        self.masterback.pack()
        self.masterback.configure(background = 'white')

        self.FramesFolder = current_dir + '\\loading_gif'
        self.imagelist = [join(self.FramesFolder,s) for s in os.listdir(self.FramesFolder) if not s.endswith('db')]
        # extract width and height info
        self.photo = tk.PhotoImage(file=self.imagelist[0])
        self.width = self.photo.width()
        self.height = self.photo.height()
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg='white', bd = 0, highlightthickness = 0, relief = 'ridge')
        self.canvas.place(relx = 0.25, rely = 0.2)
        self.master.update()
        # create a list of image objects
        self.giflist = []
        for imagefile in self.imagelist:
            self.photo = tk.PhotoImage(file=imagefile)
            self.giflist.append(self.photo)
        
        self.thread = threading.Thread(target = self.publish_tickets)
        self.master.config(cursor='wait')
        self.master.update()
        self.thread.start()
        self.start_loading()
        self.master.after(50, self.check_completed)

    def check_completed(self):
        if self.thread.is_alive():
            self.master.after(50, self.check_completed)
        else:
            self.stop_loading()
            self.master.config(cursor='')
            self.master.update()
            self.page_7()   

class help_window():
    def __init__(self):
        #first things first
        global icon
        
        winmaster = tk.Toplevel()
        self.master = winmaster
        self.master.geometry('600x550')
        self.master.option_add("*Font", 'helvetica 10')
        self.master.title('Εφαρμογή Κράτησης Θέσης ΚΤΕΛ ΑΧΑΪΑΣ -- Οδηγίες Χρήσης')
        self.master.configure(background = 'white')
        self.master.resizable(False, False)
 
        self.masterback = tk.Frame()
        self.masterback.pack()
        self.masterback.configure(background = 'white')

        #HEADER
        self.help_header = tk.Label(self.master, text = 'ΟΔΗΓΙΕΣ ΧΡΗΣHΣ', font = 'Helvetica 20')
        self.help_header.place(relx = 0.5, rely = 0.1, anchor = 's')
        self.help_header.configure(background = 'white')

        self.Message2 = tk.Label(self.master, text="""Καλώς ήρθατε στο σύστημα κρατήσεων θέσεων λεωφορείων της ΚΤΕΛ Αχαΐας. Για να εισέλθετε στο σύστημα, \
πατήστε 'Είσοδος'. Για να κλείσετε τα εισιτήριά σας, ακολουθήστε τα παρακάτω βήματα:\n1. Ξεκινήστε επιλέγοντας αφετηρία και προορισμό.\n2. Επιλέξτε ημερομηνία \
και ώρα αναχώρησης.\n3. Εισάγετε το ονοματεπώνυμο στο οποίο θα γίνει η κράτηση και επιλέξτε αριθμό εισιτηρίων (μέγιστος 4).\n4. Για κάθε ένα από τα εισιτήρια \
που επιλέξατε, εισάγετε ονοματεπώνυμο επιβάτη (για το πρώτο εισιτήριο είναι προεπιλεγμένο το ονοματεπώνυμο κράτησης \
και επιλέξτε είδος κομίστρου. Εάν ο επιβάτης δικαιούται μειωμένο εισιτήριο, εισάγετε τον αριθμό της κάρτας (π.χ. αριθμός κάρτας πολυτέκνων για πολύτεκνους). \
Η έκπτωση εισιτηρίου ισχύει στους φοιτητές Ελληνικών πανεπιστημίων και Τεχνολογικών ιδρυμάτων (Α.Ε.Ι. & Τ.Ε.Ι.), κάτοχοι Ακαδημαϊκής ταυτότητας, \
ΑΜΕΑ και πολύτεκνους αναγνωρισμένους από το Ελληνικό κράτος.\n5. Με τη βοήθεια του πλάνου ελεύθερων θέσεων, επιλέξτε για κάθε εισιτήριο τις θέσεις που επιθυμείτε. \
Στις κατειλημμένες θέσεις, το πλήκτρο επιλογής είναι απενεργοποιημένο.\n6. Επιβεβαιώστε τα στοιχεία που υποβάλατε και εφόσον σιγουρευτείτε για την ορθότητά τους \
πατήστε το κουμπί 'Τελική Υποβολή'.\n7. Τα εισιτήριά σας είναι έτοιμα και είναι αποθηκευμένα σε αρχείο PDF στον φάκελο Documents του υπολογιστή σας.
Ευχαριστούμε για την προτίμηση και σας ευχόμαστε καλό ταξίδι!""", wraplength = 500, justify = 'left')
        self.Message2.configure(background = 'white')
        self.Message2.place(relx = 0.5, rely = 0.55, anchor = 'center')
        self.master.tk.call('wm', 'iconphoto', self.master._w, icon)
        self.master.mainloop()
 
#δημιουργεί το παράθυρο βοήθειας
def open_help_win():
    h = help_window()
 
def on_closing():
    global restart_flag
    if messagebox.askokcancel("Έξοδος", "Είστε σίγουρος ότι θέλετε να κλείσετε την εφαρμογή;"):
        restart_flag = False
        a.destroy()

def main():
    global a, icon, win1
    a = tk.Tk()
    win1 = window_1(a)
    a.protocol("WM_DELETE_WINDOW", on_closing)
    icon = tk.PhotoImage(file=image_path)
    a.tk.call('wm', 'iconphoto', a._w, icon)
    a.mainloop()

restart_flag = True
while restart_flag:
    main()
