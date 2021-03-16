from tkinter import *
from tkinter import messagebox,filedialog
from tkinter import ttk
import pymysql
from  datetime import datetime
taz=Tk()
########### main treeview #################
tazTV = ttk.Treeview(height=10, columns=('Item Name''Rate','Type'))

tazTV1 = ttk.Treeview(height=10, columns=('Date''Name','Type','Rate','Total'))



############# validation ######################
def Only_Numeric_Input(P):
    # checks if entry's value is an integer or empty and returns an appropriate boolean
    if P.isdigit() or P == "":  # if a digit was entered or nothing was entered
        return True
    return False

def Only_Char_Input(P):
    # checks if entry's value is an integer or empty and returns an appropriate boolean
    if P.isalpha() or P == "":  # if a digit was entered or nothing was entered
        return True
    return False
callback = taz.register(Only_Char_Input)  # registers a Tcl to Python callback
callback1 = taz.register(Only_Numeric_Input)  # registers a Tcl to Python callback

####################  combo data  ##########
def combo_input():
    dbconfig()
    mycursor.execute('select item_name from itemlist')
    data = []
    for row in mycursor.fetchall():
        data.append(row[0])
    return data

################ optionCallBack ######
def optionCallBack(*args):
    global itemname
    itemname=combovariable.get()
    #print(itemname)
    aa=ratelist()
    #print(aa)
    baserate.set(aa)
    global v
    for i in aa:
        for j in i:
            v=j
 ######################### callback 1 ##############
def optionCallBack1(*args):
    global qty
    qty=qtyvariable.get()
    final = int(v)*int(qty)
    costVar.set(final)


def ratelist():
    dbconfig()
    que2="select item_rate from itemlist where item_name=%s"
    val=(itemname)
    mycursor.execute(que2,val)
    data=mycursor.fetchall()
    #print(data)
    return data
############# bill generation ########################
global x
x=datetime.now()
datetimeVar=StringVar()
datetimeVar.set(x)
customer_nameVar=StringVar()
phoneVar=StringVar()
combovariable=StringVar()
baserate=StringVar()
costVar=StringVar()
qtyvariable=StringVar()
def BillGenerationWindow():
    remove_all_widgets()
    mainheading()
    itemnameLabel = Label(taz, text="Generate Bill", font="Arial 30")
    itemnameLabel.grid(row=1, column=1, padx=(50, 0), columnspan=2, pady=10)

    BackButton = Button(taz, text="Back", width=20, height=2, fg="green", bd=10, command=Back)
    BackButton.grid(row=2, column=0, columnspan=1)

    printButton = Button(taz, text="Print Bill", width=20, height=2, fg="green", bd=10, command=PrintBill)
    printButton.grid(row=5, column=0, columnspan=1)

    logoutButton = Button(taz, text="Logout", width=20, height=2, fg="green", bd=10, command=LogOut)
    logoutButton.grid(row=2, column=3, columnspan=1)

    dateTimeLabel = Label(taz,text="Date & Time",font=("arial",13,"bold"))
    dateTimeLabel.grid(row=2,column=1,padx=20,pady=5)

    dateTimeEntry=Entry(taz,textvariable=datetimeVar,font=("arial",13,"bold"))
    dateTimeEntry.grid(row=2, column=2, padx=20, pady=5)

    customer_nameLabel = Label(taz, text="Customer Name", font=("arial", 13, "bold"))
    customer_nameLabel.grid(row=3, column=1, padx=20, pady=5)

    customer_nameEntry = Entry(taz, textvariable=customer_nameVar, font=("arial", 13, "bold"))
    customer_nameEntry.grid(row=3, column=2, padx=20, pady=5)
    customer_nameEntry.configure(validate="key", validatecommand=(callback, "%P"))

    phoneLabel = Label(taz, text="Mobile_No", font=("arial", 13, "bold"))
    phoneLabel.grid(row=4, column=1, padx=20, pady=5)

    phoneEntry = Entry(taz, textvariable=phoneVar, font=("arial", 13, "bold"))
    phoneEntry.grid(row=4, column=2, padx=20, pady=5)
    phoneEntry.configure(validate="key", validatecommand=(callback1, "%P"))

    selectLabel = Label(taz,text="Select Item",font=("ariel",13,"bold"))
    selectLabel.grid(row=5,column=1,padx=20,pady=5)

    l = combo_input()

    c = ttk.Combobox(taz,values=l,textvariable=combovariable,font=("ariel",13,"bold"))
    c.set("select Item")
    combovariable.trace('w',optionCallBack)
    c.grid(row=5,column=2,padx=20,pady=5)

    rateLabel = Label(taz, text="Item Rate", font=("arial", 13, "bold"))
    rateLabel.grid(row=6, column=1, padx=20, pady=5)

    rateEntry = Entry(taz, textvariable=baserate, font=("arial", 13, "bold"))
    rateEntry.grid(row=6, column=2, padx=20, pady=5)
    rateEntry.configure(validate="key", validatecommand=(callback1, "%P"))

    qtyLabel = Label(taz,text="Select Quantity",font=("ariel",13,"bold"))
    qtyLabel.grid(row=7,column=1,padx=20,pady=5)


    global qtyvariable
    l2 = [1,2,3,4,5,6,7]
    qty = ttk.Combobox(taz, values=l2, textvariable=qtyvariable, font=("ariel", 13, "bold"))
    qty.set("select Quantity")
    qtyvariable.trace('w', optionCallBack1)
    qty.grid(row=7, column=2, padx=20, pady=5)

    costLabel = Label(taz, text="Cost", font=("arial", 13, "bold"))
    costLabel.grid(row=8, column=1, padx=20, pady=5)

    costEntry = Entry(taz, textvariable=costVar, font=("arial", 13, "bold"))
    costEntry.grid(row=8, column=2, padx=20, pady=5)
    costEntry.configure(validate="key", validatecommand=(callback1, "%P"))

    saveBillButton = Button(taz, text="Save Bill", width=20, height=2, fg="red", bd=10, command=Save_Bill)
    saveBillButton.grid(row=5, column=3, columnspan=1)

