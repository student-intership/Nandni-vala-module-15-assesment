from tkinter import *
from tkinter import Tk, Text, END
from tkinter import messagebox 
import os
import smtplib
import pymysql


# Database connection
mydb = pymysql.connect(host="localhost", user="root", password="", database="Billing")
mycursor = mydb.cursor()

def Exit():
    root.destroy()

def insert_data1():
    try:
        # Ensure database connection and cursor are initialized
        if mydb is None or mycursor is None:
            raise pymysql.Error("Database connection is not initialized")

        # Validate input fields
        if not nameEntry.get() or not Phone_NumberEntry.get() or not Bill_NoEntry.get():
            messagebox.showerror('Error', 'Please fill all required fields!')
            return

        bill_no = Bill_NoEntry.get()
        name = nameEntry.get()
        phone_no = Phone_NumberEntry.get()
        email = Email_idEntry.get()  # Assuming you have an email entry field

        if len(phone_no) > 10:
            messagebox.showerror('Error', 'Phone Number must be at most 10 digits!')
            return

        # Check if the email already exists
        email_check_query = "SELECT * FROM person WHERE email = %s"
        mycursor.execute(email_check_query, (email,))
        if mycursor.fetchone():
            messagebox.showerror('Error', 'Email already exists! Please use a different email.')
            return

        # Check if bill number already exists
        bill_check_query = "SELECT * FROM person WHERE bill_no = %s"
        mycursor.execute(bill_check_query, (bill_no,))
        if mycursor.fetchone():
            messagebox.showerror('Error', 'Bill Number already exists!')
            return

        # Insert data into the database
        query = "INSERT INTO person (name, phone_no, bill_no, email) VALUES (%s, %s, %s, %s)"
        args = (name, phone_no, bill_no, email)

        mycursor.execute(query, args)
        mydb.commit()
        
        print("Data Inserted!!")
        messagebox.showinfo('Success', 'Customer data saved successfully!')

    except pymysql.IntegrityError as e:
        if "1062" in str(e):
            messagebox.showerror('Error', 'Duplicate entry detected! Email or Bill No must be unique.')
        else:
            messagebox.showerror('Error', f'Integrity Error: e')
        mydb.rollback()

    except pymysql.OperationalError as e:
        messagebox.showerror('Error', f'Operational Error: ',e)
        mydb.rollback()

    except pymysql.ProgrammingError as e:
        messagebox.showerror('Error', f'Programming Error: e',e)
        mydb.rollback()

    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database Error: e',e)
        mydb.rollback()

    except Exception as e:
        messagebox.showerror('Error', f'Unexpected Error: e',e)

def clear():
    bathsoapEntry.delete(0,END)
    FaceCreamEntry.delete(0,END)
    FaceWashEntry.delete(0,END)
    HairSprayEntry.delete(0,END)
    BodyLotionsEntry.delete(0,END)

    RiceEntry.delete(0,END)
    Food_oilEntry.delete(0,END)
    DaalEntry.delete(0,END)
    WheatEntry.delete(0,END)
    SugarEntry.delete(0,END)

    MazaEntry.delete(0,END)
    CokeEntry.delete(0,END)
    FrootiEntry.delete(0,END)
    NimkosEntry.delete(0,END)
    BiscuitEntry.delete(0,END)

    bathsoapEntry.insert(0,0)
    FaceCreamEntry.insert(0,0)
    FaceWashEntry.insert(0,0)
    HairSprayEntry.insert(0,0)
    BodyLotionsEntry.insert(0,0)

    RiceEntry.insert(0,0)
    Food_oilEntry.insert(0,0)
    DaalEntry.insert(0,0)
    WheatEntry.insert(0,0)
    SugarEntry.insert(0,0)

    MazaEntry.insert(0,0)
    CokeEntry.insert(0,0)
    FrootiEntry.insert(0,0)
    NimkosEntry.insert(0,0)
    BiscuitEntry.insert(0,0)

    cosmeticstaxEntry.delete(0,END)
    grocerytaxEntry.delete(0,END)
    otherstaxEntry.delete(0,END)

    cosmaticspriceEntry.delete(0,END)
    grocerypriceEntry.delete(0,END)
    otherspriceEntry.delete(0,END)

    nameEntry.delete(0,END)
    Phone_NumberEntry.delete(0,END)
    Bill_NoEntry.delete(0,END)

    textarea.delete(1.0,END)

