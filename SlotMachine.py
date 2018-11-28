#######################################################################################
#
#     Program was written for the Advanced Programming class at Lakeland University.
#     Author: Zachary Dorow
#     Teacher: Mr. Kevin Kurek
#     Last Edited: Nov 18, 2018
#
#     Description: The program function is to simulate a Slot Machine.
#
#
#######################################################################################
import os
import re
import time
import random
import threading
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox


class Wheel:

    def __init__(self):
        self.pick = self.spin()

    @staticmethod
    def spin():
        random_pick = random.randint(1, 3)
        return random_pick

    def set_pick(self):
        self.pick = self.spin()
        return self.pick

    def get_pick(self):
        return self.pick


class Customer:

    def __init__(self, balance, bet):
        self.balance = self.set_balance(balance)
        self.bet = self.set_bet(bet)

    def set_balance(self, balance):
        if balance < 0:
            self.balance = 0
        else:
            self.balance = balance
        return self.balance

    def get_balance(self):
        return self.balance

    def set_bet(self, bet):
        if bet in range(1, 4):
            self.bet = bet
        elif bet < 1:
            self.bet = 1
        else:
            self.bet = 4

        return self.bet

    def get_bet(self):
        return self.bet


class SlotMachineGUI:

    def __init__(self, master):

        try:
            # File locations of the pictures used for the slot machine.
            # These ones are used to create the .exe
            lemon = self.resource_path("assets/lemon.png")
            lemon_img = PhotoImage(file=lemon)
            grape = self.resource_path("assets/grape.png")
            grape_img = PhotoImage(file=grape)
            cherry = self.resource_path("assets/cherry.png")
            cherry_img = PhotoImage(file=cherry)

            # These are needing the paths
            # lemon_img = PhotoImage(file=r"C:\Users\ZD\IdeaProjects\PythonClassStuff\lemon.png")
            # grape_img = PhotoImage(file=r"C:\Users\ZD\IdeaProjects\PythonClassStuff\grape.png")
            # cherry_img = PhotoImage(file=r"C:\Users\ZD\IdeaProjects\PythonClassStuff\cherry.png")

            # Dictionary to easily reference the different pieces of the wheel.
            pieces = {1: lemon_img, 2: grape_img, 3: cherry_img}

            # Getting the GUI going.
            self.master = master
            master.geometry("455x435")
            master.resizable(False, False)
            master.title("Slot Machine")
            master.configure(background='black')

            # Initializing the Customer and Wheel classes.
            self.customer = Customer(0, 1)
            self.first_wheel = Wheel()
            self.second_wheel = Wheel()
            self.third_wheel = Wheel()

            # Frames to help split up the interface.
            top_frame = Frame(master, highlightbackground="green", highlightcolor="green", highlightthickness=1)
            self.top_frame = top_frame

            middle_frame = Frame(master, highlightbackground="green", highlightcolor="green", highlightthickness=2,
                                 bg="white", )
            self.middle_frame = middle_frame

            top_bottom_frame = Frame(master, highlightbackground="green", highlightcolor="green", highlightthickness=1)
            self.top_bottom_frame = top_bottom_frame

            middle_bottom_frame = Frame(master, highlightbackground="green", highlightcolor="green",
                                        highlightthickness=1)
            self.middle_bottom_frame = middle_bottom_frame

            bottom_bottom_frame = Frame(master, highlightbackground="green", highlightcolor="green",
                                        highlightthickness=1)
            self.bottom_bottom_frame = bottom_bottom_frame

            # The labels and buttons are defined here.
            self.mainLabel = Label(top_frame, text="  Welcome to the Slot Machine!", fg="black",
                                   font="Helvetica 12 bold")
            self.balanceTotalOutput = Label(top_frame, text=f"Balance:   0", fg="black", font="Helvetica 13 bold")
            self.betTotalOutput = Label(top_frame, text=f"Bet: 1", fg="black", font="Helvetica 13 bold")

            # This is where the pictures are setup initially.
            self.firstWheel = Label(middle_frame, image=lemon_img)
            self.firstWheel.image = lemon_img

            self.secondWheel = Label(middle_frame, image=grape_img)
            self.secondWheel.image = grape_img

            self.thirdWheel = Label(middle_frame, image=cherry_img)
            self.thirdWheel.image = cherry_img

            # Threading needed for the "spin" affect on the spin button.
            thread = threading.Thread(target=lambda: self.spin_the_wheels(pieces, self.first_wheel.pick,
                                                                          self.second_wheel.pick, self.third_wheel.pick,
                                                                          self.customer.get_bet(),
                                                                          self.customer.get_balance()), args=())
            self.thread = thread
            self.buttonToSpinWheels = Button(top_bottom_frame, text="   Spin    ", bg="white", fg="black",
                                             font="Helvetica 11 bold", underline=3,
                                             command=lambda: self.thread_start_if_not(self.customer.get_balance(),
                                                                                      self.thread))

            self.winningsLabel = Label(top_bottom_frame, text="Last Winnings: 0 ", fg="black", font="Helvetica 12 bold")
            self.buttonToAddFunds = Button(top_bottom_frame, text=" Add Coins ", bg="white", fg="black",
                                           font="Helvetica 11 bold", underline=1,
                                           command=lambda: self.add_coins(Customer.get_balance(self.customer)))

            self.buttonToIncreaseBet = Button(middle_bottom_frame, text=" Increase Bet ", bg="white", fg="black",
                                              font="Helvetica 10 bold", underline=1,
                                              command=lambda: self.increase_bet(Customer.get_bet(self.customer),
                                                                                Customer.get_balance(self.customer)))

            self.buttonToDecreaseBet = Button(middle_bottom_frame, text=" Decrease Bet ", bg="white", fg="black",
                                              font="Helvetica 10 bold", underline=1,
                                              command=lambda: self.decrease_bet(Customer.get_bet(self.customer)))

            self.buttonMaxBet = Button(middle_bottom_frame, text="\n Max Bet \n", bg="white", fg="black", underline=2,
                                       font="Helvetica 10 bold",
                                       command=lambda: self.max_bet(Customer.get_bet(self.customer),
                                                                    Customer.get_balance(self.customer)))

            self.buttonCashOut = Button(bottom_bottom_frame, text=" Cash Out ", bg="white", fg="black",
                                        font="Helvetica 10 bold", underline=1,
                                        command=lambda: self.cash_out(Customer.get_balance(self.customer)))
            self.exitButton = Button(bottom_bottom_frame, text=" Exit ", command=master.destroy, bg="white", fg="blue",
                                     font="Helvetica 10 bold", underline=2)

            # Settings for the layout.
            self.top_frame.pack(padx=5, pady=2, fill="both", expand="yes")

            self.balanceTotalOutput.pack(side=LEFT, padx=7, pady=5)
            self.mainLabel.pack(side=LEFT, padx=7, pady=5)
            self.betTotalOutput.pack(side=LEFT, padx=7, pady=5)

            self.middle_frame.pack(padx=5, pady=5, fill="both", expand="yes")

            self.firstWheel.pack(side=LEFT, padx=(16, 5), pady=5)
            self.secondWheel.pack(side=LEFT, padx=5, pady=5)
            self.thirdWheel.pack(side=LEFT, padx=(5, 10), pady=5)

            self.top_bottom_frame.pack(padx=5, pady=2, fill="both")

            self.buttonToAddFunds.pack(side=LEFT, padx=32, pady=5)
            self.winningsLabel.pack(side=LEFT)
            self.buttonToSpinWheels.pack(side=RIGHT, padx=35, pady=5)

            self.middle_bottom_frame.pack(padx=5, pady=2, fill="both")

            self.buttonToIncreaseBet.pack(side=LEFT, padx=25, pady=5)
            self.buttonMaxBet.pack(side=LEFT, padx=25, pady=5)
            self.buttonToDecreaseBet.pack(side=LEFT, padx=25, pady=5)

            self.bottom_bottom_frame.pack(padx=5, pady=2, fill="both")

            self.buttonCashOut.pack(side=LEFT, padx=35, pady=5)
            self.exitButton.pack(side=RIGHT, padx=35, pady=5)

            # Key bindings.
            master.bind('<Alt_L><A>', lambda e: self.add_coins(Customer.get_balance(self.customer)))
            master.bind('<Alt_L><a>', lambda e: self.add_coins(Customer.get_balance(self.customer)))
            master.bind('<Alt_L><S>', lambda f: self.thread_start_if_not(Customer.get_balance(self.customer),
                                                                         self.thread))
            master.bind('<Alt_L><s>', lambda f: self.thread_start_if_not(Customer.get_balance(self.customer),
                                                                         self.thread))
            master.bind('<Alt_L><I>', lambda g: self.increase_bet(Customer.get_bet(self.customer),
                                                                  Customer.get_balance(self.customer)))
            master.bind('<Alt_L><i>', lambda g: self.increase_bet(Customer.get_bet(self.customer),
                                                                  Customer.get_balance(self.customer)))
            master.bind('<Alt_L><M>', lambda h: self.max_bet(Customer.get_bet(self.customer),
                                                             Customer.get_balance(self.customer)))
            master.bind('<Alt_L><m>', lambda h: self.max_bet(Customer.get_bet(self.customer),
                                                             Customer.get_balance(self.customer)))
            master.bind('<Alt_L><D>', lambda i: self.decrease_bet(Customer.get_bet(self.customer)))
            master.bind('<Alt_L><d>', lambda i: self.decrease_bet(Customer.get_bet(self.customer)))
            master.bind('<Alt_L><C>', lambda j: self.cash_out(Customer.get_balance(self.customer)))
            master.bind('<Alt_L><c>', lambda j: self.cash_out(Customer.get_balance(self.customer)))
            master.bind('<Alt_L><X>', lambda k: self.master.destroy())
            master.bind('<Alt_L><x>', lambda k: self.master.destroy())

        except Exception:
            messagebox.showerror("Pictures Amount", "The program was unable to find the pieces\n"
                                                    + lemon + cherry + grape)

    # Add coins function with a simpledialog box to simulate a cash input.
    # They can input any number up to 100. Max 1000.
    def add_coins(self, customer_balance):

        added_coins = simpledialog.askinteger("Input", "How many coins would you like to add?", parent=self.master,
                                              minvalue=0, maxvalue=100)
        new_customer_balance = added_coins + customer_balance
        if new_customer_balance >= 1000:
            messagebox.showerror("Max Amount", "Please cash out.\n"
                                               "This game has a limit of 1000 coins.\n"
                                               "Returning coins.")
        else:
            self.customer.set_balance(new_customer_balance)
            self.balanceTotalOutput.configure(text=f"Balance: {new_customer_balance:3}")
            self.buttonToSpinWheels.configure(state=NORMAL)

    # Cash out function to make file simulating a receipt.
    def cash_out(self, customer_balance):

        receipt = self.resource_path("assets/receipt_file.txt")

        receipt_file = open(receipt, "w+")

        messagebox.showinfo("Success", f"Printing Receipt... \n"
                                       f"Please see the cashier for your payout of: {customer_balance}")

        self.customer.set_balance(0)
        self.balanceTotalOutput.configure(text="Balance:   0")
        self.buttonToSpinWheels.configure(state=DISABLED)

        # receipt_file = open("receipt_file.txt", "w+")

        receipt_file.write("##################################################################\n"
                           "#                                                                #\n"
                           "#                                                                #\n"
                           "#       This is an official Slot machine receipt.                #\n"
                           "#                                                                #\n"
                           f"#          Payout is: {customer_balance:4}                                       #\n"
                           "#                                                                #\n"
                           "#                                                                #\n"
                           "##################################################################\n")

        os.startfile(receipt_file.name)

    # Increasing the bet by 1.
    def increase_bet(self, bet, balance):

        if balance >= bet:
            new_current_bet = bet + 1
            self.customer.set_bet(new_current_bet)
            self.betTotalOutput.configure(text=f"Bet: {self.customer.get_bet():1}")
        else:
            messagebox.showerror("Not Enough Funds", "Please Add more coins to bet.\n"
                                                     "This game has to have enough coins for the bet.\n")

    # Decreasing the bet by 1.
    def decrease_bet(self, bet):
            new_current_bet = bet - 1
            self.customer.set_bet(new_current_bet)
            self.betTotalOutput.configure(text=f"Bet: {self.customer.get_bet():1}")

    # Increasing the bet by the max 4.
    def max_bet(self, bet, balance):
        if balance >= bet:
            self.customer.set_bet(4)
            self.betTotalOutput.configure(text=f"Bet: {self.customer.get_bet():1}")
        else:
            messagebox.showerror("Not Enough Funds", "Please Add more coins to bet.\n"
                                                     "This game has to have enough coins for the bet.\n")

    # Here is where the wheel spinning occurs and the final picks are made.
    def spin_the_wheels(self, pieces, wheel_one, wheel_two, wheel_three, bet, balance):
        if balance >= bet:
            # For loop to simulate spinning.
            for run in range(1, 15):
                # Disabling the spin button until the spinning is done.
                self.buttonToSpinWheels.configure(state=DISABLED)

                # Converting them randomly to a list pick and then setting the image to it every 10 milliseconds.
                time.sleep(0.1)
                number, random_pick1 = random.choice(list(pieces.items()))
                number, random_pick2 = random.choice(list(pieces.items()))
                number, random_pick3 = random.choice(list(pieces.items()))
                self.firstWheel.configure(image=random_pick1)
                self.secondWheel.configure(image=random_pick2)
                self.thirdWheel.configure(image=random_pick3)

            # Setting the output for the final pick.
            self.firstWheel.configure(image=pieces[wheel_one])
            self.secondWheel.configure(image=pieces[wheel_two])
            self.thirdWheel.configure(image=pieces[wheel_three])

            # Calculating the winnings for the round.
            winnings = self.winnings(wheel_one, wheel_two, wheel_three, bet)
            self.winningsLabel.configure(text=f"Last Winnings: {winnings:2}")
            current_balance = winnings + self.customer.get_balance() - bet

            # Setting the customers new balance.
            self.customer.set_balance(current_balance)
            self.balanceTotalOutput.configure(text=f"Balance: {current_balance:3}")

        else:
            messagebox.showerror("Not Enough Funds", "Please Add more coins to bet.\n"
                                                     "This game has to have enough coins for the bet.\n")

        # Starting a new thread for the next spin and configuring the buttons and key bindings
        #  to use the new thread.

        new_thread = threading.Thread(target=lambda: self.spin_the_wheels(pieces,
                                                                          self.first_wheel.spin(),
                                                                          self.second_wheel.spin(),
                                                                          self.third_wheel.spin(),
                                                                          self.customer.get_bet(),
                                                                          self.customer.get_balance()))
        new_thread = new_thread
        self.buttonToSpinWheels.configure(state=NORMAL,
                                          command=lambda: self.thread_start_if_not(self.customer.get_balance(), new_thread))
        self.master.bind('<Alt_L><S>', lambda f: self.thread_start_if_not(self.customer.get_balance(), new_thread))
        self.master.bind('<Alt_L><s>', lambda f: self.thread_start_if_not(self.customer.get_balance(), new_thread))

    # Static method that does a thread start check along with min and max balance checks.
    def thread_start_if_not(self, customer_balance, thread):

        if customer_balance >= 1000:
            messagebox.showerror("Max Amount", "Please cash out.\n"
                                               "This game has a limit of 1000 coins.")

        elif not customer_balance >= 0 and thread.is_alive():
            thread.join(1)
            messagebox.showerror("Error", "Please insert coins.\n"
                                          "This game needs coins to play.")

        elif not thread.is_alive() and customer_balance > 0:
            thread.start()

        else:
            messagebox.showerror("Error", "Please insert coins.\n"
                                          "This game needs coins to play.")

    # Function to calculate the winnings.
    @staticmethod
    def winnings(wheel_one, wheel_two, wheel_three, bet):

        combo = int(f"{wheel_one}{wheel_two}{wheel_three}")
        winning_combos = {111: 10, 222: 7, 333: 5,
                          112: 3, 113: 3, 121: 3, 131: 3, 211: 3, 311: 3,
                          221: 1, 223: 1, 212: 1, 232: 1, 122: 1, 322: 1}

        print(bet)
        print(combo)
        if combo in winning_combos:
            print(winning_combos[combo])
            multiplier = int(winning_combos[combo])
            winnings = bet * multiplier
            print(winnings)
            return winnings
        else:
            return 0

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


# Initializing the GUI class and keeping it open.
root = Tk()
slot_machine_gui = SlotMachineGUI(root)
root.mainloop()
