# MaxHeap can store any data type sorted by priority
class MaxHeap: 
	def __init__(self):
		self.nodes = []
		self.size = 0

	def swap(self, idx_a, idx_b):
		tmp = self.nodes[idx_a]
		self.nodes[idx_a] = self.nodes[idx_b]
		self.nodes[idx_b] = tmp

	def get_parent_idx(self, idx):
		return (idx - 1) // 2

	def get_left_child_idx(self, idx): 
		return (2*idx) + 1

	def get_right_child_idx(self, idx):
		return (2*idx) + 2

	def get_max_child_idx(self, idx):
		lc_idx = self.get_left_child_idx(idx)
		rc_idx = self.get_right_child_idx(idx)
		if rc_idx >= self.size or self.nodes[lc_idx].priority >= self.nodes[rc_idx].priority: 
			return lc_idx
		return rc_idx

	def is_leaf(self, idx): 
		return self.get_left_child_idx(idx) >= self.size 

	def extract_max(self):
		if self.size == 0:
			return None 
		extract_me = self.nodes[0]
		self.swap(0, self.size-1)
		self.size -= 1
		self.heapify(0)
		return extract_me.data

	def heapify(self, idx):
		cur_idx = idx
		while(not self.is_leaf(cur_idx)):
			max_child_idx = self.get_max_child_idx(cur_idx)
			if self.nodes[cur_idx].priority >= self.nodes[max_child_idx].priority:
				return
			self.swap(cur_idx, max_child_idx)
			cur_idx = max_child_idx
			continue

	def insert(self, data, priority):
		if (self.size == len(self.nodes)):
			self.nodes.append(Node(data, priority))
		else:
			self.nodes[self.size] = Node(data, priority)
		self.size += 1
		cur_idx = self.size - 1
		while self.get_parent_idx(cur_idx) >= 0 and self.nodes[self.get_parent_idx(cur_idx)].priority < self.nodes[cur_idx].priority:
			parent_idx = self.get_parent_idx(cur_idx)
			self.swap(parent_idx, cur_idx)
			cur_idx = parent_idx
		

class Node:
	def __init__(self, data, priority):
		self.data = data
		self.priority = priority
