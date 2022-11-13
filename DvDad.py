# DVD database applicatin for Dad to sort his DVDs

import sqlite3
import datetime
import sys
from tkinter import *

screenSize = "1200x700+360+150"
smallScreenSize = "400x200+760+350"
mainMenuTitle = "Main Menu"
mainbg = "#525867"
btnbg = "#646B79"
activebtnbg = "#575D6A"
mainfg = "#ffffff"
mainFont = "Arial 18 bold"
white = "#ffffff"
red = "#D73A3A"
dark_red = "#AF3232"
green = "#4DD73A"
dark_green = "#3DAA2E"
yellow = "#EEF629"
dark_yellow = "#BFC522"
entryFont = "Arial 18"
rbFont = "Arial 12 bold"
small_btn_font = "Arial 14 bold"
sm_btn_width = 10
sm_btn_height = 2

conn = sqlite3.connect("DVDs.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS dvds(
    dvd_ID INTEGER NOT NULL PRIMARY KEY, dvd_name TEXT, runtimeHours INTEGER, runtimeMins INTEGER,
    date INTEGER, location TEXT)'''
)

c.execute('''CREATE TABLE IF NOT EXISTS directors(
    director_ID INTEGER NOT NULL PRIMARY KEY, director_name TEXT)'''
)

c.execute('''CREATE TABLE IF NOT EXISTS genres(
    genre_ID INTEGER NOT NULL PRIMARY KEY, genre_name TEXT)'''
)

c.execute('''CREATE TABLE IF NOT EXISTS dirate(
    dvd_ID INTEGER, director_ID INTEGER, genre_ID INTEGER,
    FOREIGN KEY (dvd_ID) REFERENCES dvds (dvd_ID),
    FOREIGN KEY (director_ID) REFERENCES directors(director_ID),
    FOREIGN KEY (genre_ID) REFERENCES genres(genre_ID))'''
)


def addCD(mainMenu):
    mainMenu.withdraw()

    add_CD_screen = Toplevel()
    add_CD_screen.geometry(screenSize)
    add_CD_screen.title("Add a CD")
    add_CD_screen["bg"] = mainbg
    
    confirm_btn = Button(add_CD_screen, text="Confirm", command=lambda: confirmCD(add_CD_screen, mainMenu), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=sm_btn_width, height=sm_btn_height)
    confirm_btn.pack()
            
    menu_btn = Button(add_CD_screen, text="Back to\n main menu", command=lambda: back_to_menu(add_CD_screen, mainMenu), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=sm_btn_width, height=sm_btn_height)
    menu_btn.pack()

    add_CD_screen.mainloop()

def searchCD(mainMenu):
    mainMenu.withdraw()

    search_CD_screen = Toplevel()
    search_CD_screen.geometry(screenSize)
    search_CD_screen.title("Search CDs")
    search_CD_screen["bg"] = mainbg
        
    menu_btn = Button(search_CD_screen, text="Back to\n main menu", command=lambda: back_to_menu(search_CD_screen, mainMenu), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg)
    menu_btn.pack()

    search_CD_screen.mainloop()

def backToSearch(screen):

    screen.destroy()

def confirmDelete(mainMenu, searchScreen, editScreen, deleteScreen, dvd_details_list):

    c.execute('''DELETE FROM dirate WHERE dvd_ID = ?''',
            (dvd_details_list[0],))
    conn.commit()
    c.execute('''DELETE FROM dvds WHERE dvd_ID = ?''',
              (dvd_details_list[0],))
    conn.commit()
    
    deleteScreen.destroy()
    editScreen.destroy()
    back_to_menu(searchScreen, mainMenu)

def deleteDVD(mainMenu, searchScreen, editScreen, dvd_details_list):

    deleteScreen = Toplevel()
    deleteScreen.title = ("Confirm")
    deleteScreen.geometry(smallScreenSize)
    deleteScreen["bg"] = mainbg

    frame1 = Frame(deleteScreen, bg=mainbg) #label
    frame2 = Frame(deleteScreen, bg=mainbg) #buttons

    spaceLab1 = Label(frame1, text="", bg=mainbg)
    spaceLab1.pack()

    savedLab = Label(frame1, text="Delete this DVD?", bg=mainbg, fg=mainfg, font=mainFont)
    savedLab.pack()

    spaceLab2 = Label(frame1, text="", bg=mainbg)
    spaceLab2.pack()

    delete_btn = Button(frame2, text="Delete", command=lambda: confirmDelete(mainMenu, searchScreen, editScreen, deleteScreen, dvd_details_list), bg=red, activebackground=dark_red, fg=mainfg, activeforeground=mainfg, font=mainFont)
    delete_btn.pack(side=LEFT)

    back_btn = Button(frame2, text="Back", command=lambda: backToSearch(deleteScreen), bg=mainbg, activebackground=activebtnbg, activeforeground=mainfg, fg=mainfg, font=mainFont)
    back_btn.pack(side=LEFT)

    frame1.pack()
    frame2.pack()

    deleteScreen.mainloop()


    

def saveConfirm(mainMenu, searchScreen, editScreen, saveConfirmScreen):

    saveConfirmScreen.destroy()
    editScreen.destroy()
    searchScreen.destroy()
    mainMenu.deiconify()
    
def saveChanges(mainMenu, searchScreen, editScreen, dvd_name, dvd_details_list, getgen, getdate, DVDnameEntry, runtimeHoursEntry, runtimeMinutesEntry, directorEntry, locationEntry):

    new_DVDname = DVDnameEntry.get()
    new_runtimeHours = int(runtimeHoursEntry.get())
    new_runtimeMinutes = int(runtimeMinutesEntry.get())
    new_year = int(getdate())
    new_location = locationEntry.get()
    new_genre = getgen()
    new_director = directorEntry.get()

    if new_runtimeHours == "": #if hours or minutes is left blank, put a 0 there
        new_runtimeHours = 0
    if new_runtimeMinutes == "":
        new_runtimeMinutes = 0
    if new_DVDname == "" or new_location == "" or new_director == "": #if any of these are left empty, data cannot be inputted into database
        confirmDVDFailure()


    if new_DVDname != dvd_name:
        c.execute('''UPDATE dvds SET dvd_name = ? WHERE dvd_ID = ?''',
                  (new_DVDname, dvd_details_list[0],))
        conn.commit()
    if new_runtimeHours != dvd_details_list[1]:
        c.execute('''UPDATE dvds SET runtimeHours = ? WHERE dvd_ID = ?''',
                  (new_runtimeHours, dvd_details_list[0],))
        conn.commit()
    if new_runtimeMinutes != dvd_details_list[2]:
        c.execute('''UPDATE dvds SET runtimeMins = ? WHERE dvd_ID = ?''',
                  (new_runtimeMinutes, dvd_details_list[0]))
        conn.commit()
    if new_year != dvd_details_list[3]:
        c.execute('''UPDATE dvds SET date = ? WHERE dvd_ID = ?''',
                  (new_year, dvd_details_list[0],))
        conn.commit()
    if new_location != dvd_details_list[4]:
        c.execute('''UPDATE dvds SET location = ? WHERE dvd_ID = ?''',
                  (new_location, dvd_details_list[0],))
        conn.commit()
    if new_genre != dvd_details_list[6]:
        c.execute('''SELECT genre_ID FROM genres WHERE genre_name = ?''',
                  (new_genre,)) #get genre id, so can update dirate, as that table only uses IDs
        for row in c.fetchall():
            print(row)
        dvd_genre_ID = list(row)
        c.execute('''UPDATE dirate SET genre_ID = ? WHERE dvd_ID = ?''',
                  (dvd_genre_ID[0], dvd_details_list[0],))
        conn.commit()
    if new_director != dvd_details_list[5]: #if the new director is different (i.e. is it a typo or diff director?)
        c.execute('''SELECT director_ID FROM dirate WHERE dvd_ID = ?''',
                  (dvd_details_list[0],)) #first retrieve directorID from the database
        for row in c.fetchall():
            print(row)
        dirID = list(row) #director ID
        howManyDirectors_list = []
        c.execute('''SELECT dvd_ID FROM dirate WHERE director_ID = ?''',
                  (dirID[0],)) #now check to see if that director has directed multiple movies
        for row in c.fetchall():
            howManyDirectors_list.append(row[0])
        if len(howManyDirectors_list) > 1:
            #print("There are multiple movies directed by this director") #find out if the new director exists
            if c.execute('''SELECT EXISTS(SELECT 1 FROM directors WHERE director_name = ?)''', (new_director,)).fetchone() == (1,):
                #the director does exist, now need to find out their ID so can change dirate
                c.execute('''SELECT director_ID FROM directors WHERE director_name = ?''',
                          (new_director,))
                for row in c.fetchall():
                    print(row)
                newDirID = list(row) #new director's ID              
                c.execute('''UPDATE dirate SET director_ID = ? WHERE dvd_ID = ?''',
                          (newDirID[0], dvd_details_list[0],)) #changed the director to the new one in dirate; now the dvd and new director are linked
                conn.commit()
            else:
                #need to make a new record in directors and change dirate
                c.execute('''INSERT INTO directors(director_name) VALUES(?)''',
                          (new_director,))
                conn.commit()
                c.execute('''SELECT director_ID FROM directors WHERE director_name = ?''',
                          (new_director,))
                for row in c.fetchall():
                    print(row)
                    newDirID = list(row)
                c.execute('''UPDATE dirate SET director_ID = ? WHERE dvd_ID = ?''',
                          (newDirID[0], dvd_details_list[0],))
                conn.commit()
        else:
            #delete old director record and make new one AND change dirate
            c.execute('''DELETE FROM directors WHERE director_ID = ?''',
                      (dirID[0],))
            conn.commit()
            if c.execute('''SELECT EXISTS(SELECT 1 FROM directors WHERE director_name = ?)''', (new_director,)).fetchone() == (1,):
                #the director does exist, now need to find out their ID so can change dirate
                c.execute('''SELECT director_ID FROM directors WHERE director_name = ?''',
                          (new_director,))
                for row in c.fetchall():
                    print(row)
                newDirID = list(row) #new director's ID              
                c.execute('''UPDATE dirate SET director_ID = ? WHERE dvd_ID = ?''',
                          (newDirID[0], dvd_details_list[0],)) #changed the director to the new one in dirate; now the dvd and new director are linked
                conn.commit()
            else:
                #need to make a new record in directors and change dirate
                c.execute('''INSERT INTO directors(director_name) VALUES(?)''',
                          (new_director,))
                conn.commit()
                c.execute('''SELECT director_ID FROM directors WHERE director_name = ?''',
                          (new_director,))
                for row in c.fetchall():
                    print(row)
                    newDirID = list(row)
                c.execute('''UPDATE dirate SET director_ID = ? WHERE dvd_ID = ?''',
                          (newDirID[0], dvd_details_list[0],))
                conn.commit()

    saveConfirmScreen = Toplevel()
    saveConfirmScreen.title = ("Confirm")
    saveConfirmScreen.geometry(smallScreenSize)
    saveConfirmScreen["bg"] = mainbg

    spaceLab1 = Label(saveConfirmScreen, text="", bg=mainbg)
    spaceLab1.pack()
        
    savedLab = Label(saveConfirmScreen, text="Saved changes!", bg=mainbg, fg=mainfg, font=mainFont)
    savedLab.pack()

    spaceLab2 = Label(saveConfirmScreen, text="", bg=mainbg)
    spaceLab2.pack()

    saved_btn = Button(saveConfirmScreen, text="OK", command=lambda: saveConfirm(mainMenu, searchScreen, editScreen, saveConfirmScreen), bg=mainbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, font=mainFont)
    saved_btn.pack()

    saveConfirmScreen.mainloop()
  

def editDVD(mainMenu, searchScreen, dvdDetails, dvd_name, dvd_details_list): #basically the addDVD screen, but the confirm btn updates instead of adds

    dvdDetails.destroy()

    editScreenTitle = "Edit DVD details"
    spacelabelheight = 2

    def getgen():
        genre = gen.get()
        return genre

    def getdate():
        date = variable.get()
        return date

    editScreen = Toplevel()
    editScreen.title(editScreenTitle)
    editScreen.geometry(screenSize)
    editScreen["bg"] = mainbg

    frame00 = Frame(editScreen, bg=mainbg) #title space
    frame0 = Frame(editScreen, bg=mainbg) #confirm/back button
    frame1 = Frame(editScreen, bg=mainbg) #dvd name
    frame1_5 = Frame(editScreen, bg=mainbg) #s p a c e
    frame2 = Frame(editScreen, bg=mainbg) #runtime
    frame2_5 = Frame(editScreen, bg=mainbg) #s p a c e
    frame3 = Frame(editScreen, bg=mainbg) #director
    frame3_5 = Frame(editScreen, bg=mainbg) #s p a c e
    frame4 = Frame(editScreen, bg=mainbg) #location
    frame4_5 = Frame(editScreen, bg=mainbg) #s p a c e
    frame5 = Frame(editScreen, bg=mainbg) #release year
    frame5_5 = Frame(editScreen, bg=mainbg) #s p a c e
    frame6 = Frame(editScreen, bg=mainbg) #genre
    frameSpace = Frame(editScreen, bg=mainbg) #give space
    frame7 = Frame(editScreen, bg=mainbg) #genre radiobuttons
    frame8 = Frame(editScreen, bg=mainbg) #genre radiobuttons 2

    titleLabel = Label(frame00, text="", font=mainFont, bg=mainbg, fg=mainfg) 
    titleLabel.pack()

    menu_btn = Button(frame0, text="Cancel", command=lambda: backToSearch(editScreen), font=small_btn_font, bg=yellow, fg=mainfg, activebackground=dark_yellow, activeforeground=mainfg,width=sm_btn_width, height=sm_btn_height)
    menu_btn.pack()

    delete_btn = Button(frame0, text="Delete\nDVD", command=lambda: deleteDVD(mainMenu, searchScreen, editScreen, dvd_details_list), font=small_btn_font, bg=red, fg=mainfg, activebackground=dark_red, activeforeground=mainfg,width=sm_btn_width, height=sm_btn_height)
    delete_btn.pack()

    confirm_btn = Button(frame0, text="Save\nchanges", command=lambda: saveChanges(mainMenu, searchScreen, editScreen, dvd_name, dvd_details_list, getgen, getdate, DVDnameEntry, runtimeHoursEntry, runtimeMinutesEntry, directorEntry, locationEntry), font=small_btn_font, bg=green, fg=mainfg, activebackground=dark_green, activeforeground=mainfg,width=sm_btn_width, height=sm_btn_height)
    confirm_btn.pack()
    
    DVDnameLabel = Label(frame1, text="DVD Title:", font=mainFont, bg=mainbg, fg=mainfg, width=28)
    DVDnameLabel.pack(side=LEFT)

    DVDnameEntry = Entry(frame1, font=entryFont, bg=white)
    DVDnameEntry.insert(END, dvd_name)
    DVDnameEntry.pack(side=LEFT)

    spaceLabel = Label(frame1_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    runtimeLabel = Label(frame2, text="Runtime:", font=mainFont, bg=mainbg, fg=mainfg, width=23)
    runtimeLabel.pack(side=LEFT)

    runtimeHoursEntry = Entry(frame2, font=entryFont, bg=white, width=5) #want here
    runtimeHoursEntry.insert(END, dvd_details_list[1])
    runtimeHoursEntry.pack(side=LEFT)

    runtimeHLabel = Label(frame2, text="h", font=mainFont, fg=mainfg, bg=mainbg)
    runtimeHLabel.pack(side=LEFT)
    
    runtimeMinutesEntry = Entry(frame2, font=entryFont, bg=white, width=5)
    runtimeMinutesEntry.insert(END, dvd_details_list[2])
    runtimeMinutesEntry.pack(side=LEFT)

    runtimeMLabel = Label(frame2, text="m", font=mainFont, fg=mainfg, bg=mainbg)
    runtimeMLabel.pack(side=LEFT)

    spaceLabel = Label(frame2_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    directorLabel = Label(frame3, text="Director:", font=mainFont, bg=mainbg, fg=mainfg, width=28)
    directorLabel.pack(side=LEFT)

    directorEntry = Entry(frame3, font=entryFont, bg=white)
    directorEntry.insert(END, dvd_details_list[5])
    directorEntry.pack(side=LEFT)

    spaceLabel = Label(frame3_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    locationLabel = Label(frame4, text="Location in house:", font=mainFont, bg=mainbg, fg=mainfg, width=28)
    locationLabel.pack(side=LEFT)

    locationEntry = Entry(frame4, font=entryFont, bg=white)
    locationEntry.insert(END, dvd_details_list[4])
    locationEntry.pack(side=LEFT)

    spaceLabel = Label(frame4_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    yearLabel = Label(frame5, text="Release year:", font=mainFont, bg=mainbg, fg=mainfg, width=15)
    yearLabel.pack(side=LEFT)

    now = datetime.datetime.now()
    year = now.year
    Options = []
    yearDifference = year - 2020
    yearRange = 71 + yearDifference
    year = year + 1
    for i in range(yearRange):
        year = year - 1
        Options.append(year)

    variable = StringVar(frame5)
    #variable.set(Options[0])
    variable.set(dvd_details_list[3])

    dateOption = OptionMenu(frame5, variable, *Options)
    dateOption["highlightthickness"]=0
    dateOption.config(font="Arial 11")
    dateOption["menu"].config(font="Arial 12")
    dateOption.pack(side=LEFT)

    spaceLabel = Label(frame5_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    genreLabel = Label(frame6, text="Genre:", font=mainFont, bg=mainbg, fg=mainfg, width=28)
    genreLabel.pack(side=LEFT)

    genreSpace = Label(frame6, text="", font=mainFont, bg=mainbg, width=10)
    genreSpace.pack(side=LEFT)

    spaceLabel = Label(frameSpace, text = "", font=mainFont, bg=mainbg, width=40)
    spaceLabel.pack()
    
    gen = StringVar(frame7, dvd_details_list[6])
    rb1 = Radiobutton(frame7, text="Action", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Action", variable=gen, command=getgen)
    rb1.pack(anchor=W)
    rb2 = Radiobutton(frame7, text="Adventure", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Adventure", variable=gen, command=getgen)
    rb2.pack(anchor=W)
    rb3 = Radiobutton(frame7, text="Comedy", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Comedy", variable=gen, command=getgen)
    rb3.pack(anchor=W)
    rb4 = Radiobutton(frame7, text="Comedy drama", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Comedy drama", variable=gen, command=getgen)
    rb4.pack(anchor=W)
    rb5 = Radiobutton(frame7, text="Crime", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Crime", variable=gen, command=getgen)
    rb5.pack(anchor=W)
    rb6 = Radiobutton(frame7, text="Documentary", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Documentary", variable=gen, command=getgen)
    rb6.pack(anchor=W)
    rb7 = Radiobutton(frame7, text="Drama", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Drama", variable=gen, command=getgen)
    rb7.pack(anchor=W)
    rb8 = Radiobutton(frame7, text="Epic", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Epic", variable=gen, command=getgen)
    rb8.pack(anchor=W)
    rb9 = Radiobutton(frame7, text="Fantasy", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Fantasy", variable=gen, command=getgen)
    rb9.pack(anchor=W)
    rb10 = Radiobutton(frame7, text="Historical", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Historical", variable=gen, command=getgen)
    rb10.pack(anchor=W)

    rb11 = Radiobutton(frame8, text="Horror", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Horror", variable=gen, command=getgen)
    rb11.pack(anchor=W)
    rb12 = Radiobutton(frame8, text="Musical", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Musical", variable=gen, command=getgen)
    rb12.pack(anchor=W)
    rb13 = Radiobutton(frame8, text="Mystery", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Mystery", variable=gen, command=getgen)
    rb13.pack(anchor=W)
    rb14 = Radiobutton(frame8, text="Romance", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Romance", variable=gen, command=getgen)
    rb14.pack(anchor=W)
    rb15 = Radiobutton(frame8, text="Romantic comedy", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Romantic comedy", variable=gen, command=getgen)
    rb15.pack(anchor=W)
    rb16 = Radiobutton(frame8, text="Sci-Fi", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Sci-Fi", variable=gen, command=getgen)
    rb16.pack(anchor=W)
    rb17 = Radiobutton(frame8, text="Spy film", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Spy film", variable=gen, command=getgen)
    rb17.pack(anchor=W)
    rb18 = Radiobutton(frame8, text="Thriller", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Thriller", variable=gen, command=getgen)
    rb18.pack(anchor=W)
    rb19 = Radiobutton(frame8, text="War", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="War", variable=gen, command=getgen)
    rb19.pack(anchor=W)
    rb20 = Radiobutton(frame8, text="Western", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Western", variable=gen, command=getgen)
    rb20.pack(anchor=W)

    frame0.pack(side=RIGHT)
    frame00.pack()
    frame1.pack()
    frame1_5.pack()
    frame2.pack()
    frame2_5.pack()
    frame3.pack()
    frame3_5.pack()
    frame4.pack()
    frame4_5.pack()
    frame5.pack()
    frame5_5.pack()
    frame6.pack()
    frameSpace.pack(side=LEFT)
    frame7.pack(side=LEFT)
    frame8.pack(side=LEFT)
    
    editScreen.mainloop()

    
    

def OK(Screen):
    Screen.destroy()

DVDs_found = [] #has to be declared outside the function so that it can be passed over when it is called from main menu

def searchDVD(mainMenu, text_to_search, DVDs_found):
    try:
        mainMenu.withdraw()
    except:
        print("Main menu was already withdrawn (failed to withdraw, continuing onwards)")

    searchScreenTitle = "Search DVDs"

    searchScreen = Toplevel()
    searchScreen.geometry(screenSize)
    searchScreen.title(searchScreenTitle)
    searchScreen["bg"] = mainbg

    def view_DVD_details(dvd_name):

        dvdDetails = Toplevel()
        dvdDetails.geometry(screenSize) 
        dvdDetails.title("Details")
        dvdDetails["bg"] = mainbg

        def close_window(dvdDetails):
            dvdDetails.destroy()

        c.execute('''SELECT dvds.dvd_ID, dvds.runtimeHours, dvds.runtimeMins, dvds.date, dvds.location, directors.director_name, genres.genre_name
                        FROM dvds, directors, genres, dirate
                        WHERE dvds.dvd_ID = dirate.dvd_ID
                        AND dirate.director_ID = directors.director_ID
                        AND dirate.genre_ID = genres.genre_ID
                        AND dvds.dvd_name = ?''', (dvd_name,))
        for row in c.fetchall():
            print(row)
        dvd_details_list = list(row)

        dvd_runtime_text = str(dvd_details_list[1]) + "h" + str(dvd_details_list[2]) + "m"

        frame0 = Frame(dvdDetails, bg=mainbg) #spacing
        frame0_5 = Frame(dvdDetails, bg=mainbg) #spacing again
        frame1 = Frame(dvdDetails, bg=mainbg)
        frame1_5 = Frame(dvdDetails, bg=mainbg) #spacing between 1 and 2
        frame2 = Frame(dvdDetails, bg=mainbg)
        frame3 = Frame(dvdDetails, bg=mainbg)

        spaceLab = Label(frame0_5, text="", bg=mainbg, font=mainFont, width=10)
        spaceLab.pack()

        spaceLab = Label(frame0, text="", bg=mainbg, font=mainFont, width=10)
        spaceLab.pack()

        nameLabel = Label(frame1, text="Title:", font=mainFont, bg=mainbg, fg=mainfg)
        nameLabel.pack(anchor=E)
        lab1 = Label(frame2, text=dvd_name, font=mainFont, bg=mainbg, fg=mainfg) #dvd name
        lab1.pack(anchor=W)
        runtimeLabel = Label(frame1, text="Runtime:", font=mainFont, bg=mainbg, fg=mainfg)
        runtimeLabel.pack(anchor=E)
        lab2 = Label(frame2, text=dvd_runtime_text, font=mainFont, bg=mainbg, fg=mainfg) #dvd runtime
        lab2.pack(anchor=W)
        yearLabel = Label(frame1, text="Release year:", font=mainFont, bg=mainbg, fg=mainfg)
        yearLabel.pack(anchor=E)
        lab3 = Label(frame2, text=dvd_details_list[3], font=mainFont, bg=mainbg, fg=mainfg) #release year
        lab3.pack(anchor=W)
        locationLabel = Label(frame1, text="Location:", font=mainFont, bg=mainbg, fg=mainfg)
        locationLabel.pack(anchor=E)
        lab4 = Label(frame2, text=dvd_details_list[4], font=mainFont, bg=mainbg, fg=mainfg) #location in house
        lab4.pack(anchor=W)
        directorLabel = Label(frame1, text="Director:", font=mainFont, bg=mainbg, fg=mainfg)
        directorLabel.pack(anchor=E)
        lab5 = Label(frame2, text=dvd_details_list[5], font=mainFont, bg=mainbg, fg=mainfg) #director
        lab5.pack(anchor=W)
        genreLabel = Label(frame1, text="Genre:", font=mainFont, bg=mainbg, fg=mainfg)
        genreLabel.pack(anchor=E)
        lab6 = Label(frame2, text=dvd_details_list[6], font=mainFont, bg=mainbg, fg=mainfg) #genre
        lab6.pack(anchor=W)

        spaceLabBetween = Label(frame1_5, text="", bg=mainbg, font=mainFont, width=5)
        spaceLabBetween.pack()

        edit_btn = Button(frame3, text="Edit", command=lambda: editDVD(mainMenu, searchScreen, dvdDetails, dvd_name, dvd_details_list), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=10)
        edit_btn.pack()
        back_btn = Button(frame3, text="Back", command=lambda: close_window(dvdDetails), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=10)
        back_btn.pack()

        frame0.pack(side=LEFT)
        frame1.pack(side=LEFT)
        frame1_5.pack(side=LEFT)
        frame2.pack(side=LEFT)
        frame0_5.pack(side=RIGHT)
        frame3.pack(side=RIGHT)


        dvdDetails.mainloop()
        

    def search_DVDs(searchScreen, mainMenu):
        text_to_search = search_entry.get()
        search_entry.delete(0, END)

        DVDs_found = []
        c.execute("SELECT dvd_name FROM dvds WHERE dvd_name LIKE '%'||?||'%'", (text_to_search,))
        for row in c.fetchall():
            DVDs_found.append(row[0])
        print(DVDs_found)
        searchScreen.destroy()
        searchDVD(mainMenu, text_to_search, DVDs_found)
        

    frame1 = Frame(searchScreen, bg=mainbg)
    frame2 = Frame(searchScreen, bg=mainbg)

    search_entry = Entry(frame1, font=entryFont, bg=white, width=25)
    search_entry.bind("<Return>", (lambda event: search_DVDs(searchScreen, mainMenu)))
    search_entry.pack(side=LEFT)

    lab_SPACE = Label(frame1, text="", bg=mainbg, width=1)
    lab_SPACE.pack(side=LEFT)
    
    search_DVDs_btn = Button(frame1, text="Search", command=lambda: search_DVDs(searchScreen, mainMenu), font=small_btn_font, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=sm_btn_width, height=sm_btn_height)
    search_DVDs_btn.pack(side=LEFT)

    lab_SPACE = Label(frame1, text="", bg=mainbg, width=4)
    lab_SPACE.pack(side=LEFT)

    menu_btn = Button(frame1, text="Back to\n main menu", command=lambda: back_to_menu(searchScreen, mainMenu), font=small_btn_font, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=sm_btn_width, height=sm_btn_height)
    menu_btn.pack(side=LEFT)

    if len(DVDs_found) > 0:
        for i in DVDs_found:
            def cmd(x=i):
                view_DVD_details(x)
            btn = Button(frame2, command=cmd, text=i, font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg)
            btn.pack()
    else:
        pass

    frame1.pack(side=TOP)
    frame2.pack()

    searchScreen.mainloop()

def back_to_menu(Screen, mainMenu):
    Screen.destroy()
    mainMenu.deiconify()

def confirmCD(Screen, mainMenu):
    Screen.destroy()
    mainMenu.deiconify()

def confirmDVDFailure():
    failedToInput = Toplevel()
    failedToInput.geometry(smallScreenSize)
    failedToInput.title("Operation failed")
    failedToInput["bg"] = mainbg

    labSPACE = Label(failedToInput, text="", bg=mainbg)
    labSPACE.pack()
    lab_Error_message = Label(failedToInput, text="Please make sure\nevery field is filled in", bg=mainbg, fg=mainfg, font=mainFont)
    lab_Error_message.pack()
    labSPACE = Label(failedToInput, text="", bg=mainbg)
    labSPACE.pack()
    Error_btn = Button(failedToInput, text="OK", command=lambda: OK(failedToInput), bg=mainbg, fg=mainfg, font=mainFont, activebackground=activebtnbg, activeforeground=mainfg)
    Error_btn.pack()

    failedToInput.mainloop()

def confirmDVD(DVDnameEntry, runtimeHoursEntry, runtimeMinutesEntry, directorEntry, locationEntry, getgen, getdate):

    date = getdate()
    genre = getgen()

    checkList = []
    #adding data to database
    DVD_name = DVDnameEntry.get()
    checkList.append(DVD_name)
    DVDnameEntry.delete(0, END)
    DVD_hours = runtimeHoursEntry.get()
    checkList.append(DVD_hours)
    runtimeHoursEntry.delete(0, END)
    DVD_minutes = runtimeMinutesEntry.get()
    checkList.append(DVD_minutes)
    runtimeMinutesEntry.delete(0, END)
    DVD_director = directorEntry.get()
    checkList.append(DVD_director)
    directorEntry.delete(0, END)
    DVD_location = locationEntry.get()
    checkList.append(DVD_location)
    locationEntry.delete(0, END)

    if checkList[1] == "": #if hours or minutes is left blank, put a 0 there
        DVD_hours = 0
    if checkList[2] == "":
        DVD_minutes = 0
    if checkList[0] == "" or checkList[3] == "" or checkList[4] == "": #if any of these are left empty, data cannot be inputted into database
        confirmDVDFailure()
    else:
        c.execute('''INSERT INTO dvds(dvd_name, runtimeHours, runtimeMins, date, location) VALUES(?, ?, ?, ?, ?)''',
                  (DVD_name, DVD_hours, DVD_minutes, date, DVD_location,))
        conn.commit()

        if c.execute('''SELECT EXISTS(SELECT 1 FROM directors WHERE director_name = ?)''', (DVD_director,)).fetchone() == (1,):
            print("Found!")
        else:
            c.execute('''INSERT INTO directors(director_name) VALUES(?)''',
                      (DVD_director,))
            conn.commit()

        #Now put in code where director is either entered or not, because the code below needs a director ID or it throws up errors

        dirate_list = [] #get primary keys so they can be put in the compound key table
        c.execute('''SELECT director_ID FROM directors WHERE director_name = ?''',(DVD_director,))
        for row in c.fetchall():
            dirate_list.append(row[0])
        director_ID_value = dirate_list[0]

        c.execute("SELECT dvd_ID FROM dvds WHERE dvd_name = ?",(DVD_name,))
        for row in c.fetchall():
            dirate_list.append(row[0])
        dvd_ID_value = dirate_list[1]
        c.execute("SELECT genre_ID FROM genres WHERE genre_name = ?",(genre,))
        for row in c.fetchall():
            dirate_list.append(row[0])
        genre_ID_value = dirate_list[2]

        c.execute('''INSERT INTO dirate(dvd_ID, director_ID, genre_ID) VALUES(?, ?, ?)''',
                  (dvd_ID_value, director_ID_value, genre_ID_value,))
        conn.commit()

def addDVD(mainMenu):

    mainMenu.withdraw()

    addScreenTitle = "Add a DVD"
    spacelabelheight = 2

    def getgen():
        genre = gen.get()
        return genre

    def getdate():
        date = variable.get()
        return date

    addScreen = Tk()
    addScreen.title(addScreenTitle)
    addScreen.geometry(screenSize)
    addScreen["bg"] = mainbg

    frame00 = Frame(addScreen, bg=mainbg) #title space
    frame0 = Frame(addScreen, bg=mainbg) #confirm/back button
    frame1 = Frame(addScreen, bg=mainbg) #dvd name
    frame1_5 = Frame(addScreen, bg=mainbg) #s p a c e
    frame2 = Frame(addScreen, bg=mainbg) #runtime
    frame2_5 = Frame(addScreen, bg=mainbg) #s p a c e
    frame3 = Frame(addScreen, bg=mainbg) #director
    frame3_5 = Frame(addScreen, bg=mainbg) #s p a c e
    frame4 = Frame(addScreen, bg=mainbg) #location
    frame4_5 = Frame(addScreen, bg=mainbg) #s p a c e
    frame5 = Frame(addScreen, bg=mainbg) #release year
    frame5_5 = Frame(addScreen, bg=mainbg) #s p a c e
    frame6 = Frame(addScreen, bg=mainbg) #genre
    frameSpace = Frame(addScreen, bg=mainbg) #give space
    frame7 = Frame(addScreen, bg=mainbg) #genre radiobuttons
    frame8 = Frame(addScreen, bg=mainbg) #genre radiobuttons 2

    titleLabel = Label(frame00, text="", font=mainFont, bg=mainbg, fg=mainfg)
    titleLabel.pack()

    menu_btn = Button(frame0, text="Back to\n main menu", command=lambda: back_to_menu(addScreen, mainMenu), font=small_btn_font, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg,width=sm_btn_width, height=sm_btn_height)
    menu_btn.pack()

    confirm_btn = Button(frame0, text="Confirm", command=lambda: confirmDVD(DVDnameEntry, runtimeHoursEntry, runtimeMinutesEntry, directorEntry, locationEntry, getgen, getdate), font=small_btn_font, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg,width=sm_btn_width, height=sm_btn_height)
    confirm_btn.pack()
    
    DVDnameLabel = Label(frame1, text="DVD Title:", font=mainFont, bg=mainbg, fg=mainfg, width=28)
    DVDnameLabel.pack(side=LEFT)

    DVDnameEntry = Entry(frame1, font=entryFont, bg=white)
    DVDnameEntry.pack(side=LEFT)

    spaceLabel = Label(frame1_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    runtimeLabel = Label(frame2, text="Runtime:", font=mainFont, bg=mainbg, fg=mainfg, width=23)
    runtimeLabel.pack(side=LEFT)

    runtimeHoursEntry = Entry(frame2, font=entryFont, bg=white, width=5) #want here
    runtimeHoursEntry.pack(side=LEFT)

    runtimeHLabel = Label(frame2, text="h", font=mainFont, fg=mainfg, bg=mainbg)
    runtimeHLabel.pack(side=LEFT)
    
    runtimeMinutesEntry = Entry(frame2, font=entryFont, bg=white, width=5)
    runtimeMinutesEntry.pack(side=LEFT)

    runtimeMLabel = Label(frame2, text="m", font=mainFont, fg=mainfg, bg=mainbg)
    runtimeMLabel.pack(side=LEFT)

    spaceLabel = Label(frame2_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    directorLabel = Label(frame3, text="Director:", font=mainFont, bg=mainbg, fg=mainfg, width=28)
    directorLabel.pack(side=LEFT)

    directorEntry = Entry(frame3, font=entryFont, bg=white)
    directorEntry.pack(side=LEFT)

    spaceLabel = Label(frame3_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    locationLabel = Label(frame4, text="Location in house:", font=mainFont, bg=mainbg, fg=mainfg, width=28)
    locationLabel.pack(side=LEFT)

    locationEntry = Entry(frame4, font=entryFont, bg=white)
    locationEntry.pack(side=LEFT)

    spaceLabel = Label(frame4_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    yearLabel = Label(frame5, text="Release year:", font=mainFont, bg=mainbg, fg=mainfg, width=15)
    yearLabel.pack(side=LEFT)

    now = datetime.datetime.now()
    year = now.year
    Options = []
    yearDifference = year - 2020
    yearRange = 71 + yearDifference
    year = year + 1
    for i in range(yearRange):
        year = year - 1
        Options.append(year)

    variable = StringVar(frame5)
    variable.set(Options[0])

    dateOption = OptionMenu(frame5, variable, *Options)
    dateOption["highlightthickness"]=0
    dateOption.config(font="Arial 11")
    dateOption["menu"].config(font="Arial 12")
    dateOption.pack(side=LEFT)

    spaceLabel = Label(frame5_5, text="", bg=mainbg, fg=mainfg)
    spaceLabel.pack()

    genreLabel = Label(frame6, text="Genre:", font=mainFont, bg=mainbg, fg=mainfg, width=28)
    genreLabel.pack(side=LEFT)

    genreSpace = Label(frame6, text="", font=mainFont, bg=mainbg, width=10)
    genreSpace.pack(side=LEFT)

    spaceLabel = Label(frameSpace, text = "", font=mainFont, bg=mainbg, width=40)
    spaceLabel.pack()
    
    gen = StringVar(frame7, "Action")
    rb1 = Radiobutton(frame7, text="Action", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Action", variable=gen, command=getgen)
    rb1.pack(anchor=W)
    rb2 = Radiobutton(frame7, text="Adventure", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Adventure", variable=gen, command=getgen)
    rb2.pack(anchor=W)
    rb3 = Radiobutton(frame7, text="Comedy", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Comedy", variable=gen, command=getgen)
    rb3.pack(anchor=W)
    rb4 = Radiobutton(frame7, text="Comedy drama", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Comedy drama", variable=gen, command=getgen)
    rb4.pack(anchor=W)
    rb5 = Radiobutton(frame7, text="Crime", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Crime", variable=gen, command=getgen)
    rb5.pack(anchor=W)
    rb6 = Radiobutton(frame7, text="Documentary", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Documentary", variable=gen, command=getgen)
    rb6.pack(anchor=W)
    rb7 = Radiobutton(frame7, text="Drama", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Drama", variable=gen, command=getgen)
    rb7.pack(anchor=W)
    rb8 = Radiobutton(frame7, text="Epic", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Epic", variable=gen, command=getgen)
    rb8.pack(anchor=W)
    rb9 = Radiobutton(frame7, text="Fantasy", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Fantasy", variable=gen, command=getgen)
    rb9.pack(anchor=W)
    rb10 = Radiobutton(frame7, text="Historical", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Historical", variable=gen, command=getgen)
    rb10.pack(anchor=W)

    rb11 = Radiobutton(frame8, text="Horror", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Horror", variable=gen, command=getgen)
    rb11.pack(anchor=W)
    rb12 = Radiobutton(frame8, text="Musical", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Musical", variable=gen, command=getgen)
    rb12.pack(anchor=W)
    rb13 = Radiobutton(frame8, text="Mystery", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Mystery", variable=gen, command=getgen)
    rb13.pack(anchor=W)
    rb14 = Radiobutton(frame8, text="Romance", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Romance", variable=gen, command=getgen)
    rb14.pack(anchor=W)
    rb15 = Radiobutton(frame8, text="Romantic comedy", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Romantic comedy", variable=gen, command=getgen)
    rb15.pack(anchor=W)
    rb16 = Radiobutton(frame8, text="Sci-Fi", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Sci-Fi", variable=gen, command=getgen)
    rb16.pack(anchor=W)
    rb17 = Radiobutton(frame8, text="Spy film", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Spy film", variable=gen, command=getgen)
    rb17.pack(anchor=W)
    rb18 = Radiobutton(frame8, text="Thriller", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Thriller", variable=gen, command=getgen)
    rb18.pack(anchor=W)
    rb19 = Radiobutton(frame8, text="War", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="War", variable=gen, command=getgen)
    rb19.pack(anchor=W)
    rb20 = Radiobutton(frame8, text="Western", font=rbFont, selectcolor=mainbg, bg=mainbg, fg=mainfg, activebackground=mainbg, value="Western", variable=gen, command=getgen)
    rb20.pack(anchor=W)

    frame0.pack(side=RIGHT)
    frame00.pack()
    frame1.pack()
    frame1_5.pack()
    frame2.pack()
    frame2_5.pack()
    frame3.pack()
    frame3_5.pack()
    frame4.pack()
    frame4_5.pack()
    frame5.pack()
    frame5_5.pack()
    frame6.pack()
    frameSpace.pack(side=LEFT)
    frame7.pack(side=LEFT)
    frame8.pack(side=LEFT)
    
    addScreen.mainloop()

def main_menu():

    mmHeight = 2 #HEGIHT AND WIDTH OF BUTTONS FOR MAIN MENU!!!
    mmWidth = 20

    mainMenu = Tk()
    mainMenu.title(mainMenuTitle)
    mainMenu.geometry(screenSize)
    mainMenu["bg"] = mainbg

    frame1 = Frame(mainMenu, bg=mainbg)
    frame2 = Frame(mainMenu, bg=mainbg)

    logo = PhotoImage(file="ScreenlogoG.png")
    lab_logo= Label(image=logo, bg=mainbg)
    lab_logo.pack()

    lab0 = Label(frame1, text="", bg=mainbg)
    lab0.pack()

    search_btn = Button(frame1, text="Search DVDs", command=lambda: searchDVD(mainMenu, "", DVDs_found), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=mmWidth, height=mmHeight)
    search_btn.pack()

    lab0 = Label(frame1, text="", bg=mainbg)
    lab0.pack()

    add_btn = Button(frame1, text="Add a DVD", command=lambda: addDVD(mainMenu), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=mmWidth, height=mmHeight)
    add_btn.pack()

    lab0 = Label(frame1, text="", bg=mainbg)
    lab0.pack()

    #CD fucntion of the application is a WIP
    search_CD_btn = Button(frame1, text="Search CDs", command=lambda: searchCD(mainMenu), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=mmWidth, height=mmHeight)
    search_CD_btn.pack()

    lab0 = Label(frame1, text="", bg=mainbg)
    lab0.pack()

    add_CDs = Button(frame1, text="Add a CD", command=lambda: addCD(mainMenu), font=mainFont, bg=btnbg, fg=mainfg, activebackground=activebtnbg, activeforeground=mainfg, width=mmWidth, height=mmHeight)
    add_CDs.pack()

    quit_btn = Button(frame2, text="Quit", command=lambda: mainMenu.destroy(), font=mainFont, bg=red, fg=mainfg, activebackground=dark_red, activeforeground=mainfg, width=5)
    quit_btn.pack()

    frame1.pack()
    frame2.pack(side=RIGHT)

    mainMenu.mainloop()

main_menu()

c.close()
conn.close()
