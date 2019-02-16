from big_fiubrother_core.messages import AbstractMessage

class ClustersMessage(AbstractMessage):
	
	def __init__(self, clusters):
		self.clusters = clusters