def send_email():
    def exit():
        root1.destroy()

    def verify_email():
        email = emailEntry.get()

        if not email:
            messagebox.showerror('Error', 'Please enter an email!')
            return

        # Fetch user data
        mycursor.execute("SELECT email FROM person WHERE email = %s", (email,))
        user = mycursor.fetchone()

        if user:
            messagebox.showinfo('Success', 'Email exists!')
        else:
            messagebox.showerror('Error', 'Email not found!')


        
    if textarea.get(1.0, END) == '\n':
        messagebox.showerror('Error', 'Bill Is Empty!!')
    else:
        root1 = Toplevel()
        root1.title('Send Gmail')
        root1.config(bg='gray20')
        root1.resizable(0,0)

        sendframe = LabelFrame(root1, text='SENDER', font=('arial',16,'bold'), bd=6, bg='gray20', fg='white')
        sendframe.grid(row=0, column=0, padx=40, pady=20)

        senderlabel = Label(sendframe, text='Sender Email', font=('arial',14,'bold'), bg='gray20', fg='white')
        senderlabel.grid(row=0, column=0, padx=10, pady=8)

        global emailEntry
        emailEntry = Entry(sendframe, font=("arial",14,'bold'), bd=2, width=23, relief=RIDGE)
        emailEntry.grid(row=0, column=1, padx=10, pady=8)

        global email_textarea
        email_textarea = Text(sendframe, font=('arial',14,'bold'), bd=2, relief=SUNKEN, width=42, height=11)
        email_textarea.grid(row=2, column=0, columnspan=2, padx=10, pady=8)
        email_textarea.delete(1.0, END)
        email_textarea.insert(END, textarea.get(1.0, END).replace('=','').replace('-','').replace('\t\t\t','\t\t'))

        sendButton = Button(root1, text='SEND', font=('arial',14,'bold'), width=16, command=verify_email or exit)
        sendButton.grid(row=2, column=0, pady=20)

        root1.mainloop()

def enter_bill():
    if not os.path.exists('bills'):
        os.makedirs('bills')
        
    for i in os.listdir('bills/'):
        if i.split('.')[0] == Bill_NoEntry.get():
            with open(f'bills/{i}', 'r') as f:
                textarea.delete(1.0, END)
                for data in f:
                    textarea.insert(END, data)
            break
    else:
        messagebox.showerror('Error', 'Invalid Bill Number!!')

def save_bill():
    result = messagebox.askyesno('Confirm', 'Do you Want To Save The Bill!!')
    if result:
        bill_content = textarea.get(1.0, END)
        if not os.path.exists('bills'):
            os.makedirs('bills')
        with open(f'bills/{Bill_NoEntry.get()}.txt', 'w') as file:
            file.write(bill_content)
        messagebox.showinfo('Success', f'Bill Number {Bill_NoEntry.get()} is saved successfully!')

