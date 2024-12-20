from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle
from kivy.metrics import dp
from BankDatabase import BankDatabase
from functools import partial
from helper import helper
import csv


Builder.load_file("kivy_files/account_page.kv")
Builder.load_file("kivy_files/accounts_page.kv")
Builder.load_file("kivy_files/checks_page.kv")
Builder.load_file("kivy_files/fico_page.kv")
Builder.load_file("kivy_files/investments_page.kv")
Builder.load_file("kivy_files/loans_page.kv")
Builder.load_file("kivy_files/login_page.kv")
Builder.load_file("kivy_files/main_page.kv")
Builder.load_file("kivy_files/more_payments_page.kv")
Builder.load_file("kivy_files/pay_page.kv")
Builder.load_file("kivy_files/rewards_page.kv")
Builder.load_file("kivy_files/settings_page.kv")



class SharedData:
    def __init__(self):
        self.bank_database = BankDatabase()
        self.fullName = "test"
        self.accountType = ""


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        

    def get_fullName(self):
        return self.app.sharedData.fullName

    def get_login_button(self, username, password):
        # Checks the username/password with database
        if self.app.sharedData.bank_database.check_login(username, password):
            # sets the fullName and accountType to the sharedData class instance
            self.app.sharedData.fullName = self.app.sharedData.bank_database.get_name()
            self.app.sharedData.accountType = self.app.sharedData.bank_database.get_account_type()
            # sets current screen to home screen
            self.manager.current = "home"
            

        else:
            # shows error message for 10 seconds
            self.ids.error_message.opacity = 1
            Clock.schedule_once(lambda dt: setattr(self.ids.error_message, "opacity", 0), 10)

    

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_enter(self):
        self.ids.welcome_label.text = "Welcome " + self.app.sharedData.fullName
        self.ids.checkings_amount.text = self.app.sharedData.bank_database.get_amount("Checkings")
        self.ids.savings_amount.text = self.app.sharedData.bank_database.get_amount("Savings")
        self.ids.mma_amount.text = self.app.sharedData.bank_database.get_amount("MMA")
        self.app.sharedData.bank_database.view_account()
        

    def get_fullName(self):
        return self.app.sharedData.fullName

    def accounts_button(self):
        print("Accounts button pressed")
        self.manager.current = "accounts"
        return
    
    def pay_button(self):
        self.manager.current = "pay"
        return
    
    def checks_button(self):
        self.manager.current = "checks"
        return
    
    def investments_button(self):
        self.manager.current = "investments"
        return

    def fico_button(self):
        self.manager.current = "fico"
        return
    
    def rewards_button(self):
        self.manager.current = "rewards"
        return
    
    def loans_button(self):
        self.manager.current = "loans"
        return
    
    def notifications_button(self):
        return

    def settings_button(self):
        self.manager.current = "settings"
        return
        
    def logout_button(self):
        print("logout button pressed")
        self.manager.current = "login"
        return
        
class AccountsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app() # current instance of running app, so I can set/grab variables from other screens

    def on_enter(self):
        self.ids.accounts_section.clear_widgets()
        grid = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(10),
            padding=dp(10)
        )
        # grabs the accounts of the current user
        accounts = self.app.sharedData.bank_database.get_accounts()

        # swaps to the account Page based on which account button was pressed
        def switch_to_account_page(accountNum, instance):
            self.app.currAccount = accountNum
            self.manager.current = "account"
            print('Swap to account: ', accountNum)
            return
        
        # loops through all the accounts and adds a button for each one.
        for i in range(len(accounts)):
            account = accounts[i]
            button = Button(
                text=f'{account[3]} Account\n${account[5]}', 
                font_size = "16sp",
                size_hint_x=1,
                size_hint_y=None,
                height=dp(80),
                background_color=(0,0,0,0),
                halign="center",
                valign="middle",
                text_size=(None,None),
                on_press=partial(switch_to_account_page, account[0])
                )
            def update_canvas(instance, value):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    Color(0.2,0.5,0.8,1)
                    RoundedRectangle(
                        pos=instance.pos,
                        size=instance.size,
                        radius=[30]
                    )
                    Color(18/255,44/255,70/255,0.94)
                    Line(
                        width=2.35,
                        rounded_rectangle=(instance.x,instance.y,instance.width,instance.height,30)
                    )
            
            button.bind(size=update_canvas)
            button.bind(pos=update_canvas)
            grid.add_widget(button)
        def on_grid_size(instance, value):
            grid.height = grid.minimum_height

        grid.bind(size=on_grid_size)
        self.ids.accounts_section.add_widget(grid)
        self.entry = True

    # back button def
    def back_button(self):
        self.manager.current = "home"


