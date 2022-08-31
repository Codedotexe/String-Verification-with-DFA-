#!env python3
import argparse

class Node:
	def __init__(self, name, isAccept=False):
		self.name = name
		self.isAccept = isAccept

	def __eq__(self, other):
		if isinstance(other, Node):
			return self.name == other.name
		else:
			return NotImplemented
	
	def __str__(self):
		return self.name if self.name != "" else "ε"

	def __hash__(self):
		return hash(tuple(sorted(self.__dict__.items())))

class Transition:
	def __init__(self, fromNode, toNode, inputToken, color=None):
		self.fromNode = fromNode
		self.toNode = toNode
		self.inputToken = inputToken
		self.color = color
	
	def __eq__(self, other):
		if isinstance(other, Node):
			return self.fromNode == other.fromNode and self.toNode == other.toNode and self.inputToken == other.inputToken
		else:
			return NotImplemented

	def __hash__(self):
		return hash(tuple(sorted(self.__dict__.items())))
	
	def __str__(self):
		if self.color != None:
			return f"{self.fromNode} -> {self.toNode} [label = \"{self.inputToken}\", color={self.color}];"
		else:
			return f"{self.fromNode} -> {self.toNode} [label = \"{self.inputToken}\"];"

class Automaton:
	def __init__(self, nodes=set(), transitions=[]):
		self.nodes = nodes
		self.transitions = transitions

	def addNode(self, node):
		self.nodes.add(node)
	
	def addTransition(self, transition):
		self.transitions.add(transition)
	
	def __str__(self):
		lines = []
		lines.append("strict digraph DFA {")
		lines.append("fontname=\"sans-serif\"")
		lines.append("rankdir=LR;")
		acceptNodes = filter(lambda x: x.isAccept, self.nodes)
		lines.append("node [shape=doublecircle];" + " ".join(map(str, acceptNodes)) + ";")
		lines.append("node [shape=circle];")

		for transition in self.transitions:
			lines.append(str(transition))

		lines.append("}")

		return "\n".join(lines)

def generateAutomaton(words, alphabetStr="a,...,z"):
	nodes = set([Node("", False)])
	transitions = []

	maxLength = max(map(len, words))
	for i in range(maxLength):
		for word in words:
			if len(word)-1 >= i:
				newNode = Node(word[:i+1], isAccept = i+1==len(word))
				nodes.add(newNode)
				transitions.append(Transition(Node(word[:i], False), newNode, word[i]))
	
	possibleChars = set().union(*map(lambda x: set(list(x)), words))
	for node in filter(lambda x: not x.isAccept, nodes):
		alreadyUsed = set( map(lambda x: x.inputToken, filter(lambda x: x.fromNode == node,  transitions)) )
		for char in possibleChars.difference(alreadyUsed):
			for otherNode in filter(lambda x: len(x.name) > 1, nodes):
				if node != otherNode and (node.name + char).endswith(otherNode.name):
					transitions.append(Transition(node.name, otherNode.name, char, color="blue"))

	for node in nodes:
		if node.name == "":
			alreadyUsed = set( map(lambda x: x.inputToken, filter(lambda x: x.fromNode == node, transitions)) )
			transitions.append(Transition(node, node, "Σ-{" + ",".join(alreadyUsed) + "}"))
		if node.isAccept:
			transitions.append(Transition(node, node, "Σ"))

	return Automaton(nodes=nodes, transitions=transitions)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("word", nargs="+")
	parser.add_argument("-o", dest="output")
	args = parser.parse_args()

	automaton = generateAutomaton(args.word)
	
	if args.output is None:
		print(automaton)
	else:
		with open(args.output, "w") as outputFile:
			outputFile.write(str(automaton))