def bill_area():
    if nameEntry.get() == '' or Phone_NumberEntry.get() == '':
        messagebox.showerror('Error', 'Customer Details Are Required!!')
    elif cosmaticspriceEntry.get() == '' and grocerypriceEntry.get() == '' and otherspriceEntry.get() == '':
        messagebox.showerror('Error', 'No Products Are Selected!!')
    elif cosmaticspriceEntry.get() == '0 Rs' and grocerypriceEntry.get() == '0 Rs' and otherspriceEntry.get() == '0 Rs':
        messagebox.showerror('Error', 'No Products Are Selected!!')
    else:
        textarea.delete(1.0, END)
        textarea.insert(END, '\t\t\tWelcome to Hanan\'s Retail\n')
        textarea.insert(END, f'\nBill No. : {Bill_NoEntry.get()}\n')
        textarea.insert(END, f'\nCustomer Name : {nameEntry.get()}\n')
        textarea.insert(END, f'\nPhone No. : {Phone_NumberEntry.get()}\n')
        textarea.insert(END, f'\nPhone No. : {Email_idEntry.get()}\n')
        textarea.insert(END, '\n============================================================\n')
        textarea.insert(END, 'PRODUCT\t\t\tQTY\t\t\tPRICE\n')
        textarea.insert(END, '============================================================\n')
        
        if bathsoapEntry.get() != '0':
            textarea.insert(END, f'\nBath Soap\t\t\t{bathsoapEntry.get()}\t\t\t{soapprice} Rs')
        if FaceCreamEntry.get() != '0':
            textarea.insert(END, f'\nFace Cream\t\t\t{FaceCreamEntry.get()}\t\t\t{FaceCreamprice} Rs')
        if FaceWashEntry.get() != '0':
            textarea.insert(END, f'\nFace Wash\t\t\t{FaceWashEntry.get()}\t\t\t{FaceWashprice} Rs')
        if HairSprayEntry.get() != '0':
            textarea.insert(END, f'\nHair Spray\t\t\t{HairSprayEntry.get()}\t\t\t{HairSprayprice} Rs')
        if BodyLotionsEntry.get() != '0':
            textarea.insert(END, f'\nBody Lotion\t\t\t{BodyLotionsEntry.get()}\t\t\t{BodyLotionsprice} Rs')
        if RiceEntry.get() != '0':
            textarea.insert(END, f'\nRice\t\t\t{RiceEntry.get()}\t\t\t{Riceprice} Rs')
        if Food_oilEntry.get() != '0':
            textarea.insert(END, f'\nFood Oil\t\t\t{Food_oilEntry.get()}\t\t\t{Food_oilprice} Rs')
        if DaalEntry.get() != '0':
            textarea.insert(END, f'\nDaal\t\t\t{DaalEntry.get()}\t\t\t{Daalprice} Rs')
        if WheatEntry.get() != '0':
            textarea.insert(END, f'\nWheat\t\t\t{WheatEntry.get()}\t\t\t{Wheatprice} Rs')
        if SugarEntry.get() != '0':
            textarea.insert(END, f'\nSugar\t\t\t{SugarEntry.get()}\t\t\t{Sugarprice} Rs')
        if MazaEntry.get() != '0':
            textarea.insert(END, f'\nMaza\t\t\t{MazaEntry.get()}\t\t\t{Mazaprice} Rs')
        if CokeEntry.get() != '0':
            textarea.insert(END, f'\nCoke\t\t\t{CokeEntry.get()}\t\t\t{Cokeprice} Rs')
        if FrootiEntry.get() != '0':
            textarea.insert(END, f'\nFrooti\t\t\t{FrootiEntry.get()}\t\t\t{Frootiprice} Rs')
        if NimkosEntry.get() != '0':
            textarea.insert(END, f'\nNimkos\t\t\t{NimkosEntry.get()}\t\t\t{Nimkosprice} Rs')
        if BiscuitEntry.get() != '0':
            textarea.insert(END, f'\nBiscuits\t\t\t{BiscuitEntry.get()}\t\t\t{Biscuitprice} Rs')

        textarea.insert(END, '\n============================================================\n')
        
        if cosmeticstaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nCosmetics Tax\t\t\t{cosmeticstaxEntry.get()}')
        if grocerytaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nGrocery Tax\t\t\t{grocerytaxEntry.get()}')
        if otherstaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nOthers Tax\t\t\t{otherstaxEntry.get()}')

        textarea.insert(END, f'\n\nTotal\t\t\t\t {totalbill} Rs')
        textarea.insert(END, '\n============================================================\n')
        save_bill()