#############################
#######################v   Save_Bill   ###############
def Save_Bill():
    dt = datetimeVar.get()
    customer = customer_nameVar.get()
    mobile= phoneVar.get()
    item_name = itemname
    itemrate = v
    itemqty = qtyvariable.get()
    total = costVar.get()
    print(dt,customer,mobile,item_name,itemrate,itemqty,total)
    dbconfig()
    insqu = "insert into bill(datetime,customer_name,phone,item_name,item_rate,item_qty,cost) values(%s,%s,%s,%s,%s,%s,%s)"
    val=(dt,customer,mobile,item_name,itemrate,itemqty,total)
    mycursor.execute(insqu, val)
    conn.commit()
    messagebox.showinfo("Save Data","Bill Saved successfully")
    customer_nameVar.set("")
    phoneVar.set("")
    itemnameVar.set("")
    costVar.set("")

############## back buttton #####################
############## PrintBill  #######################
def PrintBill():
    remove_all_widgets()
    mainheading()

    printitem = Label(taz, text="Print Bill Details", font="Arial 30")
    printitem.grid(row=1, column=1, padx=(50, 0), columnspan=2, pady=10)

    BackButton = Button(taz, text="Back", width=20, height=2, fg="green", bd=10, command=Back)
    BackButton.grid(row=1, column=0, columnspan=1)

    logoutButton = Button(taz, text="LogOut", width=20, height=2, fg="green", bd=10, command=LogOut)
    logoutButton.grid(row=1, column=3, columnspan=1)

    ClickButton = Button(taz, text="Double Click", font="Arial 30")
    ClickButton.grid(row=2, column=1, padx=(50, 0), columnspan=2, pady=10)


################## TreeViews ###################
    tazTV1.grid(row=5, column=0, columnspan=4)
    style = ttk.Style(taz)
    style.theme_use('clam')
    style.configure("Treeview", fieldbackground="green")
    scrollBar = Scrollbar(taz, orient="vertical", command=tazTV1.yview)
    scrollBar.grid(row=5, column=5, sticky="NSE")

    tazTV1.configure(yscrollcommand=scrollBar.set)

    tazTV1.heading('#0', text="Date/Time")
    tazTV1.heading('#1', text="Name")
    tazTV1.heading('#2', text="Mobile")
    tazTV1.heading('#3', text="selected Food")
    tazTV1.heading('#4', text="Total")
    displaybill()
