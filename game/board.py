import ast
import random

class Board:

	ROWS = 4
	COLS = 4

	transformations = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

	def __init__(self, rep=None):
		if not rep:
			dist = BoggleDistribution()
			# Generate a new self.board
			self.board = []
			for r in range(self.ROWS):
				self.board.append([])
				for c in range(self.COLS):
					self.board[r].append(dist.draw())
		else:
			self.board = ast.literal_eval(rep) # De-serialize from string

	def solve(self, words):
		found = set()
		for item in words.dict:
			if self.wordExists(item):
				found.add(item)
		return found

	def wordExists(self, word, start=None):
		if len(word) == 0:
			return True

		if not start:
			for r in range(self.ROWS):
				for c in range(self.COLS):
					let = self.board[r][c]
					if let == word[0]:
						self.board[r][c] = ""
						recurse_result = self.wordExists(word[1:], start=(r, c))
						self.board[r][c] = let
						if recurse_result:
							return True
		else:
			for t in self.transformations:
				y, x = start[0] + t[0], start[1] + t[1]
				if 0 <= y < self.ROWS and 0 <= x < self.COLS:
					let = self.board[y][x]
					if let == word[0]:
						self.board[y][x] = ""
						recurse_result = self.wordExists(word[1:], start=(y, x))
						self.board[y][x] = let
						if recurse_result:
							return True
		return False

	def __str__(self):
		rep = ""
		for r in range(self.ROWS):
			for c in range(self.COLS):
				rep += self.board[r][c] + " "
			rep += "\n"
		return rep

	def __repr__(self):
		return str(self.board)


class BagDistribution:
	# Takes a map determining the weight given to each key, with larger weights
	# representing proportionally higher odds of being drawn
	def __init__(self, key_to_weight_mapping):
		self.map = key_to_weight_mapping.copy()
		self.sum = 0
		for k, v in self.map.items():
			self.sum += v

	def draw(self):
		rnd = random.random() * self.sum
		runSum = 0
		for k, v in self.map.items():
			runSum += v
			if runSum >= rnd:
				return k
		return None


# Not exactly the way that Boggle boards are generated, but close enough. Real
# Boggle boards use dice with fixed values on each side. This way of board generation
# relies on the distributions of each letter coming up, allowing for unlikely things like 
# 2 Z's being present on the board
class BoggleDistribution(BagDistribution):
	def __init__(self):
		letter_to_frequency = { "e": 19, "t": 13, "a": 12, "r": 12,
								"i": 11, "n": 11, "o": 11, "s":  9,
								"d":  6, "c":  5, "h":  5, "l":  5,
								"f":  4, "m":  4, "p":  4, "u":  4,
								"g":  3, "y":  3, "w":  2, "b":  1,
								"j":  1, "k":  1, "q":  1, "v":  1,
								"x":  1, "z":  1 }
		BagDistribution.__init__(self, letter_to_frequency)


class WordDictionary:
	def __init__(self, file_path):
		with open(file_path, 'r') as f:
			lines = f.readlines()
		self.dict = { item.strip() for item in lines }


	def contains(self, elem):
		return elem in self.dict

	def __str__(self):
		rep = ""
		for item in self.dict:
			rep += item + "\n"
		return rep
