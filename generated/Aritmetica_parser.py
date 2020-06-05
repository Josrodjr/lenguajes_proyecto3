#parser for Aritmetica_parser grammar

import scanner

class Parser:

	class Token(object):
		kind = 0
		val = 0

	t = Token()
	la = Token()
	Scanner = scanner.Scanner()
	def first(self, n):
		pass
	def follow(self, n):
		pass
	def getNumber(self):
		return int(self.t.val)

	def __init__(self):
		setattr(self.t, 'val', 'kind' )
		setattr(self.la, 'val', 'kind' )

	def Number(self):
		if self.t.kind == self.Scanner.number:
			result = self.t
		result = self.getNumber()
		return result

	def Factor(self):
		signo = 1
		if self.t.val == '-':
			signo = -1
		if self.la in self.first('Number'):
			result = self.Number()
		if self.la in self.first('Expression'):
			result = self.Expression()
		result *= signo
		return result

	def Term(self):
		result1, result2 = 1, 1
		result = self.Factor()
		while self.t.val == '*':
			result2 = self.Factor()
			result1 *= result2
		while self.t.val == '/':
			result2 = self.Factor()
			result1 /= result2
		result = result1
		return result

	def Expression(self):
		result1, result2 = 0, 0
		result = self.Term()
		while self.t.val == '+':
			result2 = self.Term()
			result1 += result2
		while self.t.val == '-':
			result2 = self.Term()
			result1 -= result2
		result = result1
		return result

	def Stat (self):
		value = 0
		result = self.Expression()
		print(str(value))
		return result

	def Expr(self):
		if self.la in self.first('Stat'):
			result = self.Stat()
		return result

test = Parser()

print(test.t.val)