def total():
    global soapprice, FaceCreamprice, FaceWashprice, HairSprayprice, BodyLotionsprice
    global Riceprice, Food_oilprice, Daalprice, Wheatprice, Sugarprice
    global Mazaprice, Cokeprice, Frootiprice, Nimkosprice, Biscuitprice
    global totalbill
    
    # Cosmetics prices
    soapprice = int(bathsoapEntry.get()) * 40  # Adjusted price to match screenshot
    FaceCreamprice = int(FaceCreamEntry.get()) * 140
    FaceWashprice = int(FaceWashEntry.get()) * 260
    HairSprayprice = int(HairSprayEntry.get()) * 180
    BodyLotionsprice = int(BodyLotionsEntry.get()) * 200

    totalcosmaticsprice = soapprice + FaceCreamprice + FaceWashprice + HairSprayprice + BodyLotionsprice
    cosmaticspriceEntry.delete(0, END)
    cosmaticspriceEntry.insert(0, f'Rs. {totalcosmaticsprice}')
    cosmeticstax = totalcosmaticsprice * 0.05  # 5% tax as per screenshot
    cosmeticstaxEntry.delete(0, END)
    cosmeticstaxEntry.insert(0, f'Rs. {cosmeticstax}')

    # Grocery prices
    Riceprice = int(RiceEntry.get()) * 200
    Food_oilprice = int(Food_oilEntry.get()) * 180
    Daalprice = int(DaalEntry.get()) * 150
    Wheatprice = int(WheatEntry.get()) * 200
    Sugarprice = int(SugarEntry.get()) * 50

    totalgroceryprice = Riceprice + Food_oilprice + Daalprice + Wheatprice + Sugarprice
    grocerypriceEntry.delete(0, END)
    grocerypriceEntry.insert(0, f'Rs. {totalgroceryprice}')
    grocerytax = totalgroceryprice * 0.05  # 5% tax as per screenshot
    grocerytaxEntry.delete(0, END)
    grocerytaxEntry.insert(0, f'Rs. {grocerytax}')

    # Others prices
    Mazaprice = int(MazaEntry.get()) * 50
    Cokeprice = int(CokeEntry.get()) * 60
    Frootiprice = int(FrootiEntry.get()) * 20
    Nimkosprice = int(NimkosEntry.get()) * 30
    Biscuitprice = int(BiscuitEntry.get()) * 20

    totalothersprice = Mazaprice + Cokeprice + Frootiprice + Nimkosprice + Biscuitprice
    otherspriceEntry.delete(0, END)
    otherspriceEntry.insert(0, f'Rs. {totalothersprice}')
    otherstax = totalothersprice * 0.05  # 5% tax as per screenshot
    otherstaxEntry.delete(0, END)
    otherstaxEntry.insert(0, f'Rs. {otherstax}')

    totalbill = totalcosmaticsprice + totalgroceryprice + totalothersprice + cosmeticstax + grocerytax + otherstax

# UI Setup
root = Tk()
root.title('Billing Software')
root.geometry('1520x650')
root.resizable(0,0)

headingLabel = Label(root, text='Billing Software', font=('Normal',30,'bold'), bg='steel blue', fg='white')
headingLabel.pack(fill=X)

customer_details_frame = LabelFrame(root, text='CUSTOMER DETAILS', font=('Normal',12,'bold'), bg='steel blue', fg='white')
customer_details_frame.pack(fill=X, pady=5)

nameLabel = Label(customer_details_frame, text='CUSTOMER NAME', font=('Normal',15,'bold'), fg='white', bg='steel blue')
nameLabel.grid(row=0, column=0, padx=20, pady=2)
nameEntry = Entry(customer_details_frame, font=('Normal',10), bd=7, width=20)
nameEntry.grid(row=0, column=1, padx=8)

Phone_NumberLabel = Label(customer_details_frame, text='PHONE NO', font=('Normal',15,'bold'), fg='white', bg='steel blue')
Phone_NumberLabel.grid(row=0, column=2, padx=25, pady=5)
Phone_NumberEntry = Entry(customer_details_frame, font=('Normal',10), bd=7, width=20)
Phone_NumberEntry.grid(row=0, column=3, padx=8)

Email_idLabel = Label(customer_details_frame, text='EMAIL NO', font=('Normal',15,'bold'), fg='white', bg='steel blue')
Email_idLabel.grid(row=0, column=4, padx=25, pady=5)
Email_idEntry = Entry(customer_details_frame, font=('Normal',10), bd=7, width=20)
Email_idEntry.grid(row=0, column=5, padx=8)

Bill_NoLabel = Label(customer_details_frame, text='BILL NO.', font=('Normal',15,'bold'), fg='white', bg='steel blue')
Bill_NoLabel.grid(row=0, column=6, padx=20, pady=2)
Bill_NoEntry = Entry(customer_details_frame, font=('Normal',10), bd=7, width=20)
Bill_NoEntry.grid(row=0, column=7, padx=8)

