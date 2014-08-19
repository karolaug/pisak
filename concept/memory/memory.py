import numpy as np

class MemoryGame(object):
	def __init__(self, dims):
		self.dims = dims
		self.n_of_pairs = dims[0] * dims[1] / 2
		self.display_field = np.empty(dims)
		self.display_field.fill(-1)
		self.create_info_field()
		self.first_uncovered = False
		self.second_uncovered = False

	def create_info_field(self):
		info = np.arange(1, self.n_of_pairs + 1, 1)
		self.info_field = np.concatenate((info, info))
		np.random.shuffle(self.info_field)
		self.info_field = np.reshape(self.info_field, self.dims)

	def check_field(self,y,x):
		if self.first_uncovered == False:
			self.display_field[x,y] = self.info_field[x,y]
			self.first_uncovered = self.info_field[x,y]
			return 'first'

		elif self.info_field[x,y] == self.first_uncovered:
			self.display_field[x,y] = self.info_field[x,y]
			self.first_uncovered = False
			return 'second-hit'

		else:
			self.display_field[x,y] = self.info_field[x,y]
			self.second_uncovered = self.info_field[x,y]
			return 'second-miss'

	def revert(self): #do poprawki
		self.display_field -= (self.display_field == self.first_uncovered)*(self.first_uncovered +1)
		self.display_field -= (self.display_field == self.second_uncovered)*(self.second_uncovered +1)

		self.first_uncovered = False
		self.second_uncovered = False