######################### End ####################################
#################################  Display Bill ##################
def displaybill():
    records = tazTV1.get_children()

    for element in records:
        tazTV1.delete(element)

    # insert data in treeview
    conn = pymysql.connect(host="localhost", user="root", db="wahtaz")
    mycursor = conn.cursor(pymysql.cursors.DictCursor)
    # print(mycursor)
    query = "select * from bill"
    mycursor.execute(query)
    data = mycursor.fetchall()
    # print(data)

    for row in data:
        tazTV1.insert('', 'end', text=row['datetime'], values=(row['customer_name'], row['phone'], row['item_name'], row['cost']))

    conn.close()
    tazTV1.bind("<Double-1>", OnDoubleClick2)
####################### OnDoubleClick2 ################
def OnDoubleClick2(event):
    item = tazTV1.selection()
    global itemNameVar11

    itemNameVar11 = tazTV1.item(item, "text")
    item_detail1 = tazTV1.item(item, "values")
    receipt()
######################## End OnDoubleClick2 #############
############## recept  #######################
def receipt():
    billstring = ""
    billstring += "========== My Hotel Bill ==========\n\n"
    billstring += "========== Customer Details ==========\n\n"

    dbconfig()
    query = "select * from bill where datetime='{}';".format(itemNameVar11)

    mycursor.execute(query)
    data=mycursor.fetchall()
    #print(data)
    for row in data:
        billstring += "{}{:<20}{:10}\n".format("Date/Time","",row[1])
        billstring += "{}{:<20}{:10}\n".format("Customer Name", "", row[2])
        billstring += "{}{:<20}{:10}\n".format("Contect No", "", row[3])
        billstring += "\n===================Item Details ===================\n "

        billstring += "{:<10}{:<10}{:<15}{:<15}".format("Item Name", "Rate", "Quantity", "Total Cost")
        billstring += "{:<10}{:<10}{:<25}{:<25}".format(row[4],row[5],row[6],row[7])
        billstring += "======================================================\n"
        billstring += "{}{:<10}{:<15}{:<10}\n".format("Total Cost","","",row[7])
        billstring += "\n\n ============== Thanks PLease Visit Again =================\n"
    billfile = filedialog.asksaveasfile(mode="w",defaultextension="txt")
    if billfile is None:
        messagebox.showerror("File Name Error","Invailid file Name")
    else:
        billfile.write(billstring)
        billfile.close()

######################## End Receipt #############
def Back():
    remove_all_widgets()
    mainheading()
    WelcomeWindow()