enterButton = Button(customer_details_frame, text='Enter', font=('Normal',10,'bold'), bd=5, command=insert_data1)
enterButton.grid(row=0, column=8, padx=20, pady=20)

productsframe = Frame(root)
productsframe.pack(pady=5)

cosmaticsFrame = LabelFrame(productsframe, text='COSMETICS', font=('Normal',15,'bold'), bg='steel blue', fg='white', relief=GROOVE, bd=8)
cosmaticsFrame.grid(row=0, column=0)

bathsoapLabel = Label(cosmaticsFrame, text='BATH SOAP', font=('Normal',15,'bold'), bg='steel blue', fg='white')
bathsoapLabel.grid(row=0, column=0, padx=9, pady=10, sticky='w')
bathsoapEntry = Entry(cosmaticsFrame, font=('Normal',15,'bold'), width=10, bd=5)
bathsoapEntry.grid(row=0, column=1, padx=9, pady=10)
bathsoapEntry.insert(0,0)

FaceCreamLabel = Label(cosmaticsFrame, text='FACE CREAM', font=('Normal',15,'bold'), bg='steel blue', fg='white')
FaceCreamLabel.grid(row=1, column=0, padx=9, pady=10, sticky='w')
FaceCreamEntry = Entry(cosmaticsFrame, font=('Normal',15,'bold'), width=10, bd=5)
FaceCreamEntry.grid(row=1, column=1, padx=9, pady=10)
FaceCreamEntry.insert(0,0)

FaceWashLabel = Label(cosmaticsFrame, text='FACE WASH', font=('Normal',15,'bold'), bg='steel blue', fg='white')
FaceWashLabel.grid(row=2, column=0, padx=9, pady=10, sticky='w')
FaceWashEntry = Entry(cosmaticsFrame, font=('Normal',15,'bold'), width=10, bd=5)
FaceWashEntry.grid(row=2, column=1, padx=9, pady=10)
FaceWashEntry.insert(0,0)

HairSprayLabel = Label(cosmaticsFrame, text='HAIR SPRAY', font=('Normal',15,'bold'), bg='steel blue', fg='white')
HairSprayLabel.grid(row=3, column=0, padx=9, pady=10, sticky='w')
HairSprayEntry = Entry(cosmaticsFrame, font=('Normal',15,'bold'), width=10, bd=5)
HairSprayEntry.grid(row=3, column=1, padx=9, pady=10)
HairSprayEntry.insert(0,0)

BodyLotionsLabel = Label(cosmaticsFrame, text='BODY LOTION', font=('Normal',15,'bold'), bg='steel blue', fg='white')
BodyLotionsLabel.grid(row=4, column=0, padx=9, pady=10, sticky='w')
BodyLotionsEntry = Entry(cosmaticsFrame, font=('Normal',15,'bold'), width=10, bd=5)
BodyLotionsEntry.grid(row=4, column=1, padx=9, pady=10)
BodyLotionsEntry.insert(0,0)

groceryFrame = LabelFrame(productsframe, text='GROCERY', font=('Normal',15,'bold'), bg='steel blue', fg='white', relief=GROOVE, bd=8)
groceryFrame.grid(row=0, column=1)

RiceLabel = Label(groceryFrame, text='RICE', font=('Normal',15,'bold'), bg='steel blue', fg='white')
RiceLabel.grid(row=0, column=0, padx=9, pady=10, sticky='w')
RiceEntry = Entry(groceryFrame, font=('Normal',15,'bold'), width=10, bd=5)
RiceEntry.grid(row=0, column=1, padx=9, pady=10)
RiceEntry.insert(0,0)

Food_oilLabel = Label(groceryFrame, text='FOOD OIL', font=('Normal',15,'bold'), bg='steel blue', fg='white')
Food_oilLabel.grid(row=1, column=0, padx=9, pady=10, sticky='w')
Food_oilEntry = Entry(groceryFrame, font=('Normal',15,'bold'), width=10, bd=5)
Food_oilEntry.grid(row=1, column=1, padx=9, pady=10)
Food_oilEntry.insert(0,0)

DaalLabel = Label(groceryFrame, text='DAAL', font=('Normal',15,'bold'), bg='steel blue', fg='white')
DaalLabel.grid(row=2, column=0, padx=9, pady=10, sticky='w')
DaalEntry = Entry(groceryFrame, font=('Normal',15,'bold'), width=10, bd=5)
DaalEntry.grid(row=2, column=1, padx=9, pady=10)
DaalEntry.insert(0,0)

