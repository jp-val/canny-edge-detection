class Node:
	def __init__(self, data):
		self.data = data
		self.next = None

class Stack:
	def __init__(self):
		self.top = None
		self.size = 0

	def push(self, data):
		new_node = Node(data)
		
		if self.top == None:
			self.top = new_node
		else:
			new_node.next = self.top
			self.top = new_node
		
		self.size += 1

	def peek(self):
		if self.top == None:
			return None
		else:
			return self.top.data

	def pop(self):
		if self.top == None:
			return None

		ex_top_node = self.top
		self.top = self.top.next
		retval = ex_top_node.data
		
		del ex_top_node
		self.size -= 1

		return retval
	
	def isEmpty(self):
		return self.size <= 0

if __name__ == '__main__':
	
	stack = Stack()

	print(stack.isEmpty())
	
	stack.push((0, 0))
	stack.push((0, 1))
	stack.push((1, 0))
	stack.push((1, 1))


	print(stack.isEmpty())

	print(stack.pop())
	print(stack.pop())

	print('peeking...')
	print(stack.peek())
	print(stack.peek())
	print(stack.peek())

	print('popping...')
	print(stack.pop())
	print(stack.pop())
	print(stack.pop())
	print(stack.pop())
	print(stack.pop())
	print(stack.pop())
	print(stack.pop())

	print(stack.isEmpty())