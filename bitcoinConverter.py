#python 3.11
__version__="2.1.0"
from blockchain import exchangerates as ex

def get_bitcoin_price():
    try:
        ticker = ex.get_ticker()
        return ticker["USD"].p15min
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

def format_usd_amount(amount):
    # If amount is less than 1 cent, show up to 8 decimal places
    if amount < 0.01:
        return f"${amount:.8f}"
    # Otherwise use standard 2 decimal places
    return f"${amount:,.2f}"

def validate_input(amount_str):
    try:
        amount = float(amount_str)
        if amount < 0:
            print("Please enter a positive number.")
            return None
        return amount
    except ValueError:
        print("Please enter a valid number.")
        return None

def main():
    # Get current Bitcoin price
    btc_price = get_bitcoin_price()
    if not btc_price:
        return
    
    print(f"\nCurrent Bitcoin Price: ${btc_price:,.2f}")
    print("\nSelect conversion type:")
    print("1. USD to BTC")
    print("2. BTC to USD")
    print("Note: 1 satoshi = 0.00000001 BTC")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        amount_str = input('\nEnter USD amount to convert to Bitcoin: $')
        amount = validate_input(amount_str)
        if amount is not None:
            btc_amount = amount / btc_price
            satoshis = int(btc_amount * 100000000)  # Convert to satoshis
            if satoshis < 100:  # If less than 100 satoshis
                print(f"\nResult: {satoshis} satoshi(s)")
                print(f"Result: {btc_amount:.8f} BTC")
            else:
                print(f"\nResult: {btc_amount:.8f} BTC")
                print(f"Result: {satoshis:,} satoshis")
    
    elif choice == "2":
        amount_str = input('\nEnter Bitcoin amount (or use "sat" for satoshis, e.g., "1000sat"): ')
        if amount_str.lower().endswith('sat'):
            # Handle satoshi input
            try:
                satoshis = float(amount_str[:-3])  # Remove 'sat' from the end
                amount = satoshis / 100000000  # Convert satoshis to BTC
            except ValueError:
                print("Invalid satoshi amount")
                return
        else:
            amount = validate_input(amount_str)
            
        if amount is not None:
            usd_amount = amount * btc_price
            formatted_usd = format_usd_amount(usd_amount)
            print(f"\nResult: {formatted_usd}")
            # If it's a very small amount, show satoshis
            if amount < 0.00001:
                satoshis = int(amount * 100000000)
                print(f"Input was approximately {satoshis} satoshi(s)")
    
    else:
        print("\nInvalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")