WheatLabel = Label(groceryFrame, text='WHEAT', font=('Normal',15,'bold'), bg='steel blue', fg='white')
WheatLabel.grid(row=3, column=0, padx=9, pady=10, sticky='w')
WheatEntry = Entry(groceryFrame, font=('Normal',15,'bold'), width=10, bd=5)
WheatEntry.grid(row=3, column=1, padx=9, pady=10)
WheatEntry.insert(0,0)

SugarLabel = Label(groceryFrame, text='SUGAR', font=('Normal',15,'bold'), bg='steel blue', fg='white')
SugarLabel.grid(row=4, column=0, padx=9, pady=10, sticky='w')
SugarEntry = Entry(groceryFrame, font=('Normal',15,'bold'), width=10, bd=5)
SugarEntry.grid(row=4, column=1, padx=9, pady=10)
SugarEntry.insert(0,0)

othersFrame = LabelFrame(productsframe, text='OTHERS', font=('Normal',15,'bold'), bg='steel blue', fg='white', relief=GROOVE, bd=8)
othersFrame.grid(row=0, column=2)

MazaLabel = Label(othersFrame, text='MAZA', font=('Normal',15,'bold'), bg='steel blue', fg='white')
MazaLabel.grid(row=0, column=0, padx=9, pady=10, sticky='w')
MazaEntry = Entry(othersFrame, font=('Normal',15,'bold'), width=10, bd=5)
MazaEntry.grid(row=0, column=1, padx=9, pady=10)
MazaEntry.insert(0,0)

CokeLabel = Label(othersFrame, text='COKE', font=('Normal',15,'bold'), bg='steel blue', fg='white')
CokeLabel.grid(row=1, column=0, padx=9, pady=10, sticky='w')
CokeEntry = Entry(othersFrame, font=('Normal',15,'bold'), width=10, bd=5)
CokeEntry.grid(row=1, column=1, padx=9, pady=10)
CokeEntry.insert(0,0)

FrootiLabel = Label(othersFrame, text='FROOTI', font=('Normal',15,'bold'), bg='steel blue', fg='white')
FrootiLabel.grid(row=2, column=0, padx=9, pady=10, sticky='w')
FrootiEntry = Entry(othersFrame, font=('Normal',15,'bold'), width=10, bd=5)
FrootiEntry.grid(row=2, column=1, padx=9, pady=10)
FrootiEntry.insert(0,0)

NimkosLabel = Label(othersFrame, text='NIMKOS', font=('Normal',15,'bold'), bg='steel blue', fg='white')
NimkosLabel.grid(row=3, column=0, padx=9, pady=10, sticky='w')
NimkosEntry = Entry(othersFrame, font=('Normal',15,'bold'), width=10, bd=5)
NimkosEntry.grid(row=3, column=1, padx=9, pady=10)
NimkosEntry.insert(0,0)

BiscuitLabel = Label(othersFrame, text='BISCUITS', font=('Normal',15,'bold'), bg='steel blue', fg='white')
BiscuitLabel.grid(row=4, column=0, padx=9, pady=10, sticky='w')
BiscuitEntry = Entry(othersFrame, font=('Normal',15,'bold'), width=10, bd=5)
BiscuitEntry.grid(row=4, column=1, padx=9, pady=10)
BiscuitEntry.insert(0,0)

billframe = Frame(productsframe, bd=8, relief=GROOVE)
billframe.grid(row=0, column=3, padx=10)

bill_areaLabel = Label(billframe, text='BILL AREA', font=('Normal',15,'bold'), fg='black', bd=7, relief=GROOVE)
bill_areaLabel.pack(fill=X)

Scrollbar = Scrollbar(billframe, orient=VERTICAL)
Scrollbar.pack(side=RIGHT, fill=Y)

textarea = Text(billframe, height=16, width=79, yscrollcommand=Scrollbar.set)
textarea.pack()
Scrollbar.config(command=textarea.yview)

billmenuFrame = LabelFrame(root, text='', font=('Normal',15,'bold'), bg='steel blue', fg='white', relief=GROOVE, bd=8)
billmenuFrame.pack(fill=X)

