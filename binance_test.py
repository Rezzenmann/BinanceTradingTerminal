from binance_api import Binance
from config_api import API_key, API_sec 

bot = Binance(
	API_KEY = API_key,
	API_SECRET = API_sec)


class BinanceBalance:
		#вызов метода с binance_api.py

		def showbalance(self): 
			a = ('account', bot.account())
			your_balance = []

		#обрабатываю json файл, иду по элемнтам баланса

			for elem in a[1]['balances']:
				for i in elem:
					if elem['free'] != '0.00000000':
						your_balance.append((elem['asset'], elem['free']))
						break

			print("--------YOUR FREE BINANCE BALANCE---------\n")
			#вывожу данные в нормальном виде
			for elem in your_balance:
				for i in elem:
					print(i)
					

class MakeOrder:

	#LIMIT                         timeInForce, quantity, price
	#MARKET                        quantity

		
	def __init__(self, symbol, order_type, side, quantity):
		self.symbol = symbol
		self.type = order_type
		self.side = side
		self.quantity = quantity
		
		if self.type == 1:

			print("You chosed: Trading Pair {}, Order Type LIMIT, Side {}, Quantity {}".format(self.symbol, self.side, self.quantity))
			price = float(input("Price\n>>>"))
			try:
				limit = bot.createOrder(
				symbol=self.symbol,
				recvWindow=5000,
				side=self.side,
				type='LIMIT',
				timeInForce='GTC',
				quantity=self.quantity,
				price=price)
				
							
				print('You have placed a limit order. Side > {}. Pair > {}. Price > {}. Quantity > {}. OrderId > {}'.format(limit['side'], limit['symbol'], 
				limit['price'], limit['origQty'], limit['orderId']))
			
			except:
				print("Error Ocurred")

		if self.type == 2:
			print("You chosed: Trading Pair {}, Order Type MARKET, Side {}, Quantity {}".format(self.symbol,  self.side, self.quantity))
			try:
				market = bot.createOrder(
					symbol=self.symbol,
					recvWindow=5000,
					side=self.side,
					type='MARKET',
					quantity=self.quantity)

				print('MARKET Order was succesfully placed. Side > {}. Pair > {}. Price > {}. Quantity > {}. OrderId > {}'.format(market['side'], market['symbol'], 
				market['price'], market['origQty'], market['orderId']))
			except:
				print("Error Ocurred")


class GetOrdersInfo:
	#Инфа по всем текущим ордерам.

	def info(self):
		print('\n----------OPENED POSITIONS----------\n')
		a = bot.openOrders()
		if len(a) == 0:
			print("\nCheking......\nYou don`t have open orders.\n")
		if len(a) >= 1:
			for elem in range(len(a)):
				print('\nYou have open order for the pair > {}. Side > {}. Price > {}. Quantity > {}. OrderId > {}'.format(a[elem]['symbol'], 
					a[elem]['side'], a[elem]['price'], a[elem]['origQty'], a[elem]['orderId']))


class DeletingOrder(GetOrdersInfo):
	#Сперва вызывает родительский метод Инфо и печатает инфу по текущим ордерам
	#Спрашивает торг пару для удаления и айди ключ ордера, который указан в выводе метода Инфо

	def __init__(self, symbol):
		super().info()
		try:
			def deleting(self,symbol, orderId):
				print()
				bot.cancelOrder(
				orderId=orderId,
				symbol= symbol)
		except:
			print("\nError Ocurred")
		else:
			print("\nYou have succesfully deleted this order!")
				

def main():

	print("\n\n----------BINANCE TRADING TERMINAL BY RMANN------------\n\n")
	print("What do you want to do:\n 1. Get my balance \n 2. Place an order \n 3. Get info about placed orders \n 4. Delete order \n 5. Exit\n")
	try:
		user_answer = int(input("\nWrite the number of the option >>> "))

		if user_answer == 1:

			print("\nYou`ve chosen the option #1...\nPreparing your balance!\n")
			balance_user = BinanceBalance()
			balance_user.showbalance()


		if user_answer == 2:

			print("\nYou`ve chosen the option #2...\nPreparing to place orders!\n")
			order_user = MakeOrder(input("Trading Pair (e.g. BTCUSDT)\n>>>"),int(input("Order Type( write the number):\n1.LIMIT\n2.MARKET\n3.STOP LOSS LIMIT\n4.TAKE PROFIT LIMIT\n>>>")),input("SELL/BUY\n>>>"),float(input("Quantity\n>>>")))
			

		if user_answer == 3:

			print("\nYou`ve chosen the option #3...\nPreparing your orders!\n")
			info_order = GetOrdersInfo()
			info_order.info()
		

		if user_answer == 4:

			print("\nYou`ve chosen the option #4...\nPreparing your orders!\n")
			delete_order = DeletingOrder(input("Input the Trading Pair to get info\n>>> "))
			
			delete_order.deleting(input("\nPlease write the Trading Pair order to delete it >>>"), 
				int(input("\nConfirm the action by writing the 'OrderId'(you may find it upper)>>>")))

		if user_answer == 5:

			raise KeyboardInterrupt

	except ValueError as v:
		print("\nPlease enter only integer numbers! Closing....")
	except KeyboardInterrupt:
		print()
		print('\nShutting down, bye!')



if __name__ == '__main__':
	main()
