a = float(input("Enter starting number: "))
b = float(input("Enter final number: "))

c = b - a

if a > b:  # if a is greater than b then to get to b your result will be negative.
    cc = f"{c:.8f}"
    d = c / b
    e = d * 100
    ee = f"{e:.2f}"
    print(f'''
  1.) {a}
  2.) {b}

        The results of getting from (1) to (2):

                    Diff = {cc}
                  % Diff = {ee}%
        ''')

elif a < b:
    cc = f"{c:.8f}"
    d = c / b
    e = d * 100
    ee = f"{e:.2f}"
    print(f'''
  1.) {a}
  2.) {b}

        The results of getting from (1) to (2):

                    Diff = {cc}
                  % Diff = {ee}%

        ''')

elif a == b:
    print("The entered numbers are the same.")

else:
    print("Thank you, come again.")