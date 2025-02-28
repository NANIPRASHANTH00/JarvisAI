#!/usr/bin/env python3
import sys
import os
import time
import pickle
import termios
import tty

# Define ANSI escape functions and console I/O functions

def gotoxy(x, y):
    # Move cursor to column x, row y (ANSI escape code)
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

def clrscr():
    # Clear screen: using system command depending on OS
    os.system('cls' if os.name == 'nt' else 'clear')

def clreol():
    # Clear from cursor to end of line
    sys.stdout.write("\033[K")
    sys.stdout.flush()

def delay(ms):
    # Delay in milliseconds
    time.sleep(ms / 1000.0)

# Color constants (ANSI color codes) for textcolor and textbackground
# These values are illustrative approximations.
LIGHTBLUE = 94
BLINK = 5
LIGHTGRAY = 37
RED = 31
BLACK = 30
WHITE = 37
GREEN = 42

def textcolor(color):
    # Set text color using ANSI escape codes.
    # Using SGR parameter 38;5;{n}m may be more complete but here we simply choose basic colors.
    sys.stdout.write(f"\033[{color}m")
    sys.stdout.flush()

def textbackground(color):
    # Set background color. For simplicity if color is given as constant, use it as background.
    # Note: In many calls, color is manipulated by addition.
    # We assume that if color is provided (like GREEN) it corresponds directly.
    sys.stdout.write(f"\033[{color + 10}m")
    sys.stdout.flush()

def reset_attributes():
    # Reset attributes to default
    sys.stdout.write("\033[0m")
    sys.stdout.flush()

def cprintf(s):
    # Print string without newline (simulate conio.cprintf)
    sys.stdout.write(s)
    sys.stdout.flush()

# getch and getche implementation (reads one character from stdin)
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getche():
    ch = getch()
    sys.stdout.write(ch)
    sys.stdout.flush()
    return ch

# gets function - in C++ gets() reads a line. We emulate using input() without prompt.
def gets(buffer=None):
    # We simply use input() to obtain a string from the user.
    # The buffer parameter is ignored.
    return input()

# -------- Classes as in original C++ code --------

class DRAW:
    # Mimics class DRAW in C++
    def __init__(self):
        pass

    def LINE_HOR(self, column1, column2, row, c):
        # Translate: for ( column1; column1<=column2; column1++ )
        while column1 <= column2:
            gotoxy(column1, row)
            cprintf(c)
            column1 += 1

    def LINE_VER(self, row1, row2, column, c):
        while row1 <= row2:
            gotoxy(column, row1)
            cprintf(c)
            row1 += 1

    def BOX(self, column1, row1, column2, row2, c):
        ch = chr(218)
        c1 = c2 = c3 = c4 = ''
        l1 = chr(196)
        l2 = chr(179)
        if c == ch:
            c1 = chr(218)
            c2 = chr(191)
            c3 = chr(192)
            c4 = chr(217)
            l1 = chr(196)
            l2 = chr(179)
        else:
            c1 = c
            c2 = c
            c3 = c
            c4 = c
            l1 = c
            l2 = c
        gotoxy(column1, row1)
        cprintf(c1)
        gotoxy(column2, row1)
        cprintf(c2)
        gotoxy(column1, row2)
        cprintf(c3)
        gotoxy(column2, row2)
        cprintf(c4)
        column1 += 1
        column2 -= 1
        self.LINE_HOR(column1, column2, row1, l1)
        self.LINE_HOR(column1, column2, row2, l1)
        column1 -= 1
        column2 += 1
        row1 += 1
        row2 -= 1
        self.LINE_VER(row1, row2, column1, l2)
        self.LINE_VER(row1, row2, column2, l2)

