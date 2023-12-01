from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

import sqlite3  as db

def connection():          #database 
    connectObj = db.connect("salesRecord.db")
    cur = connectObj.cursor()
    sql = '''
    create table if not exists sellings (
        date string,
        product string,
        price number,
        quantity number,
        total number
        )
    '''
    cur.execute(sql)
    connectObj.commit()   

connection() 
#main    
window=Tk()     
window.title("Record-Keeping")

bikeTop = PhotoImage(file = "logoMain.png")# logo
  
# Setting icon of sales record window
window.iconphoto(False, bikeTop)

tabs = ttk.Notebook(window) 
root= ttk.Frame(tabs)
root2=ttk.Frame(tabs)
#tab zone
tabs.add(root, text ="Sold Items") 
tabs.add(root2, text ="Stock-In") 
tabs.pack(expand = 1,fill ="both") 
  

#first NavBar
def GenerateBill():
    connectObj = db.connect("salesRecord.db")
    cur = connectObj.cursor()  

    global receiptZone
    if roadBkquantity.get()==0 and mountainBkQuantity.get()==0 and FoldingBkQuantity.get()==0 and BmxQuantity.get()==0:
        messagebox.showerror("Opps","Items must be purchased!")
    else:
        receiptZone.delete('1.0',END)
        receiptZone.insert(END,"\t|| shop records ||")
        receiptZone.insert(END,"\n_________________________________________\n")
        receiptZone.insert(END,"\nDate\t Products\tPrice\t   QTY\t Total")
        receiptZone.insert(END,"\n==========================================")

        price= IntVar()
        mountainBkprice2=IntVar()
        FoldingBkprice3=IntVar()
        bmxprice4=IntVar()

        print(dateE.get()) # to show the date
        price=mountainBkprice2=FoldingBkprice3=bmxprice4=0

        if roadBkquantity.get()!=0:
            price=roadBkquantity.get()*roadBkPrice.get()
            print(price)
            receiptZone.insert(END,f"\n{dateE.get()}\t roadBike-1 \t{roadBkPrice.get()}\t {roadBkquantity.get()}\t {price}")

            sql = '''
            INSERT INTO Sellings VALUES 
            (?, ?, ?, ?,?)
            '''
            cur.execute(sql,(dateE.get(),"roadBike-1",roadBkPrice.get(),roadBkquantity.get(),price))
            connectObj.commit() 

        if mountainBkQuantity.get()!=0:
            mountainBkprice2=(mountainBkQuantity.get()*mountainBkPrice.get())
            print(mountainBkprice2)
            receiptZone.insert(END,f"\n{dateE.get()}\t mountainBike-2 \t{mountainBkPrice.get()}\t {mountainBkQuantity.get()}\t {mountainBkprice2}")

            sql = '''
            INSERT INTO Sellings VALUES 
            (?, ?, ?, ?,?)
            '''
            print(dateE.get(),'mountainBike-2',mountainBkPrice.get(),mountainBkQuantity.get(),mountainBkprice2)
            cur.execute(sql,(dateE.get(),'mountainBike-2',mountainBkPrice.get(),mountainBkQuantity.get(),mountainBkprice2))
            connectObj.commit() 

        if FoldingBkQuantity.get()!=0:
            FoldingBkprice3=FoldingBkQuantity.get()*roadBkPrice.get()
            print(FoldingBkprice3)
            receiptZone.insert(END,f"\n{dateE.get()}\tProduct-3 \t{FoldingBkPrice.get()}\t {FoldingBkQuantity.get()}\t {FoldingBkprice3}")

            sql = '''
            INSERT INTO Sellings VALUES 
            (?, ?, ?, ?,?)
            '''
            cur.execute(sql,(dateE.get(),'Product-3',FoldingBkPrice.get(),FoldingBkQuantity.get(),FoldingBkprice3))
            connectObj.commit() 

        if BmxQuantity.get()!=0:
            bmxprice4=BmxQuantity.get()*roadBkPrice.get()
            receiptZone.insert(END,f"\n{dateE.get()}\tProduct-4 \t{BmxPrice.get()}\t {BmxQuantity.get()}\t {bmxprice4}")

            sql = '''
            INSERT INTO Sellings VALUES 
            (?, ?, ?, ?,?)
            '''
            cur.execute(sql,(dateE.get(),'Product-4',BmxPrice.get(),BmxQuantity.get(),bmxprice4))
            connectObj.commit() 

        Totalprice=IntVar()
        Totalprice= sum(price,mountainBkprice2,FoldingBkprice3,bmxprice4) 
        Totalquantity=IntVar()
        Totalquantity=roadBkquantity.get()+mountainBkQuantity.get()+FoldingBkQuantity.get()+BmxQuantity.get()
        receiptZone.insert(END,f"\nTotal \t \t  \t{Totalquantity}\t {Totalprice}")


