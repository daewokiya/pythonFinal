from tkinter import *
import tkinter.scrolledtext as st
import numbers
import tkinter as tk
from csv import *
import csv
import os

class GUI:
    def __init__(self, window):
        self.window = window
        global count
        count=0
        #Entry for Car Make and Model

        self.frame_title = Frame(self.window)
        self.label_title = Label(self.frame_title, text='Hot Wheels Tracker', font=('Helvetica bold', 18), justify='center')
        self.label_title.pack(padx=5, side='top')
        self.frame_title.pack(anchor='n', pady=15)

        self.message = Label(self.frame_title, text='', font=('Helvetica bold', 12), justify='center')
        self.message.pack(anchor='n', pady=0)

        self.frame_make = Frame(self.window)
        self.label_make = Label(self.frame_make, text='Make', font=('Helvetica bold', 12))
        self.entry_make = Entry(self.frame_make, font=('Helvetica bold', 12))
        self.label_make.pack(padx=15, side='left')
        self.entry_make.pack(padx=19, side='left')
        self.frame_make.pack(anchor='w', pady=10)

        self.frame_model = Frame(self.window)
        self.label_model = Label(self.frame_model, text='Model', font=('Helvetica bold', 12))
        self.entry_model = Entry(self.frame_model, font=('Helvetica bold', 12))
        self.label_model.pack(padx=15, side='left')
        self.entry_model.pack(padx=15, side='left')
        self.frame_model.pack(anchor='w', pady=10)

        #Choose Car Type

        car_type = [
            "Convertible",
            "Coupe",
            "Hatchback",
            "Minivan",
            "Pickup/Truck",
            "Sedan",
            "SUV",
            "Wagon",
            "Motorcycle",
            "Other"
        ]

        self.frame_type = Frame(self.window)
        self.label_type = Label(self.frame_type, text='Car Type', font=('Helvetica bold', 12))
        self.label_type.pack(padx=15, side='left')
        self.frame_type.pack(anchor='w', pady=5)

        global carType_menu
        carType_menu = StringVar()
        carType_menu.set("[Select Car Type]")
        self.carDrop = OptionMenu(self.frame_type, carType_menu, *car_type, command=self.getTypeOption)
        self.carDrop.pack(anchor='w', pady=5)

        #Choose Car Color
        color_options = [
            "Red",
            "Orange",
            "Yellow",
            "Green",
            "Blue",
            "Purple",
            "Black",
            "White",
            "Other"
        ]

        self.frame_color = Frame(self.window)
        self.label_color = Label(self.frame_color, text='Color', font=('Helvetica bold', 12))
        self.label_color.pack(padx=15, side='left')
        self.frame_color.pack(anchor='w', pady=5)

        global color_menu
        color_menu = StringVar()
        color_menu.set("[Select Color]")
        self.colorDrop = OptionMenu(self.frame_color, color_menu, *color_options, command=self.getColorOption)
        self.colorDrop.pack(anchor='w', padx=26, pady=5)

        #Enter a Year

        self.frame_year = Frame(self.window)
        self.label_year = Label(self.frame_year, text='Car Model Year', font=('Helvetica bold', 12))
        self.entry_year = Entry(self.frame_year, font=('Helvetica bold', 12), width=10)
        self.label_year.pack(padx=15, side='left')
        self.entry_year.pack(padx=36, side='left')
        self.frame_year.pack(anchor='w', pady=10)

        #Manufactured Year (The year the toy was made)
        
        self.frame_year2 = Frame(self.window)
        self.label_year2 = Label(self.frame_year2, text='Manufactured Year', font=('Helvetica bold', 12))
        self.entry_year2 = Entry(self.frame_year2, font=('Helvetica bold', 12), width=10)
        self.label_year2.pack(padx=15, side='left')
        self.entry_year2.pack(padx=15, side='left')
        self.frame_year2.pack(anchor='w', pady=10)

        #View Entries Before Inserting into CSV File

        self.frame_entries = Frame(self.window)
        self.label_entries = Label(self.frame_entries, text='Entries', font=('Helvetica bold', 12))
        self.carEntries = st.ScrolledText(self.frame_entries, wrap = tk.WORD, width=45, height=10, font=("Helvetica bold", 8))
        self.label_entries.pack(padx=15, side='top')
        self.frame_entries.pack(anchor='n', pady=5)
        self.carEntries.pack(anchor='n', pady=10)

        self.carEntries.configure(state='disabled')

        #Add to List Button and Add to CSV File Button

        self.frame_buttons = Frame(self.window)
        self.frame_buttons.pack(anchor='c', side='top', pady=10)
        
        clearButton = Button(self.frame_buttons, text='CLEAR', height=1, width=6, command=self.clear)
        clearButton.pack(anchor='w', side='left', padx=15)
        
        addButton = Button(self.frame_buttons, text='ADD', height=1, width=6, command=self.added)
        addButton.pack(anchor='w', side='left', padx=15)

        deleteButton = Button(self.frame_buttons, text='DELETE', height=1, width=6, command=self.delete)
        deleteButton.pack(anchor='w', side='left', padx=15)
        
        saveButton = Button(self.frame_buttons, text='SAVE', height=1, width=6, command=self.save)
        saveButton.pack(anchor='w', side='left', padx=15)

    def clear(self):
        self.entry_make.delete(0, END)
        self.entry_model.delete(0, END)
        carType_menu.set("[Select Car Type]")
        color_menu.set("[Select Color]")
        self.entry_year.delete(0, END)
        self.entry_year2.delete(0, END)

    def added(self):
        getMake = self.entry_make.get()
        getModel = self.entry_model.get()
        getType = carType_menu.get()
        getColor = color_menu.get()
        getYear = self.entry_year.get()
        getYear2 = self.entry_year2.get()
        if getYear != None:
            try:
                getYear = int(self.entry_year.get())
            except ValueError:
                self.message.config(text="Please Enter a Number for the Year")
        if getYear2 != None:
            try:
                getYear2 = int(self.entry_year2.get())
            except ValueError:
                self.message.config(text="Please Enter a Number for the Manufactured Year")

        if len(getMake) != 0:
            if len(getModel) != 0:
                if getType != "[Select Car Type]":
                    if getColor != "[Select Color]":
                        if isinstance(getYear, int) == True:
                            if isinstance(getYear2, int) == True:
                                self.carEntries.configure(state='normal')
                                temptext = getMake + ", " + getModel + ", " + getType + ", " + getColor + ", " + str(getYear) + ", " + str(getYear2)
                                self.carEntries.insert(END, temptext + '\n')
                                self.carEntries.configure(state='disabled')
                                
                                self.entry_make.delete(0, END)
                                self.entry_model.delete(0, END)
                                carType_menu.set("[Select Car Type]")
                                color_menu.set("[Select Color]")
                                self.entry_year.delete(0, END)
                                self.entry_year2.delete(0, END)

                                self.message.config(text='')
                                global count
                                count=count+1
                            else:
                                self.message.config(text="Please Enter the Manufactured Year")
                        else:
                            self.message.config(text="Please Enter a Year")                          
                    else:
                        self.message.config(text="Please Select a Car Color")
                else:
                    self.message.config(text="Please Select a Car Type")
            else:
                self.message.config(text="Please Enter a Model")
        else:
            self.message.config(text="Please Enter a Maker")

    def delete(self):
        self.carEntries.configure(state='normal')
        global count
        if count != 0:
            self.carEntries.delete(float(count), END)
            count-=1
        self.carEntries.configure(state='disabled')


    def save(self):
        global count
        if os.stat('HotWheels.csv').st_size == 0:
            valueFields = ['Make','Model','Type','Color','Year','Manufactured Year']
            with open('HotWheels.csv', 'w') as file:
                writeFile = writer(file, lineterminator='\n')
                writeFile.writerow(valueFields)
            file.close()
            if count != 0:
                while True:
                    tempCar = self.carEntries.get(1.0, 2.0)
                    tempCar = tempCar.split('\n')
                    tempCar = tempCar[0]
                    tempList = tempCar.split(', ')
                    with open('HotWheels.csv', 'a') as file:
                        writeFile = writer(file, lineterminator='\n')
                        writeFile.writerow(tempList)
                    self.carEntries.configure(state='normal')
                    self.carEntries.delete(1.0, 2.0)
                    self.carEntries.configure(state='disabled')
                    count-=1
                    if count == 0:
                        file.close()
                        self.carEntries.configure(state='normal')
                        self.carEntries.delete(0.0, END)
                        self.carEntries.configure(state='disabled')
                        break
        else:
            if count != 0:
                while True:
                    tempCar = self.carEntries.get(1.0, 2.0)
                    tempCar = tempCar.split('\n')
                    tempCar = tempCar[0]
                    tempList = tempCar.split(', ')
                    with open('HotWheels.csv', 'a') as file:
                        writeFile = writer(file, lineterminator='\n')
                        writeFile.writerow(tempList)
                    self.carEntries.configure(state='normal')
                    self.carEntries.delete(1.0, 2.0)
                    self.carEntries.configure(state='disabled')
                    count-=1
                    if count == 0:
                        file.close()
                        self.carEntries.configure(state='normal')
                        self.carEntries.delete(0.0, END)
                        self.carEntries.configure(state='disabled')
                        break
            elif count == 0:
                self.message.config(text="There is Nothing to Save")
        
    
    def getTypeOption(self, carType):
        carType = carType_menu.get()
        
    def getColorOption(self, carColor):
        carColor = color_menu.get()
        





