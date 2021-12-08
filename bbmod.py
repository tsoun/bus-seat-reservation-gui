 from random import random

#κλάση Πελάτης (συλλογή και τύπωση δεδομένων του πελάτη)
class client():
    def __init__(self, _NAME_, _AGE_, _DEST_):
        self.name = _NAME_
        self.age = _AGE_
        self.destination = _DEST_
    def __str__(self):
        return str('Όνομα πελάτη: ' + self.name + '\nΗλικία: ' + str(self.age) + '\nΠροορισμός: ' + self.destination)
 
#υποκλάση της κλάσης Πελάτης (η ίδια, αλλά δηλώνεις και πάσο)
class student_client(client):
    def __init__(self, _NAME_, _AGE_, _DEST_, _PASS_):
        super().__init__(_NAME_, _AGE_, _DEST_)
        self.passUni = _PASS_
    def __str__(self):
        return str('Όνομα πελάτη: ' + self.name+ '\nΗλικία: ' + str(self.age) + '\nΠροορισμός ' + self.destination + '\nΑριθμός Ακαδημαϊκής Ταυτότητας: ' + str(self.passUni))
 
#κλάση Μεταφορικού Μέσου
class bus():
    def __init__(self, _INPUT_FILE_ = (open('bin\\data.txt', 'r', encoding = 'UTF-8'))):
        global flag
        self.seats = 50
        self.numOfSeats = 0
        self.f = _INPUT_FILE_
        self.aseats = []
        self.destinations = []
        self.prices = {}
        destNum = sum(1 for line in self.f)
        self.f.seek(0, 0)
        for line in self.f:
            town = line.split(' ')
            town1 = str(town[-2].rstrip())
            price = float(town[-1].rstrip())
            self.destinations.append(town1)
            self.prices.update({town1: price})
    def showSchedule(self):         #δείχνει τα δρομολόγια
        for i in self.destinations:
            print('Πάτρα - ' + i)
    def showAvailSeats(self):       #δείχνει τις διαθέσιμες θέσεις
        for i in range(1, (self.seats + 1), 2):
            print('Θέση ' + str(i) + ': ' + self.aseats[i] + '\t Θέση ' + str(i + 1) + ': ' + self.aseats[i])
        print('Διαθέσιμες θέσεις συνολικά: ' + str(self.numOfSeats))
    def showAvailability(self): ########### add dest
        flag = []
        self.seats_list = [i for i in range(1, 50)]
        for self.seat in self.seats_list:
            if random() > 1 / 2:
                flag.append(False)
            else: flag.append(True)
        return flag
