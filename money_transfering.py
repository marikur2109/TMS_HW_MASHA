class Money:
    def __init__(self, amount, cents, currency):
        self.amount = amount
        self.cents = cents
        self.currency = currency

    @property
    def coins(self):
        return self.cents

    @coins.setter
    def coins(self, cents):
        if 0 < cents < 100:
            self.cents = cents
        else:
            print('Недопустимое количество coins')

    def money_print(self):
        print(f'{self.amount},{self.cents} {self.currency}')

    def money_to_cents(self, amount=None, cents=None):
        if amount is None and cents is None:
            return self.amount * 100 + self.cents
        else:
            return amount * 100 + cents

    @classmethod
    def from_cents(cls, cents, currency):
        amount = cents // 100
        fractional = cents % 100
        return cls(amount, fractional, currency)


    def add(self, amount, cents, currency):
        if self.currency != currency:
            print('Валюты не совпадают')
            return

        total_cents = self.money_to_cents() + self.money_to_cents(amount, cents)
        self.amount = total_cents // 100
        self.cents = total_cents % 100

    def subtract(self, amount, cents, currency):
        if self.currency != currency:
            print('Валюты не совпадают')
            return

        total_cents = self.money_to_cents() - self.money_to_cents(amount, cents)

        if total_cents < 0:
            print('Недостаточно средств')
            return

        self.amount = total_cents // 100
        self.cents = total_cents % 100

    def multiply(self, float_amount):
        total_cents = self.money_to_cents() * float_amount
        self.amount = int(total_cents // 100)
        self.cents = int(total_cents % 100)

    def divide(self, float_amount):
        total_cents = self.money_to_cents() / float_amount
        self.amount = int(total_cents // 100)
        self.cents = int(total_cents % 100)

    def compare(self, amount, cents, currency):
        if self.currency != currency:
            print('валюты не совпадают')
        else:
            if (self.amount > amount):
                print(f'У меня больше!')
            elif (self.amount == amount):
                if (self.cents > cents):
                    print(f'У меня больше!')
                elif (self.cents == cents):
                    print(f'У нас одинаково!')
                else:
                    print(f'У тебя больше!')



class Bank_account(Money):

    all_accounts = []

    def __init__(self,account_name, amount, cents, currency):
        super().__init__(amount, cents, currency)
        self.account_name = account_name
        Bank_account.all_accounts.append(self)

    def money_print(self):
        print(f'Счет "{self.account_name}": {self.amount},{self.cents:02d} {self.currency}')

    @classmethod
    def show_all_accounts(cls):
        if not cls.all_accounts:
            print("Нет созданных счетов")
            return

        print(f"Все счета")
        for i, account in enumerate(cls.all_accounts, 1):
            print(f"{i}. ", end='')
            account.money_print()


    def convert_acc_currency(self, converter, to_currency):
        new_money = converter.convert(self, to_currency)
        self.amount = new_money.amount
        self.cents = new_money.cents
        self.currency = new_money.currency
        print(f"счет '{self.account_name}' конвертирован в {to_currency}")

    def transfer_money(self, account_to, amount, cents, converter):

        self_cents = self.money_to_cents()
        transfer_cents = self.money_to_cents(amount, cents)

        if self_cents < transfer_cents:
            print("Недостаточно средств для перевода")
            return False

        self.subtract(amount, cents, self.currency)

        temp_money = Money(amount, cents, self.currency)
        converted = converter.convert(temp_money, account_to.currency)

        account_to.add(converted.amount, converted.cents, account_to.currency)
        print(f"\nПереведено c  '{self.account_name}' на '{account_to.account_name}'"
              f" {amount},{cents:02d} {self.currency} -> "
              f"{converted.amount},{converted.cents:02d} {account_to.currency}")
        return True


class Currency_converter:
    def __init__(self):
        self.rates = {}

    def set_rate(self, from_currency, to_currency, rate):
        key = f'{from_currency}-{to_currency}'
        self.rates[key] = rate

    def get_rate(self, from_currency, to_currency):
        if from_currency == to_currency:
            return 1

        key = f'{from_currency}-{to_currency}'
        if key in self.rates:
            return self.rates[key]
        else:
            print(f"Нет курса {from_currency} -> {to_currency}")

    def convert(self, money, to_currency):
        rate = self.get_rate(money.currency, to_currency)
        in_cents = money.money_to_cents()
        new_cents = round(in_cents * rate)
        return Money.from_cents(new_cents, to_currency)




# money = Money(amount=45, cents=15, currency='USD')
# money.money_print()
#
# money.add(amount=105, cents=97, currency='USD')
# money.money_print()
#
# money.subtract(amount=105, cents=97, currency='USD')
# money.money_print()
#
# money.multiply(float_amount=2.22)
# money.money_print()
#
# money.divide(float_amount=2.22)
# money.money_print()

acc1 = Bank_account("Счет в рублях", 1000, 0, "BYN")
acc2 = Bank_account("Счет в долларах", 500, 0, "USD")
acc3 = Bank_account("Счет в евро", 300, 0, "EUR")
acc4 = Bank_account("Накопительный в рублях", 5000, 50, "BYN")

Bank_account.show_all_accounts()

conv = Currency_converter()
conv.set_rate("USD", "BYN", 2.8)
conv.set_rate("BYN", "USD", 0.36)
conv.set_rate("EUR", "BYN", 3.28)
conv.set_rate("EUR", "USD", 1.17)
conv.set_rate("USD", "EUR", 0.85)

acc1.transfer_money(acc2, 250, 0, conv)

print("\nПосле перевода:")
Bank_account.show_all_accounts()

acc2.transfer_money(acc4, 200, 0, conv)

print("\nПосле перевода:")
Bank_account.show_all_accounts()