####################Update Button###############
def Update():

    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemTypeVar.get()
    dbconfig()
    que ="update itemlist set item_rate=%s,item_type=%s where item_name=%s"
    val=(rate,type,name)
    mycursor.execute(que,val)
    conn.commit()
    messagebox.showinfo("Updating configuration","Item Updated Successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemTypeVar.set("")
    GetItemInTreeView()

################ Delete Button ################
def Delete():
    name=itemnameVar.get()
    rate=itemrateVar.get()
    type=itemTypeVar.get()
    dbconfig()
    que1 = "delete from itemlist where item_name=%s"
    val=(name)
    mycursor.execute(que1,val)
    conn.commit()
    messagebox.showinfo("Delete configuration","Item Deleted Successfully")
    itemnameVar.set("")
    itemrateVar.set("")
    itemTypeVar.set("")
    GetItemInTreeView()

############# BILLING BUtton ###########

def Billing():
    BillGenerationWindow()

########## add item ################

def AddItem():
    name = itemnameVar.get()
    rate = itemrateVar.get()
    type = itemTypeVar.get()
   # print(name, rate, type)
    dbconfig()
    query = "insert into itemlist (item_name,item_rate,item_type) values(%s,%s,%s);"
    val = (name, rate, type)
    mycursor.execute(query, val)
    conn.commit()
    messagebox.showinfo("Save Data", 'Item Inserted Successfully')
    itemnameVar.set("")
    itemrateVar.set("")
    itemTypeVar.set("")
    # to fetch data in treeview
    GetItemInTreeView()
############ get Item in tree view ###############
def GetItemInTreeView():
    # to delete already inserted item
    records = tazTV.get_children()

    for element in records:
        tazTV.delete(element)

    # insert data in treeview
    conn = pymysql.connect(host="localhost", user="root", db="wahtaz")
    mycursor = conn.cursor(pymysql.cursors.DictCursor)
   # print(mycursor)
    query = "select * from itemlist"
    mycursor.execute(query)
    data = mycursor.fetchall()
   # print(data)

    for row in data:
        tazTV.insert('', 'end', text=row['item_name'], values=(row["item_rate"], row["item_type"]))

    conn.close()
    tazTV.bind("<Double-1>", OnDoubleClick)
############## OnDoubleClick ###########

def OnDoubleClick(event):
    item = tazTV.selection()
    itemNameVar1 = tazTV.item(item,"text")
    item_detail = tazTV.item(item,"values")
    itemnameVar.set(itemNameVar1)
    itemrateVar.set(item_detail[0])
    itemTypeVar.set(item_detail[1])
#######################################
itemnameVar=StringVar()
itemrateVar=StringVar()
itemTypeVar=StringVar()

def AddItemWindow():
    remove_all_widgets()
    mainheading()
    itemnameLabel = Label(taz, text="ITEM DETAILS", font="Arial 30")
    itemnameLabel.grid(row=1, column=1, padx=(50, 0), columnspan=2, pady=10)

    ###############################
    BackButton = Button(taz, text="Back", width=20, height=2, fg="green", bd=10, command=Back)
    BackButton.grid(row=1, column=0, columnspan=1)

    DeleteButton = Button(taz, text="Delete", width=20, height=2, fg="green", bd=10, command=Delete)
    DeleteButton.grid(row=3, column=0, columnspan=1)

    logoutButton = Button(taz, text="Logout", width=20, height=2, fg="green", bd=10, command=LogOut)
    logoutButton.grid(row=1, column=3, columnspan=1)

    updateButton = Button(taz, text="Update", width=20, height=2, fg="green", bd=10, command=Update)
    updateButton.grid(row=3, column=3, columnspan=1)

    BillButton = Button(taz, text="Billing", width=20, height=2, fg="green", bd=10, command=Billing)
    BillButton.grid(row=5, column=3, columnspan=1)

    ###########################

    itemnameLabel = Label(taz, text="Item name",font=("arial",15,"bold"))
    itemnameLabel.grid(row=2, column=1, padx=20, pady=5)

    itemrateLabel = Label(taz, text="Item Rate(INR)",font=("arial",15,"bold"))
    itemrateLabel.grid(row=3, column=1, padx=20, pady=5)

    itemTypeLabel = Label(taz, text="Item Type",font=("arial",15,"bold"))
    itemTypeLabel.grid(row=4, column=1, padx=20, pady=5)

    itemnameEntry = Entry(taz, textvariable=itemnameVar,font=("arial",13,"bold"))
    itemnameEntry.grid(row=2, column=2, padx=5, pady=5)
    itemnameEntry.configure(validate="key", validatecommand=(callback, "%P"))  # enables validation

    itemrateEntry = Entry(taz, textvariable=itemrateVar,font=("arial",13,"bold"))
    itemrateEntry.grid(row=3, column=2, padx=5, pady=5)
    itemrateEntry.configure(validate="key", validatecommand=(callback1, "%P"))  # enables validation

    itemTypeEntry = Entry(taz, textvariable=itemTypeVar,font=("arial",13,"bold"))
    itemTypeEntry.grid(row=4, column=2, padx=5, pady=5)
    itemTypeEntry.configure(validate="key", validatecommand=(callback, "%P"))  # enables validation

    additemButton = Button(taz, text="Add Item", width=20, height=2, fg="green", bd=10, command=AddItem)
    additemButton.grid(row=5, column=0, columnspan=1)

    label = Label(taz)
    label.grid(row=6, column=2, padx=20, pady=5)
    ###############################################
###############  TReeviews  #############################

    tazTV.grid(row=7, column=0, columnspan=3)
    style = ttk.Style(taz)
    style.theme_use('clam')
    style.configure("Treeview", fieldbackground="green")
    scrollBar = Scrollbar(taz, orient="vertical", command=tazTV.yview)
    scrollBar.grid(row=7, column=2, sticky="NSE")

    tazTV.configure(yscrollcommand=scrollBar.set)

    tazTV.heading('#0', text="Item Name")
    tazTV.heading('#1', text="Rate")
    tazTV.heading('#2', text="Type")
    # to fetch data in treeview
    GetItemInTreeView()
#########################remove all widgets from screen #################

def remove_all_widgets():
    global taz
    for widget in taz.winfo_children():
        widget.grid_remove()
############ mainheading creation ###########
def mainheading():
    label = Label(taz, text="          Hotel WahTaz Management system              " , bg="blue", fg="Red",
                  font=("Comic Sans Ms", 40, "bold"), padx=0, pady=0)
    label.grid(row=0, columnspan=4)
##############################################
############# def logout ########################
def LogOut():
    remove_all_widgets()
    mainheading()
    LoginWindow()
############### database conncetion #########################
def dbconfig():
    global mycursor,conn
    conn = pymysql.connect(host="localhost", user="root", db="wahtaz")
    mycursor = conn.cursor()

############ Welcome window ############
def WelcomeWindow():
    remove_all_widgets()
    mainheading()
    welcomeLabel = Label(taz, text="Welcome User", font="Arial 30")
    welcomeLabel.grid(row=1, column=1, padx=(50, 0), columnspan=2, pady=10)

    additemButton = Button(taz, text="Manage Restaurant", width=20, height=2, fg="green", bd=10, command=AddItemWindow)
    additemButton.grid(row=3, column=0, columnspan=1)

    billButton = Button(taz, text="Bill Generation", width=20, height=2, fg="green", bd=10, command=BillGenerationWindow)
    billButton.grid(row=3, column=1, columnspan=2)

    logoutButton = Button(taz, text="Logout", width=20, height=2, fg="green", bd=10, command=LogOut)
    logoutButton.grid(row=3, column=3, columnspan=1)


############### admin Login ###################
def AdminLogin():
    username = usernameVar.get()
    password = passwordVar.get()
    if(username=="" or password==""):
        messagebox.showerror("Data Filling Error","Please Fill user Name and Password both")
    else:
        dbconfig()
        que = "select * from user_info where user_id=%s and password=%s"
        val = (username, password)
        mycursor.execute(que, val)
        data = mycursor.fetchall()
        flag = False
        for row in data:
            flag = True

        conn.close()
        if flag == True:
            WelcomeWindow()

        else:
            messagebox.showerror("Invalid User Credential", 'either User Name or Password is incorrect')
            usernameVar.set("")
            passwordVar.set("")

##########################################
############### login window ####################
usernameVar = StringVar()
passwordVar = StringVar()

def LoginWindow():
    usernameVar.set("")
    passwordVar.set("")
    loginLabel = Label(taz, text="Admin Login", font="Arial 30")
    loginLabel.grid(row=1, column=1, padx=(50, 0), columnspan=2, pady=10)

    usernameLabel = Label(taz, text="Username",font=("arial",13,"bold"))
    usernameLabel.grid(row=3, column=1, padx=20, pady=5)

    passwordLabel = Label(taz, text="Password",font=("arial",13,"bold"))
    passwordLabel.grid(row=6, column=1, padx=20, pady=5)

    usernameEntry = Entry(taz, textvariable=usernameVar,font=("arial",13,"bold"))
    usernameEntry.grid(row=3, column=2, padx=20, pady=5)
    usernameEntry.configure(validate="key", validatecommand=(callback, "%P"))

    passwordEntry = Entry(taz, show="*", textvariable=passwordVar,font=("arial",13,"bold"))
    passwordEntry.grid(row=6, column=2, padx=20, pady=5)

    loginButton = Button(taz, text="Login", width=20, height=2, fg="green", bd=10, command=AdminLogin)
    loginButton.grid(row=8, column=1, columnspan=2)


################################################
screen_width=taz.winfo_screenwidth()
#print(screen_width)
screen_height=taz.winfo_screenheight()
#print(screen_height)
taz.title("             Hotel WahTaz Managment System    ")
mainheading()
LoginWindow()

#taz.geometry("900x600+120+50")
taz.geometry("%dx%d+0+0"%(screen_width,screen_height))
mainloop()