def view():# this helps retrieve data from my database
    connectObj = db.connect("salesRecord.db")
    cur = connectObj.cursor()  

    sql = 'Select * from Sellings'#sql to select everything
    cur.execute(sql)

    rows=cur.fetchall()
    viewarea.insert(END,f"Date\t Product\t  Price of 1\t  Quantity\t  Price\n")
    
    
    for i in rows:
        allrows=""
        for j in i:
            allrows+=str(j)+'\t'
        allrows+='\n'
        viewarea.insert(END,allrows)

dateL=Label(root,text="Date",bg="orange",width=12,font=('Ubuntu',15,'bold'))
dateL.grid(row=0,column=0,padx=7,pady=7)

dateE=DateEntry(root,width=12,font=('Ubuntu',13,'bold'))
dateE.grid(row=0,column=1,padx=7,pady=7)

l=Label(root, text="Merchandise",font=('Ubuntu',13,'bold'),bg="#c0c3d1",width=12)
l.grid(row=1,column=0,padx=7,pady=7)

l=Label(root, text="Price",font=('Lato',13,'bold'),bg="#c0c3d1",width=12)
l.grid(row=1,column=1,padx=7,pady=7)

l=Label(root, text="Quantity",font=('arial',13,'bold'),bg="#fcba03",width=12)
l.grid(row=1,column=2,padx=7,pady=7)

###########Road Bike####################
roadBkName=StringVar()
roadBkName.set('Road Bike -1')

roadBkPrice=IntVar()
roadBkPrice.set(650) #price for roadBike

roadBkquantity=IntVar()
roadBkquantity.set(0)

l=Label(root, text=roadBkName.get(),font=('arial',15,'bold'),width=12)
l.grid(row=2,column=0,padx=7,pady=7)

l=Label(root, text=roadBkPrice.get(),font=('arial',15,'bold'),width=12)
l.grid(row=2,column=1,padx=7,pady=7)

t=Entry(root,textvariable=roadBkquantity,font=('arial',15,'bold'),width=12)
t.grid(row=2,column=2,padx=7,pady=7)

#MountainBike
mountainBkName=StringVar()
mountainBkName.set('Mountain Bike')

mountainBkPrice=IntVar()
mountainBkPrice.set(2000)

mountainBkQuantity=IntVar()
mountainBkQuantity.set(0)

l=Label(root, text=mountainBkName.get(),font=('arial',15,'bold'),width=12)
l.grid(row=3,column=0,padx=7,pady=7)

l=Label(root, text=mountainBkPrice.get(),font=('arial',15,'bold'),width=12)
l.grid(row=3,column=1,padx=7,pady=7)

t=Entry(root,textvariable=mountainBkQuantity,font=('arial',15,'bold'),width=12)
t.grid(row=3,column=2,padx=7,pady=7)

#Folding Bike###########
p3name=StringVar()
p3name.set('Folding Bike')

FoldingBkPrice=IntVar()
FoldingBkPrice.set(1200) #assingning price to product

FoldingBkQuantity=IntVar()
FoldingBkQuantity.set(0)

l=Label(root, text=p3name.get(),font=('arial',15,'bold'),width=12)
l.grid(row=4,column=0,padx=7,pady=7)

l=Label(root, text=FoldingBkPrice.get(),font=('arial',15,'bold'),width=12)
l.grid(row=4,column=1,padx=7,pady=7)

t=Entry(root,textvariable=FoldingBkQuantity,font=('arial',15,'bold'),width=12)
t.grid(row=4,column=2,padx=7,pady=7)

#BMX
BmxName=StringVar()
BmxName.set("BMX")

