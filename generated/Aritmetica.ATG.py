#parser for Aritmetica.ATG grammar

class Parser:

	t, la = 0, 0
	def __init__(self):
		self.t = 1
		self.la = 2

	def Number(self):
		if self.t.kind == self.Scanner.number:
			result = self.t
		result = self.getNumber()

	def Factor(self):
		signo = 1
		result = self.Number(self):
		result = self.Expression(self):
		result *= signo

	def Term(self):
		result1, result2 = 1, 1
		result = result1

	def Expression(self):
		result1, result2 = 0, 0
		result = result1

	def Stat (self):
		value = 0
		print(str(value))

	def Expr(self):

