import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class AVLNode:
    def __init__(self, segment):
        self.segment = segment
        self.height = 1
        self.left = None
        self.right = None


def get_height(node):
    return node.height if node else 0


def get_balance_factor(node):
    return get_height(node.left) - get_height(node.right) if node else 0


def update_height(node):
    if node:
        node.height = 1 + max(get_height(node.left), get_height(node.right))


def right_rotate(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    update_height(y)
    update_height(x)

    return x


def left_rotate(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    update_height(x)
    update_height(y)

    return y


def insert_segment_into_avl(root, seg):
    if not root:
        return AVLNode(seg)

    if seg.left.x < root.segment.left.x:
        root.left = insert_segment_into_avl(root.left, seg)
    elif seg.left.x > root.segment.left.x:
        root.right = insert_segment_into_avl(root.right, seg)

    update_height(root)

    balance = get_balance_factor(root)

    if balance > 1:
        if seg.left.x > root.left.segment.left.x:
            root.left = left_rotate(root.left)
        return right_rotate(root)

    if balance < -1:
        if seg.left.x < root.right.segment.left.x:
            root.right = right_rotate(root.right)
        return left_rotate(root)

    return root


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


def find_first_intersection_in_avl(root, seg):
    if not root:
        return None

    if do_intersect(root.segment, seg):
        print(f"Intersection found: Line 1 - {root.segment.left.__dict__} to {root.segment.right.__dict__}", end=" ")
        print(f"Line 2 - {seg.left.__dict__} to {seg.right.__dict__}")
        return (root.segment, seg)

    if seg.left.x < root.segment.left.x:
        return find_first_intersection_in_avl(root.left, seg)

    if seg.left.x > root.segment.left.x:
        return find_first_intersection_in_avl(root.right, seg)

    return None


def find_first_intersection_in_avl_tree(arr):
    root = None
    arr = sorted(arr, key=lambda x: min(x.left.x, x.right.x))
    for seg in arr:
        res = find_first_intersection_in_avl(root, seg)
        if res:
            return res
        root = insert_segment_into_avl(root, seg)


def generate_random_segments_avl(num_segments, x_range, y_range):
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

if __name__ == "__main__":
    num_segments = 10  # Измените на желаемое количество отрезков
    x_range = (0, 20)  # Границы для координат x
    y_range = (0, 20)  # Границы для координат y

    segments = generate_random_segments_avl(num_segments, x_range, y_range)

    print("Generated Segments:")
    for idx, segment in enumerate(segments, start=1):
        print(f"Segment {idx}: Line - {segment.left.__dict__} to {segment.right.__dict__}")

    find_first_intersection_in_avl_tree(segments)