BmxPrice=IntVar()
BmxPrice.set(750)

BmxQuantity=IntVar()
BmxQuantity.set(0)

l=Label(root, text=BmxName.get(),font=('arial',15,'bold'),width=12)
l.grid(row=5,column=0,padx=7,pady=7)

l=Label(root, text=BmxPrice.get(),font=('arial',15,'bold'),width=12)
l.grid(row=5,column=1,padx=7,pady=7)

t=Entry(root,textvariable=BmxQuantity,font=('arial',15,'bold'),width=12)
t.grid(row=5,column=2,padx=7,pady=7)

#The receipt
receiptZone=Text(root)

submitbtn=Button(root,command=GenerateBill,text="Bill", #submition button
font=('arial',15,'bold'),bg="#fcba03",width=20 )

submitbtn.grid(row=6,column=0,padx=7,pady=7)

viewbtn=Button(root,command=view,text="View All Sellings",
font=('arial',15,'bold'),bg="#fcba03",width=20 )

viewbtn.grid(row=6,column=2,padx=7,pady=7)

receiptZone.grid(row=9,column=0)
viewarea=Text(root)
viewarea.grid(row=9,column=2)

#Second NavBar
def connection2():
    connectObj2 = db.connect("salesRecord.db")
    cur = connectObj2.cursor()
    sql = '''
    create table if not exists stocks (
        date string,
        product string,
        price number,
        quantity number
        )
    '''
    cur.execute(sql)
    connectObj2.commit()   

connection2() 

def addStock():# function adding stock 
    global dateE2,qty,name,price

    connectObj = db.connect("salesRecord.db")
    cur = connectObj.cursor()  
    sql = '''
            INSERT INTO stocks VALUES 
            (?, ?, ?, ?)
            '''
    cur.execute(sql,(dateE2.get(),name.get(),price.get(),qty.get()))
    connectObj.commit() 

def viewStock():##function to view stock
    connectObj = db.connect("salesRecord.db")
    cur = connectObj.cursor()  

    sql = 'Select * from stocks'
    cur.execute(sql)

    rows=cur.fetchall()
    viewarea2.insert(END,f"Date \tProduct\t  Price\t  Quantity\t \n")
    
    for i in rows:
        allrows=""
        for j in i:
            allrows+=str(j)+'\t'
        allrows+='\n'
        viewarea2.insert(END,allrows)

dateL=Label(root2,text="Date",bg="#fcba03",width=12,font=('arial',15,'bold'))
dateL.grid(row=0,column=0,padx=7,pady=7)

dateE2=DateEntry(root2,width=12,font=('arial',15,'bold'))
dateE2.grid(row=0,column=1,padx=7,pady=7)

l=Label(root2, text="Product",font=('arial',15,'bold'),bg="#d99f19",width=12)
l.grid(row=1,column=0,padx=7,pady=7)

l=Label(root2, text="Price",font=('arial',15,'bold'),bg="#d99f18",width=12)#price button
l.grid(row=2,column=0,padx=7,pady=7)

l=Label(root2, text="Quantity",font=('arial',15,'bold'),bg="#d99f19",width=12)
l.grid(row=3,column=0,padx=7,pady=7)

name=StringVar()
price=IntVar()
qty=IntVar()

Name=Entry(root2,textvariable=name,font=('arial',15,'bold'),width=12)
Name.grid(row=1,column=1,padx=7,pady=7)

Price=Entry(root2,textvariable=price,font=('arial',15,'bold'),width=12)
Price.grid(row=2,column=1,padx=7,pady=7)

Qty=Entry(root2,textvariable=qty,font=('arial',15,'bold'),width=12)
Qty.grid(row=3,column=1,padx=7,pady=7)

addbtn=Button(root2,command=addStock,text="Add",
font=('arial',15,'bold'),bg="#fcba03",width=20)

addbtn.grid(row=4,column=1,padx=7,pady=7)

viewarea2=Text(root2)
viewarea2.grid(row=5,column=0,columnspan=2)

viewbtn2=Button(root2,command=viewStock,text="View Stock",
font=('arial',15,'bold'),bg="#fcba03",width=20 )

viewbtn2.grid(row=4,column=0,padx=7,pady=7)

mainloop()