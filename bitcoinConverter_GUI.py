__version__="0.1.8"
import tkinter
import customtkinter
from blockchain import exchangerates as ex


#Function to delete last result
def myDelete():
    label.configure(text="")


#Function that takes the dollar entry input to convert to bitcoin
def button_function():
    global label
    entryState = entry.get()
    e = entryState
    if e.isdigit():        
        btcAmount = int(e)/btcPrice
        btcA = ("{:.8f}".format(btcAmount))
        print(f"{btcA} BTC")
        #shows results. Need to show after convert somehow
        label.configure(text=f"Results: {btcA} BTC")
    else:
        print(False)



customtkinter.set_appearance_mode("System")#.set_default_color_theme("blue") #Modes: system (default), light, dark
 # Themes: blue (default), dark-blue, green

app = customtkinter.CTk() #create CTK window like you do with the Tk window
app.geometry("400x300")
app.title("Bitcoin Converter App")

#creates a frame effect in background
frame1 = customtkinter.CTkFrame(master = app)
frame1.pack(pady=10, padx=15, expand=True) #master or placement is the "app" defined

#Bitcoin Price Tracker
ticker = ex.get_ticker()
for k in ticker:
    if k == "USD":
        btcPrice = (ticker[k].p15min)

#Bitcoin Label for the current interface showing
label1 = customtkinter.CTkLabel(master=frame1, justify=tkinter.LEFT,text=f'''
    Bitcoin
${btcPrice}''')
label1.pack(pady=10, padx=10)

#Entry box for the conversion
entry = customtkinter.CTkEntry(master=frame1, placeholder_text="Enter $ Amount")
entry.pack(padx=25, pady=10)

#Dropdown menu Next to entry box for currency conversion
#???Need to make this drop menu smaller and adjacent to the left of the entry box. Default USD.
#dropMenu1 = customtkinter.CTkOptionMenu(frame1, values=["USD", "CAD", "JPY", "GBP"])
#dropMenu1.pack(padx=10, pady=10)
#dropMenu1.set("Fiat Type")

#Use CTKButton instead of tkinter Button
#used pack to keep button in place instead of using place which lets it move with window
button = customtkinter.CTkButton(master=frame1, text="Convert", command=button_function).pack(padx=25, pady=10)


#button to delete the label of result
dbutton = customtkinter.CTkButton(master=frame1, text="Delete", command=myDelete).pack(padx=25, pady=1)

#widget to create placement for the results
label = customtkinter.CTkLabel(master=frame1, text="")
label.pack()

app.mainloop()