# This class is pretty much the same, functionally, as AccountsScreen, but swapping accounts for transactions and obviously displays different info
class AccountScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()


    def on_enter(self):
        self.ids.transaction_section.clear_widgets()
        grid = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=dp(10),
            padding=dp(10)
        )
        transactions = self.app.sharedData.bank_database.get_transactions(self.app.currAccount)
        print(transactions)
        for i in range(len(transactions)):
            transaction = transactions[i]
            button = Button(
                text=f'${transaction[4]}\n{transaction[3]} on {transaction[5].strftime("%Y-%m-%d, %H:%M")} at "{transaction[7]}" in {transaction[9]}\nStatus: {transaction[6]} | Description: {transaction[8]}', 
                font_size = "16sp",
                size_hint_x=1,
                size_hint_y=None,
                height=dp(80),
                background_color=(0,0,0,0),
                halign="center",
                valign="middle",
                text_size=(None,None)
                )
            def update_canvas(instance,value):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    Color(0.2,0.5,0.8,1)
                    RoundedRectangle(
                        pos=instance.pos,
                        size=instance.size,
                        radius=[30]
                    )
                    Color(18/255,44/255,70/255,0.94)
                    Line(
                        width=2.35,
                        rounded_rectangle=(instance.x,instance.y,instance.width,instance.height,30)
                    )
            
            button.bind(size=update_canvas)
            button.bind(pos=update_canvas)
            grid.add_widget(button)
        def on_grid_size(instance, value):
            grid.height = grid.minimum_height

        grid.bind(size=on_grid_size)
        

        self.ids.transaction_section.add_widget(grid)
        self.entry = True

        
    
    def back_button(self):
        self.manager.current = "accounts"
    def update_rect(self, instance, value):
        # Update the rectangle's size and position when the layout is resized or moved
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        return
    def delete_account(self):
        content = BoxLayout(orientation='vertical', padding=10)
        with content.canvas.before:
            Color(100/255, 100/255, 154/255, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)
        content.bind(size=self.update_rect, pos=self.update_rect)
        label = Label(
            text = "Are you sure you want to delete this account?",
            halign="center",
            valign="middle",
            size_hint_y=0.4,
            height=20,
            line_height=0.5,
            font_size="20sp",
            bold=True,
            text_size=(None,None)
        )
        content.add_widget(label)
        grid_layout = GridLayout(cols = 2, size_hint_y=None, spacing=10, padding=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        yes_button = Button(
            text = 'Yes',
            size_hint_y= None,
            height = 50,
            orientation='vertical',
            padding=10,
            background_color=(0,0,0,0),
            text_size=(None,None)
        )
        no_button = Button(
            text = 'No',
            size_hint_y= None,
            height = 50,
            orientation='vertical',
            padding=10,
            background_color=(0,0,0,0),
            text_size=(None,None)
        )
        def update_canvas(instance, value):
            instance.canvas.before.clear()  # Clear previous canvas elements
            with instance.canvas.before:
                # Draw the background as a rounded rectangle
                Color(0.2, 0.5, 0.8, 1)  # Background color
                RoundedRectangle(pos=instance.pos, size=instance.size, radius=[20])

                # Draw the border as a rounded rectangle with Line
                Color(18/255, 44/255, 70/255, 0.94)  # Border color
                Line(width=2.35, rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 20))
        error_label = Label(
                text = '',
                halign="center",
                valign="middle",
                padding=[10,10],
                size_hint_y=None,
                height=40,
                color=(1,0,0,1),
                line_height=0.5,
                font_size="15sp",
                opacity=0,
                text_size=(None,None)
            )
        def yes_button_press():
            if self.app.sharedData.bank_database.delete_curr_account(self.app.currAccount):
                popup.dismiss()
                self.manager.current = 'home'
            else:
                error_label.text = 'Account must have a balance of $0.00 to be deleted.'
                error_label.opacity = 1
                Clock.schedule_once(lambda dt: setattr(error_label, "opacity", 0), 6)
                return
        def no_button_press():
            popup.dismiss()
            return
        yes_button.bind(pos=update_canvas, size=update_canvas)
        yes_button.bind(on_press=lambda instance: yes_button_press())
        no_button.bind(pos=update_canvas, size=update_canvas)
        no_button.bind(on_press=lambda instance: no_button_press())
        grid_layout.add_widget(yes_button)
        grid_layout.add_widget(no_button)
        def on_grid_size(isntance,value):
            grid_layout.height = grid_layout.minimum_height
        grid_layout.bind(size=on_grid_size)
        content.add_widget(grid_layout)
        content.add_widget(error_label)
        popup = Popup(title='', content=content, size_hint=(0.7, 0.8), background_color=(1, 1, 1, 0), auto_dismiss=False)
        popup.open()
        return
    
    # 7. Generate reports that can be exported (excel or csv format)
    # Generates an extended transaction history of the user and exports it as a csv
    def download_transaction_history(self):
        transactions = self.app.sharedData.bank_database.get_transaction_history()
        headers = ["userID", "fullName", "email", "accountNumber", "accountType", "cardNumber", "cardType", "transactionID", "transactionType", "amount", "transactionDate", "transactionStatus"]
        transaction_dicts = []
        for transaction in transactions:
            transaction_dict = {
                # not displaying userID for security reasons
                "fullName": transaction[1],
                "email": transaction[2],
                "accountNumber": transaction[3],
                "accountType": transaction[4],
                "cardNumber": transaction[5],
                "cardType": transaction[6],
                "transactionID": transaction[7],
                "transactionType": transaction[8],
                "amount": transaction[9],
                "transactionDate": transaction[10].strftime("%Y-%m-%d %H:%M:%S"),
                "transactionStatus": transaction[11]
            }
            transaction_dicts.append(transaction_dict)
        
        with open("transaction_history.csv", mode='w', newline='') as file:
            writer = csv.DictWriter(file,fieldnames=headers)
            writer.writeheader()
            writer.writerows(transaction_dicts)

    

class ChecksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def back_button(self):
        self.manager.current = "home"
class FicoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def back_button(self):
        self.manager.current = "home"
class InvestmentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def back_button(self):
        self.manager.current = "home"
class LoansScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def back_button(self):
        self.manager.current = "home"
class PayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def on_enter(self):
        statements = self.app.sharedData.bank_database.get_statements(2)
        statement = statements[0]
        self.ids.first_recent.text = f'''Statement for {statement[12][-4:]} | Status: {statement[11]}\n
        Amount Due: ${statement[8]} | Minimum: ${statement[10]} | Interest: {statement[9] if statement[9] != 0 else "No interest"}%'''
        self.ids.first_recent_second.text = f'Period Start: {statement[4]}, Period End: {statement[5]}, Issue Date: {statement[6]}, Due Date: {statement[7]}'
        if len(statements) > 1:
            statement = statements[1]
            self.ids.second_recent.text = f'''Statement for {statement[12][-4:]} | Status: {statement[11]}\n
            Amount Due: ${statement[8]} | Minimum: ${statement[10]} | Interest: {statement[9] if statement[9] != 0 else "No interest"}%'''
            self.ids.second_recent_second.text = f'Period Start: {statement[4]}, Period End: {statement[5]}, Issue Date: {statement[6]}, Due Date: {statement[7]}'
        return

    def pay_bills(self):
        content = BoxLayout(orientation='vertical', padding=10)
        with content.canvas.before:
            Color(100/255, 100/255, 154/255, 1)
            self.rect = Rectangle(size=content.size, pos=content.pos)

        # Update rectangle size and position when the layout changes
        content.bind(size=self.update_rect, pos=self.update_rect)

        grid_layout = GridLayout(cols=5, size_hint_y=None,spacing=10, padding=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        close_button = Button(text="Close",col=1,size_hint_y=0.5, size_hint_x=0.7, height="5sp",background_color=(0,0,0,0))
        total_money = self.app.sharedData.bank_database.total_money_owed()
        total_label = Label(text=f"Total Money Owed: ${total_money}",halign="center",valign="middle",padding=[10,10],size_hint_y=None,height=20,line_height=0.5,font_size="15sp",bold=True,text_size=(None,None))
        def update_canvas(instance, value):
            instance.canvas.before.clear()  # Clear previous canvas elements
            with instance.canvas.before:
                # Draw the background as a rounded rectangle
                Color(0.5, 0.5, 0.6, 1)  # Background color
                RoundedRectangle(pos=instance.pos, size=instance.size, radius=[20])

                # Draw the border as a rounded rectangle with Line
                Color(18/255, 44/255, 70/255, 0.94)  # Border color
                Line(width=2.35, rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 20))

        # Bind the button's position and size to update the canvas when changed
        close_button.bind(pos=update_canvas)
        close_button.bind(size=update_canvas)
        close_button.bind(on_press=lambda instance: popup.dismiss())
        grid_layout.add_widget(close_button)
        blank_widget = Widget(size_hint_y=None)
        grid_layout.add_widget(blank_widget)
        grid_layout.add_widget(total_label)
        blank_widget = Widget(size_hint_y=None)
        grid_layout.add_widget(blank_widget)
        blank_widget = Widget(size_hint_y=None)
        grid_layout.add_widget(blank_widget)
        content.add_widget(grid_layout)
        statements_not_paid = self.app.sharedData.bank_database.get_notPaid_statements()
        print(statements_not_paid)
        # Create the body section with a label
        scroll_view = ScrollView(size_hint=(1, 0.9))
        grid_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        def on_grid_size(isntance,value):
            grid_layout.height = grid_layout.minimum_height
        def pay_bill(statementNum, instance):
            statement = statements_not_paid[statementNum]
            grid_layout.clear_widgets()
            blank_widget = Widget(size_hint_y=None, height=20)
            grid_layout.add_widget(blank_widget)
            label1 = Label(
                text = f'''Statement for "...{statement[12][-4:]}"\n
            Status: {statement[11]}     \n
            Amount Due: ${statement[8]} | Minimum: ${statement[10]}\n
            Interest: {statement[9] if statement[9] != 0 else "No interest"}% if not paid before {statement[7]}
                ''',
                halign="center",
                valign="middle",
                padding=[10,10],
                size_hint_y=None,
                height=150,
                line_height=0.5,
                font_size="15sp",
                bold=True,
                text_size=(None,None)
            )
            grid_layout.add_widget(label1)
            accounts = self.app.sharedData.bank_database.get_accounts_checkings_savings()
            print(accounts)
            account_number = TextInput(
                hint_text=f"Enter your account Number. Your accounts: {', '.join(str(item[0]) for item in accounts)}",
                multiline=False,
                height=50,
                size_hint_y=None,
                input_filter='int'
            )
            grid_layout.add_widget(account_number)
            amount_input = TextInput(
                hint_text="Enter amount you want to pay", 
                multiline=False,
                height=50,
                size_hint_y=None,
                input_filter='float'
                )

            grid_layout.add_widget(amount_input)
            label2 = Label(
                text = f'''Details:\n
                Period Start: {statement[4]} | Period End: {statement[5]}\n
                Issued: {statement[6]}
                ''',
                halign="center",
                valign="middle",
                padding=[10,10],
                size_hint_y=None,
                height=150,
                line_height=0.5,
                font_size="15sp",
                text_size=(None,None)
            )
            grid_layout.add_widget(label2)
            error_label = Label(
                text = '',
                halign="center",
                valign="middle",
                padding=[10,10],
                size_hint_y=None,
                height=40,
                color=(1,0,0,1),
                line_height=0.5,
                font_size="15sp",
                opacity=0,
                text_size=(None,None)
            )

            def enter_payment():
                amount = amount_input.text
                amount = helper.convert(amount)
                accountNumber = account_number.text
                accountNumber = helper.convert(accountNumber)
                # if entered amount is less than statement minimum
                if amount < statement[10]:
                    error_label.text = f'Must be above minimum, ${statement[10]}'
                    error_label.opacity = 1
                    Clock.schedule_once(lambda dt: setattr(error_label, "opacity", 0), 6)
                # if entered amount is more than total statement amount
                elif amount > statement[8]:
                    error_label.text = f'Must be below total statement amount, ${statement[8]}'
                    error_label.opacity = 1
                    Clock.schedule_once(lambda dt: setattr(error_label, "opacity", 0), 6)
                elif accountNumber not in accounts[0]:
                    error_label.text = f'Must be a valid account Number'
                    error_label.opacity = 1
                    Clock.schedule_once(lambda dt: setattr(error_label, "opacity", 0), 6)
                else:
                    print('Entered payment')
                    self.app.sharedData.bank_database.update_statement(statement, statement[8], amount, accountNumber)
                    popup.dismiss()
                    

                
                return
            enter_button = Button(
                text="Enter",
                size_hint_y= None,
                height = 50,
                orientation='vertical',
                padding=10,
                background_color=(0,0,0,0),
                text_size=(None,None)
            )
            def update_canvas(instance, value):
                instance.canvas.before.clear()  # Clear previous canvas elements
                with instance.canvas.before:
                    # Draw the background as a rounded rectangle
                    Color(0.2, 0.5, 0.8, 1)  # Background color
                    RoundedRectangle(pos=instance.pos, size=instance.size, radius=[20])

                    # Draw the border as a rounded rectangle with Line
                    Color(18/255, 44/255, 70/255, 0.94)  # Border color
                    Line(width=2.35, rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 20))
            enter_button.bind(pos=update_canvas)
            enter_button.bind(size=update_canvas)
            enter_button.bind(on_press=lambda instance: enter_payment())
            grid_layout.add_widget(enter_button)
            grid_layout.add_widget(error_label)
            

            grid_layout.bind(size=on_grid_size)

            return
        
        for i in range(len(statements_not_paid)):
            statement = statements_not_paid[i]
            box = BoxLayout(
                orientation='vertical',
                size_hint_x=1,
                size_hint_y=None,
                height=dp(80)
            )

            button = Button(
                text = f'''Statement for "...{statement[12][-4:]}" | Status: {statement[11]}\n
                Amount Due: ${statement[8]} | Minimum: ${statement[10]} | Interest: {statement[9] if statement[9] != 0 else "No interest"}%
                ''',
                line_height=0.7,
                font_size="16sp",
                background_color=(0,0,0,0),
                halign="center",
                valign="middle",
                size_hint=(1,1),
                text_size=(None,None),
                on_press=partial(pay_bill, i)
            )
            box.add_widget(button)
            def update_canvas(instance, value):
                instance.canvas.before.clear()
                with instance.canvas.before:
                    Color(0.2, 0.5, 0.8, 1)
                    RoundedRectangle(
                        pos=instance.pos,
                        size=instance.size,
                        radius=[30]
                    )
                    # Border color
                    Color(18/255, 44/255, 70/255, 0.94)
                    Line(
                        width=2.35,
                        rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 30)
                    )
            box.bind(size=update_canvas, pos=update_canvas)
            grid_layout.add_widget(box)

        

        grid_layout.bind(size=on_grid_size)
        scroll_view.add_widget(grid_layout)
        content.add_widget(scroll_view)

        popup = Popup(title='', content=content, size_hint=(0.7, 0.8), background_color=(1, 1, 1, 0), auto_dismiss=False)
        popup.open()
        return

    def update_rect(self, instance, value):
        # Update the rectangle's size and position when the layout is resized or moved
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        return
    
    def download_statement_history(self):
        statements = self.app.sharedData.bank_database.get_statement_history()
        headers = ["userID", "fullName", "accountNumber", "accountType", "cardNumber", "cardType", "totalSpent", "totalDue", "dueDate", "statementStatus"]
        statement_dicts = []
        for statement in statements:
            statement_dict = {
                "userID": statement[0],
                "fullName": statement[1],
                "accountNumber": statement[2],
                "accountType": statement[3],
                "cardNumber": statement[4],
                "cardType": statement[5],
                "totalSpent": statement[6],
                "totalDue": statement[7],
                "dueDate": statement[8].strftime("%Y-%m-%d"),  # Convert datetime to string
                "statementStatus": statement[9]
            }
            statement_dicts.append(statement_dict)


        with open("statement_history.csv", mode='w', newline='') as file:
            writer = csv.DictWriter(file,fieldnames=headers)
            writer.writeheader()
            writer.writerows(statement_dicts)
        return

    def transfer_money(self):
        print("Transfer Money Button Pressed")
        return
    
    def pay_person(self):
        print("Pay Person Button Pressed")
        return
    
    def more_payments(self):
        print("More payments button pressed")
        self.manager.current = "payments"
        return
    
    def back_button(self):
        self.manager.current = "home"
        return

class MorePaymentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def back_button(self):
        self.manager.current = "home"

class RewardsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def back_button(self):
        self.manager.current = "home"
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def back_button(self):
        self.manager.current = "home"




class BankApp(App):

    sharedData = SharedData()
    
    def build(self):
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AccountsScreen(name='accounts'))
        sm.add_widget(ChecksScreen(name='checks'))
        sm.add_widget(FicoScreen(name='fico'))
        sm.add_widget(InvestmentsScreen(name='investments'))
        sm.add_widget(LoansScreen(name='loans'))
        sm.add_widget(PayScreen(name='pay'))
        sm.add_widget(RewardsScreen(name='rewards'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(AccountScreen(name='account'))
        sm.add_widget(MorePaymentsScreen(name='payments'))
        return sm