cosmaticspriceLabel = Label(billmenuFrame, text='TOTAL COSMETICS', font=('Normal',15,'bold'), bg='steel blue', fg='white')
cosmaticspriceLabel.grid(row=0, column=0, pady=9, padx=10, sticky='w')
cosmaticspriceEntry = Entry(billmenuFrame, font=('Normal',15,'bold'), width=10, bd=5)
cosmaticspriceEntry.grid(row=0, column=1, pady=9, padx=10)

grocerypriceLabel = Label(billmenuFrame, text='TOTAL GROCERY', font=('Normal',15,'bold'), bg='steel blue', fg='white')
grocerypriceLabel.grid(row=1, column=0, pady=9, padx=10, sticky='w')
grocerypriceEntry = Entry(billmenuFrame, font=('Normal',15,'bold'), width=10, bd=5)
grocerypriceEntry.grid(row=1, column=1, pady=9, padx=10)

otherspriceLabel = Label(billmenuFrame, text='OTHERS TOTAL', font=('Normal',15,'bold'), bg='steel blue', fg='white')
otherspriceLabel.grid(row=2, column=0, pady=9, padx=10, sticky='w')
otherspriceEntry = Entry(billmenuFrame, font=('Normal',15,'bold'), width=10, bd=5)
otherspriceEntry.grid(row=2, column=1, pady=9, padx=10)

cosmeticstaxLabel = Label(billmenuFrame, text='COSMETICS TAX', font=('Normal',15,'bold'), bg='steel blue', fg='white')
cosmeticstaxLabel.grid(row=0, column=2, pady=9, padx=10, sticky='w')
cosmeticstaxEntry = Entry(billmenuFrame, font=('Normal',15,'bold'), width=10, bd=5)
cosmeticstaxEntry.grid(row=0, column=3, pady=9, padx=10)

grocerytaxLabel = Label(billmenuFrame, text='GROCERY TAX', font=('Normal',15,'bold'), bg='steel blue', fg='white')
grocerytaxLabel.grid(row=1, column=2, pady=9, padx=10, sticky='w')
grocerytaxEntry = Entry(billmenuFrame, font=('Normal',15,'bold'), width=10, bd=5)
grocerytaxEntry.grid(row=1, column=3, pady=9, padx=10)

otherstaxLabel = Label(billmenuFrame, text='OTHERS TAX', font=('Normal',15,'bold'), bg='steel blue', fg='white')
otherstaxLabel.grid(row=2, column=2, pady=9, padx=10, sticky='w')
otherstaxEntry = Entry(billmenuFrame, font=('Normal',15,'bold'), width=10, bd=5)
otherstaxEntry.grid(row=2, column=3, pady=9, padx=10)

buttonFrame = Frame(billmenuFrame, bd=8, relief=GROOVE)
buttonFrame.grid(row=0, column=4, rowspan=3)

totalButton = Button(buttonFrame, text='TOTAL', font=('Normal',16,'bold'), bg='steel blue', fg='white', bd=5, width=8, pady=10, command=total)
totalButton.grid(row=0, column=0, pady=20, padx=5)

billButton = Button(buttonFrame, text='GENERATE BILL', font=('Normal',16,'bold'), bg='steel blue', fg='white', bd=5, width=12, pady=10, command=bill_area)
billButton.grid(row=0, column=1, pady=25, padx=25)

emailButton = Button(buttonFrame, text='EMAIL', font=('Normal',16,'bold'), bg='steel blue', fg='white', bd=5, width=8, pady=10, command=send_email)
emailButton.grid(row=0, column=2, pady=20, padx=5)

clearButton = Button(buttonFrame, text='CLEAR', font=('Normal',16,'bold'), bg='steel blue', fg='white', bd=5, width=8, pady=10, command=clear)
clearButton.grid(row=0, column=3, pady=20, padx=5)

exitButton = Button(buttonFrame, text='EXIT', font=('Normal',16,'bold'), bg='steel blue', fg='white', bd=5, width=8, pady=10, command=Exit)
exitButton.grid(row=0, column=4, pady=20, padx=5)

root.mainloop()

# Close database connection when program ends
mydb.close()