__version__="0.1.1"
import tkinter
import customtkinter
from blockchain import exchangerates as ex




customtkinter.set_appearance_mode("System") #Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue") # Themes: blue (default), dark-blue, green

app = customtkinter.CTk() #create CTK window like you do with the Tk window
app.geometry("400x240")
app.title("Bitcoin Converter App")

#creates a frame effect in background
frame1 = customtkinter.CTkFrame(master = app) #master or placement is the "app" defined
frame1.pack(pady=20, padx=60, fill="both", expand=True)


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


#Function that takes the dollar entry input to convert to bitcoin
def button_function():
    entryState = entry.get()
    e = entryState
    if e.isdigit():        
        btcAmount = int(e)/btcPrice
        btcA = ("{:.8f}".format(btcAmount))
        print(f"{btcA} BTC")
        #shows results. Need to show after convert somehow
        label = customtkinter.CTkLabel(master=app, text=f"Results: {btcA} BTC")
        label.pack(pady=15, padx=15)        
    else:
        print(False)


#Entry box for the conversion
entry = customtkinter.CTkEntry(master=frame1, placeholder_text="Enter $ Amount")
entry.pack(padx=20, pady=10)

#Dropdown menu Next to entry box for currency conversion
#???Need to make this drop menu smaller and adjacent to the left of the entry box. Default USD.
dropMenu1 = customtkinter.CTkOptionMenu(frame1, values=["USD", "CAD", "JPY", "GBP"])
dropMenu1.pack(padx=10, pady=10)
dropMenu1.set("Fiat Type")

#Use CTKButton instead of tkinter Button
#used pack to keep button in place instead of using place which lets it move with window
button = customtkinter.CTkButton(master=frame1, text="Convert", command=button_function)
button.pack(padx=25, pady=10)




app.mainloop()