class TICKET:
    # Mimics class TICKET in C++
    def __init__(self):
        # Protected members: fltno, from, to; economic and executive fair.
        self.fltno = ""
        self.__dict__["from"] = ""
        self.to = ""
        self.ecofair = 0
        self.exefair = 0

    def ADD_RECORD(self, t_fltno, t_from, t_to, t_ecofair, t_exefair):
        # Open file "TICKET.DAT" in append binary mode.
        try:
            file = open("TICKET.DAT", "ab")
        except:
            file = open("TICKET.DAT", "wb")
        self.fltno = t_fltno
        self.__dict__["from"] = t_from
        self.to = t_to
        self.ecofair = t_ecofair
        self.exefair = t_exefair
        pickle.dump(self, file)
        file.close()

    def FLIGHTNO(self, sno):
        try:
            file = open("TICKET.DAT", "rb")
        except:
            return ""
        count = 1
        result = ""
        while True:
            try:
                rec = pickle.load(file)
                if sno == count:
                    result = rec.fltno
                    break
                count += 1
            except EOFError:
                break
        file.close()
        return result

    def ADDITION(self):
        # Open file "TICKET.DAT" in read binary mode; if exists, simply return.
        if os.path.exists("TICKET.DAT"):
            try:
                file = open("TICKET.DAT", "rb")
                file.close()
                return
            except:
                pass
        # If not present, add default records.
        self.ADD_RECORD("KL146", "DELHI", "MUMBAI", 1500, 1700)
        self.ADD_RECORD("KL146", "MUMBAI", "DELHI", 1500, 1700)
        self.ADD_RECORD("KL156", "DELHI", "CALCUTTA", 1700, 1900)
        self.ADD_RECORD("KL156", "CALCUTTA", "DELHI", 1700, 1900)
        self.ADD_RECORD("KL166", "DELHI", "MADRAS", 2100, 2300)
        self.ADD_RECORD("KL166", "MADRAS", "DELHI", 2100, 2300)
        self.ADD_RECORD("KL176", "MUMBAI", "CALCUTTA", 1900, 2100)
        self.ADD_RECORD("KL176", "CALCUTTA", "MUMBAI", 1900, 2100)
        self.ADD_RECORD("KL186", "MUMBAI", "MADRAS", 1800, 2000)
        self.ADD_RECORD("KL186", "MADRAS", "MUMBAI", 1800, 2000)
        self.ADD_RECORD("KL196", "CALCUTTA", "MADRAS", 1600, 1800)
        self.ADD_RECORD("KL196", "MADRAS", "CALCUTTA", 1600, 1800)

    def ENQUIRY(self):
        clrscr()
        try:
            file = open("TICKET.DAT", "rb")
        except:
            return
        d = DRAW()
        d.BOX(1, 2, 80, 24, chr(218))
        d.LINE_HOR(2, 79, 4, chr(196))
        d.LINE_HOR(2, 79, 6, chr(196))
        d.LINE_HOR(2, 79, 22, chr(196))
        textcolor(RED + BLINK)
        gotoxy(30, 3)
        cprintf("LIST OF THE FLIGHTS")
        textcolor(RED)
        textcolor(WHITE)
        textbackground(GREEN)
        for i in range(2, 80):
            gotoxy(i, 5)
            cprintf(" ")
        gotoxy(2, 5)
        cprintf(" Sno. FLIGHT NO.    FROM          TO           ECONOMIC FAIR  EXECUTIVE FAIR")
        textcolor(LIGHTGRAY)
        textbackground(BLACK)
        row = 7
        sno = 1
        while True:
            try:
                rec = pickle.load(file)
                gotoxy(4, row)
                cprintf(str(sno))
                gotoxy(9, row)
                cprintf(rec.fltno)
                gotoxy(20, row)
                cprintf(rec.__dict__["from"])
                gotoxy(34, row)
                cprintf(rec.to)
                gotoxy(52, row)
                cprintf(str(rec.ecofair))
                gotoxy(67, row)
                cprintf(str(rec.exefair))
                row += 1
                sno += 1
            except EOFError:
                break
        file.close()
        reset_attributes()

