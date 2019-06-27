from big_fiubrother_core.messages import AbstractMessage

class ClustersMessage(AbstractMessage):
	def __init__(self, clusters):
		self.clusters = clusters

    def is_empty(self):
        len(self.clusters) == 0