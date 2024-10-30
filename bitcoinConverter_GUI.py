#python 3.11
__version__="2.1.0"
import customtkinter
import re
from blockchain import exchangerates as ex

class BitcoinConverter:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.geometry("500x440")
        self.app.title("Bitcoin Converter App")
        
        # Get Bitcoin price
        ticker = ex.get_ticker()
        self.btcPrice = ticker["USD"].p15min
        
        # Initialize conversion mode
        self.is_usd_to_btc = True
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        self.frame1 = customtkinter.CTkFrame(master=self.app)
        self.frame1.pack(pady=10, padx=15, expand=True)
        
        # Bitcoin price label
        self.label1 = customtkinter.CTkLabel(
            master=self.frame1,
            text=f"Bitcoin\n${self.btcPrice:,.2f}"
        )
        self.label1.pack(pady=10, padx=10)
        
        # Satoshi info label
        self.satoshi_info = customtkinter.CTkLabel(
            master=self.frame1,
            text="1 satoshi = 0.00000001 BTC",
            font=("Helvetica", 12)
        )
        self.satoshi_info.pack(pady=5)
        
        # Toggle switch frame
        self.toggle_frame = customtkinter.CTkFrame(master=self.frame1)
        self.toggle_frame.pack(pady=5)
        
        # Toggle switch with labels
        self.mode_label = customtkinter.CTkLabel(
            master=self.toggle_frame,
            text="USD → BTC"
        )
        self.mode_label.pack(side='left', padx=10)
        
        self.toggle_switch = customtkinter.CTkSwitch(
            master=self.toggle_frame,
            text="",
            command=self.toggle_conversion_mode
        )
        self.toggle_switch.pack(side='left', padx=10)
        
        # Entry frame
        self.entry_frame = customtkinter.CTkFrame(master=self.frame1)
        self.entry_frame.pack(pady=10, padx=10, fill="x")
        
        # Entry box
        self.entry = customtkinter.CTkEntry(
            master=self.entry_frame,
            placeholder_text="Enter Amount"
        )
        self.entry.pack(side='left', padx=5, expand=True, fill="x")
        
        # Satoshi checkbox
        self.use_satoshi = customtkinter.CTkCheckBox(
            master=self.entry_frame,
            text="Satoshi",
            command=self.toggle_satoshi_mode
        )
        self.use_satoshi.pack(side='right', padx=5)
        self.use_satoshi.configure(state="disabled")
        
        # Convert button
        self.convert_button = customtkinter.CTkButton(
            master=self.frame1,
            text="Convert",
            command=self.convert
        )
        self.convert_button.pack(padx=25, pady=10)
        
        # Delete button
        self.delete_button = customtkinter.CTkButton(
            master=self.frame1,
            text="Clear",
            command=self.delete_result
        )
        self.delete_button.pack(padx=25, pady=1)
        
        # Result labels
        self.result_label = customtkinter.CTkLabel(
            master=self.frame1,
            text="",
            font=("Helvetica", 14, "bold")
        )
        self.result_label.pack(pady=5)
        
        self.satoshi_result_label = customtkinter.CTkLabel(
            master=self.frame1,
            text="",
            font=("Helvetica", 12)
        )
        self.satoshi_result_label.pack(pady=5)
        
        # Additional label for micro-amounts
        self.micro_amount_label = customtkinter.CTkLabel(
            master=self.frame1,
            text="",
            font=("Helvetica", 12)
        )
        self.micro_amount_label.pack(pady=5)
    
    def toggle_satoshi_mode(self):
        self.delete_result()
    
    def toggle_conversion_mode(self):
        self.is_usd_to_btc = not self.is_usd_to_btc
        if self.is_usd_to_btc:
            self.mode_label.configure(text="USD → BTC")
            self.entry.configure(placeholder_text="Enter USD Amount")
            self.use_satoshi.configure(state="disabled")
            self.use_satoshi.deselect()
        else:
            self.mode_label.configure(text="BTC → USD")
            self.entry.configure(placeholder_text="Enter BTC Amount")
            self.use_satoshi.configure(state="normal")
        self.delete_result()
    
    def format_usd_amount(self, amount):
        if amount < 0.01:
            return f"${amount:.8f}"
        return f"${amount:,.2f}"
    
    def convert(self):
        entry_value = self.entry.get().strip()
        
        try:
            # Handle satoshi input
            if not self.is_usd_to_btc and self.use_satoshi.get():
                amount = float(entry_value) / 100000000  # Convert satoshis to BTC
            else:
                amount = float(entry_value)
            
            if amount < 0:
                self.result_label.configure(
                    text="Please enter a positive number",
                    text_color="red"
                )
                return
                
            if self.is_usd_to_btc:
                # Convert USD to BTC
                btc_amount = amount / self.btcPrice
                satoshis = int(btc_amount * 100000000)
                
                self.result_label.configure(
                    text=f"{btc_amount:.8f} BTC",
                    text_color="green"
                )
                self.satoshi_result_label.configure(
                    text=f"{satoshis:,} satoshis",
                    text_color="green"
                )
                
                # Clear micro amount label in this mode
                self.micro_amount_label.configure(text="")
                
            else:
                # Convert BTC to USD
                usd_amount = amount * self.btcPrice
                formatted_usd = self.format_usd_amount(usd_amount)
                
                self.result_label.configure(
                    text=formatted_usd,
                    text_color="green"
                )
                
                # Show additional information for small amounts
                if usd_amount < 0.01:
                    self.satoshi_result_label.configure(
                        text=f"Less than 1¢ (USD)",
                        text_color="orange"
                    )
                    # Show micro-amount details
                    micro_usd = usd_amount * 1000000  # Convert to millionths of a dollar
                    self.micro_amount_label.configure(
                        text=f"(Approximately {micro_usd:.6f} millionths of a dollar)",
                        text_color="orange"
                    )
                else:
                    self.satoshi_result_label.configure(text="")
                    self.micro_amount_label.configure(text="")
                
                # Show satoshi amount for small BTC inputs
                if amount < 0.00001:
                    satoshis = int(amount * 100000000)
                    self.satoshi_result_label.configure(
                        text=f"Input was approximately {satoshis} satoshi(s)",
                        text_color="green"
                    )
                
        except ValueError:
            self.result_label.configure(
                text="Please enter a valid number",
                text_color="red"
            )
            self.satoshi_result_label.configure(text="")
            self.micro_amount_label.configure(text="")
    
    def delete_result(self):
        self.result_label.configure(text="")
        self.satoshi_result_label.configure(text="")
        self.micro_amount_label.configure(text="")
        self.entry.delete(0, 'end')
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")
    app = BitcoinConverter()
    app.run()