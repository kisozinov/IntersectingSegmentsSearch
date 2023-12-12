# 2-3 Tree
# balanced tree data structure with up to 2 data items per node

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, left, right):
        self.left = left
        self.right = right
	
    def __lt__(self, other):
       return self.left.x < other.left.x
    
    def show(self):
	    return self.left.__dict__, self.right.__dict__


class Node:
	def __init__(self, segment, par = None):
		#print ("Node __init__: " + str(data))
		self.data = list([segment])
		self.parent = par
		self.child = list()
		
	def __str__(self):
		if self.parent:
			return str(self.parent.data) + ' : ' + str(self.data)
		return 'Root : ' + str(self.data)
	
	def __lt__(self, node):
		return self.data[0] < node.data[0]
		
	def _isLeaf(self):
		return len(self.child) == 0
			
	# merge new_node sub-tree into self node
	def _add(self, new_node):
		# print ("Node _add: " + str(new_node.data) + ' to ' + str(self.data))
		for child in new_node.child:
			child.parent = self
		self.data.extend(new_node.data)
		self.data.sort()
		self.child.extend(new_node.child)
		if len(self.child) > 1:
			self.child.sort()
		if len(self.data) > 2:
			self._split()
	
	# find correct node to insert new node into tree
	def _insert(self, new_node):
		# print ('Node _insert: ' + str(new_node.data) + ' into ' + str(self.data))
		
		# leaf node - add data to leaf and rebalance tree
		if self._isLeaf():
			self._add(new_node)
			
		# not leaf - find correct child to descend, and do recursive insert
		elif new_node.data[0] > self.data[-1]:
			self.child[-1]._insert(new_node)
		else:
			for i in range(0, len(self.data)):
				if new_node.data[0] < self.data[i]:
					self.child[i]._insert(new_node)
					break
	
	# 3 items in node, split into new sub-tree and add to parent	
	def _split(self):
		# print("Node _split: " + str(self.data))
		left_child = Node(self.data[0], self)
		right_child = Node(self.data[2], self)
		if self.child:
			self.child[0].parent = left_child
			self.child[1].parent = left_child
			self.child[2].parent = right_child
			self.child[3].parent = right_child
			left_child.child = [self.child[0], self.child[1]]
			right_child.child = [self.child[2], self.child[3]]
					
		self.child = [left_child]
		self.child.append(right_child)
		self.data = [self.data[1]]
		
		# now have new sub-tree, self. need to add self to its parent node
		if self.parent:
			if self in self.parent.child:
				self.parent.child.remove(self)
			self.parent._add(self)
		else:
			left_child.parent = self
			right_child.parent = self
			
	# find an item in the tree; return item, or False if not found		
	def _find(self, item):
		# print ("Find " + str(item))
		if item in self.data:
			return item
		elif self._isLeaf():
			return False
		elif item > self.data[-1]:
			return self.child[-1]._find(item)
		else:
			for i in range(len(self.data)):
				if item < self.data[i]:
					return self.child[i]._find(item)
		
	def _remove(self, item):
		pass
		
	# print preorder traversal		
	def _preorder(self):
		print (self) 
		for child in self.child:
			child._preorder()
	
class Tree:
	def __init__(self):
		print("Tree __init__")
		self.root = None
		
	def insert(self, item):
		print("Tree insert: " + str(item))
		if self.root is None:
			self.root = Node(item)
		else:
			self.root._insert(Node(item))
			while self.root.parent:
				self.root = self.root.parent
		return True
	
	def find(self, item):
		return self.root._find(item)
		
	def remove(self, item):
		self.root.remove(item)
		
	def printTop2Tiers(self):
		print ('----Top 2 Tiers----')
		print (str([seg.show() for seg in self.root.data]))
		for child in self.root.child:
			print (str([seg.show() for seg in child.data]), end=' ')
		print(' ')
		
	def preorder(self):
		print ('----Preorder----')
		self.root._preorder()

def on_segment(p, q, r):
    return q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)


def orientation(p, q, r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    return 1 if val > 0 else 2


def do_intersect(s1, s2):
    p1, q1, p2, q2 = s1.left, s1.right, s2.left, s2.right

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1):
        return True

    if o2 == 0 and on_segment(p1, q2, q1):
        return True

    if o3 == 0 and on_segment(p2, p1, q2):
        return True

    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def find_first_intersection_in_23(root, seg):
    if not root:
        return None
    
    for s in root.data:
        if do_intersect(s, seg):
            print(f"Intersection found: Line 1 - {s.left.__dict__} to {s.right.__dict__}", end=" ")
            print(f"Line 2 - {seg.left.__dict__} to {seg.right.__dict__}")
            return (s, seg)

    if root.child:
        for s in root.data:
            if seg.left.x < s.left.x:
           	#tree.root = tree.root.c
                if len(root.child) > 1:
                    return find_first_intersection_in_23(root.child[1], seg)
                else:
                    return find_first_intersection_in_23(root.child[0], seg)
                #return find_first_intersection_in_23(tree.root.child[1], seg)

            elif seg.left.x > s.left.x:
                return find_first_intersection_in_23(root.child[-1], seg)

    return None


def find_first_intersection_in_23_tree(arr):
    tree = Tree()
    arr = sorted(arr, key=lambda x: min(x.left.x, x.right.x))
    for seg in arr:
        res = find_first_intersection_in_23(tree.root, seg)
        if res:
            return res
        tree.insert(seg)
        # tree.printTop2Tiers()

import random
def generate_random_segments_23(num_segments, x_range, y_range):
    segments = []
    for _ in range(num_segments):
        x1 = random.randint(*x_range)
        y1 = random.randint(*y_range)
        x2 = random.randint(*x_range)
        y2 = random.randint(*y_range)

        left = Point(min(x1, x2), min(y1, y2))
        right = Point(max(x1, x2), max(y1, y2))

        segments.append(Segment(left, right))
    return segments

#lst = [13, 7, 24, 15, 4, 29, 20, 16, 19, 1, 5, 22, 17]
arr = [
    Segment(Point(1, 5), Point(4, 5)),
    Segment(Point(2, 5), Point(10, 1)),
    Segment(Point(3, 2), Point(10, 3)),
    Segment(Point(6, 4), Point(9, 4)),
    Segment(Point(7, 1), Point(8, 1)),
]

#find_first_intersection_in_23_tree(arr)
# for item in arr:
# 	tree.insert(item)
# tree.printTop2Tiers()

if __name__ == "__main__":
    num_segments = 10  # Измените на желаемое количество отрезков
    x_range = (0, 20)  # Границы для координат x
    y_range = (0, 20)  # Границы для координат y

    segments = generate_random_segments_23(num_segments, x_range, y_range)

    print("Generated Segments:")
    for idx, segment in enumerate(segments, start=1):
        print(f"Segment {idx}: Line - {segment.left.__dict__} to {segment.right.__dict__}")

    find_first_intersection_in_23_tree(segments)