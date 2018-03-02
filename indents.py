class Indents(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.indent_stack = [0]
		self.token_queue = []
		self.eof = False

	def token(self):
		if len(self.token_queue) > 0:
			token = self.token_queue[-1]
			self.token_queue = self.token_queue[0:-1]
			return token

		if self.eof:
			return None

		token = self.lexer.token()

		if token is None:
			self.eof = true

			if len(self.indent_stack) > 1:
				token = ('DEDENT', None)

				for i in range(len(self.indent_stack) - 1):
					self.token_queue.append(token)

				self.indent_stack=[0]

		elif token.type == 'NEW_LINE':

			if token.value > self.indent_stack[-1]:
				self.indent_stack.append(token.value)
				self.token_queue.append(('INDENT', None))

			else:

				while token.value < self.indent_stack[-1]:
					self.indent_stack = self.indent_stack[0:-1]
					self.token_queue.append(('DEDENT', None))

				if token.value != self.indent_stack[-1]:
					print("Indent Error")
					sys.exit()
					
		return token
