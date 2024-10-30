__version__="1.0.1"
from blockchain import exchangerates as ex

def get_bitcoin_price():
    try:
        ticker = ex.get_ticker()
        return ticker["USD"].p15min
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

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
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        amount_str = input('\nEnter USD amount to convert to Bitcoin: $')
        amount = validate_input(amount_str)
        if amount is not None:
            btc_amount = amount / btc_price
            print(f"\nResult: {btc_amount:.8f} BTC")
    
    elif choice == "2":
        amount_str = input('\nEnter Bitcoin amount to convert to USD: ')
        amount = validate_input(amount_str)
        if amount is not None:
            usd_amount = amount * btc_price
            print(f"\nResult: ${usd_amount:,.2f}")
    
    else:
        print("\nInvalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")