class PASSANGER:
    # Mimics class PASSANGER in C++
    def __init__(self):
        # Protected members: Class, name, address, sex, slno, age, ticketno.
        self.Class = ''
        self.name = ""
        self.address = ""
        self.sex = ''
        self.slno = 0
        self.age = 0
        self.ticketno = 0

    def ADD_RECORD(self, tno, sno, pname, paddress, page, psex, pclass):
        try:
            file = open("PASS.DAT", "ab")
        except:
            file = open("PASS.DAT", "wb")
        self.ticketno = tno
        self.slno = sno
        self.name = pname
        self.address = paddress
        self.age = page
        self.sex = psex
        self.Class = pclass
        pickle.dump(self, file)
        file.close()

    def LAST_TICKETNO(self):
        count = 0
        try:
            file = open("PASS.DAT", "rb")
        except:
            return count
        while True:
            try:
                rec = pickle.load(file)
                count = rec.ticketno
            except EOFError:
                break
        file.close()
        return count

    def SEATS(self, sno):
        count = 0
        try:
            file = open("PASS.DAT", "rb")
        except:
            return count
        while True:
            try:
                rec = pickle.load(file)
                if sno == rec.slno:
                    count += 1
            except EOFError:
                break
        file.close()
        return count

    def FOUND(self, tno):
        found = 0
        try:
            file = open("PASS.DAT", "rb")
        except:
            return found
        while True:
            try:
                rec = pickle.load(file)
                if tno == rec.ticketno:
                    found = 1
                    break
            except EOFError:
                break
        file.close()
        return found

    def NAME(self, tno):
        s = ""
        try:
            file = open("PASS.DAT", "rb")
        except:
            return s
        while True:
            try:
                rec = pickle.load(file)
                if tno == rec.ticketno:
                    s = rec.name
                    break
            except EOFError:
                break
        file.close()
        return s

    def LIST(self):
        clrscr()
        t1 = ""
        valid = 0
        ticket = TICKET()
        ticket.ENQUIRY()
        while True:
            valid = 1
            gotoxy(3, 23)
            cprintf("                                  ")
            gotoxy(3, 23)
            cprintf("PRESS <ENTER> TO EXIT")
            gotoxy(3, 20)
            cprintf("                                                                       ")
            gotoxy(3, 20)
            cprintf("Enter Sno. of the FLIGHT for which you want to see list of passanger ")
            t1 = gets()
            try:
                t2 = int(t1)
            except:
                t2 = 0
            sno = t2
            if len(t1) == 0:
                return
            if sno < 1 or sno > 12:
                valid = 0
                gotoxy(3, 23)
                cprintf("                           ")
                gotoxy(3, 23)
                cprintf("\7ENTER CORRECTLY")
                getch()
            if valid:
                break
        clrscr()
        row = 7
        found = 0
        flag = 0
        ch = ''
        d = DRAW()
        d.BOX(1, 2, 80, 24, chr(218))
        d.LINE_HOR(2, 79, 4, chr(196))
        d.LINE_HOR(2, 79, 6, chr(196))
        d.LINE_HOR(2, 79, 22, chr(196))
        gotoxy(3, 3)
        cprintf("Flight no. " + ticket.FLIGHTNO(sno))
        gotoxy(32, 3)
        cprintf("LIST OF PASSANGER")
        textcolor(BLACK)
        textbackground(WHITE)
        gotoxy(2, 5)
        cprintf(" TICKET NO.    NAME                            CLASS                          ")
        textcolor(LIGHTGRAY)
        textbackground(BLACK)
        try:
            file = open("PASS.DAT", "rb")
        except:
            return
        # Ensure pointer at beginning
        file.seek(0, os.SEEK_SET)
        while True:
            try:
                rec = pickle.load(file)
                if sno == rec.slno:
                    flag = 0
                    delay(20)
                    found = 1
                    gotoxy(5, row)
                    cprintf(str(rec.ticketno))
                    gotoxy(17, row)
                    cprintf(rec.name)
                    gotoxy(49, row)
                    if rec.Class == 'X':
                        cprintf("Executive")
                    else:
                        cprintf("Economic")
                    if row == 21:
                        flag = 1
                        row = 7
                        gotoxy(5, 23)
                        cprintf("Press any key to continue or Press <ESC> to exit")
                        ch = getch()
                        if ord(ch) == 27:
                            break
                        clrscr()
                        d.BOX(1, 2, 80, 24, chr(218))
                        d.LINE_HOR(2, 79, 4, chr(196))
                        d.LINE_HOR(2, 79, 6, chr(196))
                        d.LINE_HOR(2, 79, 22, chr(196))
                        gotoxy(32, 3)
                        cprintf("LIST OF PASSANGER")
                        textcolor(BLACK)
                        textbackground(WHITE)
                        gotoxy(2, 5)
                        cprintf(" TICKET NO.    NAME                     FLIGHT NO.           CLASS            ")
                        textcolor(LIGHTGRAY)
                        textbackground(BLACK)
                    else:
                        row += 1
            except EOFError:
                break
        if not found:
            gotoxy(5, 10)
            cprintf("\7Records not found")
        if not flag:
            gotoxy(5, 23)
            cprintf("Press any key to continue...")
            getch()
        file.close()
        reset_attributes()

    def DELETE_TICKET(self, tno):
        try:
            file = open("PASS.DAT", "rb")
        except:
            return
        temp = open("temp.dat", "wb")
        # Read all records and write those which do not match tno
        while True:
            try:
                rec = pickle.load(file)
                if tno != rec.ticketno:
                    pickle.dump(rec, temp)
            except EOFError:
                break
        file.close()
        temp.close()

        file = open("PASS.DAT", "wb")
        try:
            temp = open("temp.dat", "rb")
        except:
            return
        temp.seek(0, os.SEEK_SET)
        while True:
            try:
                rec = pickle.load(temp)
                pickle.dump(rec, file)
            except EOFError:
                break
        file.close()
        temp.close()

    def DELETE_FLIGHT(self, sno):
        try:
            file = open("PASS.DAT", "rb")
        except:
            return 0
        temp = open("temp.dat", "wb")
        file.seek(0, os.SEEK_SET)
        found = 0
        while True:
            try:
                rec = pickle.load(file)
                if sno != rec.slno:
                    pickle.dump(rec, temp)
                else:
                    found = 1
            except EOFError:
                break
        file.close()
        temp.close()
        file = open("PASS.DAT", "wb")
        try:
            temp = open("temp.dat", "rb")
        except:
            return found
        temp.seek(0, os.SEEK_SET)
        while True:
            try:
                rec = pickle.load(temp)
                pickle.dump(rec, file)
            except EOFError:
                break
        file.close()
        temp.close()
        return found

class RESERVE(TICKET, PASSANGER):
    # Inherits from TICKET and PASSANGER
    def __init__(self):
        TICKET.__init__(self)
        PASSANGER.__init__(self)

    def RESERVATION(self):
        clrscr()
        self.ENQUIRY()
        t1 = ""
        pclass = ''
        pname = ""
        paddress = ""
        psex = ''
        pfltno = ""
        t2 = 0
        valid = 0
        page = 0
        tno = 0
        sno = 0
        p = PASSANGER()
        tno = p.LAST_TICKETNO() + 1
        while True:
            valid = 1
            gotoxy(3, 23)
            cprintf("                                  ")
            gotoxy(3, 23)
            cprintf("PRESS <ENTER> TO EXIT")
            gotoxy(3, 20)
            cprintf("                                  ")
            gotoxy(3, 20)

