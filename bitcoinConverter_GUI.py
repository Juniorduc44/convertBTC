#python 3.11
__version__="0.2.0"
import customtkinter
from blockchain import exchangerates as ex
import re

class BitcoinConverter:
    def __init__(self):
        self.app = customtkinter.CTk()
        self.app.geometry("400x340")
        self.app.title("Bitcoin Converter App")
        
        # Get Bitcoin price
        ticker = ex.get_ticker()
        self.btcPrice = ticker["USD"].p15min
        
        # Initialize conversion mode
        self.is_usd_to_btc = True  # True for USD->BTC, False for BTC->USD
        
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
        
        # Entry box with validation
        self.entry = customtkinter.CTkEntry(
            master=self.frame1,
            placeholder_text="Enter Amount (decimals allowed)"
        )
        self.entry.pack(padx=25, pady=10)
        
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
            text="Delete",
            command=self.delete_result
        )
        self.delete_button.pack(padx=25, pady=1)
        
        # Result label
        self.result_label = customtkinter.CTkLabel(
            master=self.frame1,
            text=""
        )
        self.result_label.pack(pady=10)

    def validate_input(self, input_str):
        # Regular expression to match numbers with optional decimal point
        pattern = r'^\d*\.?\d*$'
        return bool(re.match(pattern, input_str)) and input_str != '.'
    
    def toggle_conversion_mode(self):
        self.is_usd_to_btc = not self.is_usd_to_btc
        if self.is_usd_to_btc:
            self.mode_label.configure(text="USD → BTC")
            self.entry.configure(placeholder_text="Enter USD Amount")
        else:
            self.mode_label.configure(text="BTC → USD")
            self.entry.configure(placeholder_text="Enter BTC Amount")
        self.delete_result()
    
    def convert(self):
        entry_value = self.entry.get().strip()
        
        # Validate input
        if not self.validate_input(entry_value):
            self.result_label.configure(
                text="Please enter a valid number\n(decimals allowed)",
                text_color="red"
            )
            return

        try:
            amount = float(entry_value)
            
            # Additional validation for negative numbers
            if amount < 0:
                self.result_label.configure(
                    text="Please enter a positive number",
                    text_color="red"
                )
                return
                
            if self.is_usd_to_btc:
                # Convert USD to BTC
                btc_amount = amount / self.btcPrice
                self.result_label.configure(
                    text=f"Results: {btc_amount:.8f} BTC",
                    text_color="green"
                )
            else:
                # Convert BTC to USD
                usd_amount = amount * self.btcPrice
                self.result_label.configure(
                    text=f"Results: ${usd_amount:,.2f}",
                    text_color="green"
                )
        except ValueError:
            self.result_label.configure(
                text="Please enter a valid number",
                text_color="red"
            )
    
    def delete_result(self):
        self.result_label.configure(text="")
        self.entry.delete(0, 'end')
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")
    app = BitcoinConverter()
    app.run()