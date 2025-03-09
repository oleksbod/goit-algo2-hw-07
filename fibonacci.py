import sys
sys.setrecursionlimit(10000)

import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# Реалізація Splay Tree
class SplayTreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self.splay(root.left.left, key)
                root = self.right_rotate(root)
            elif key > root.left.key:
                root.left.right = self.splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self.left_rotate(root.left)
            return self.right_rotate(root) if root.left else root
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self.splay(root.right.right, key)
                root = self.left_rotate(root)
            elif key < root.right.key:
                root.right.left = self.splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self.right_rotate(root.right)
            return self.left_rotate(root) if root.right else root

    def search(self, key):
        self.root = self.splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return
        self.root = self.splay(self.root, key)
        if key == self.root.key:
            self.root.value = value
            return
        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

# Реалізація fibonacci з lru_cache
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Реалізація fibonacci з Splay Tree
def fibonacci_splay(n, tree):
    cached = tree.search(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

# Вимірювання часу
def measure_time_lru(n):
    fibonacci_lru.cache_clear()
    start = timeit.default_timer()
    fibonacci_lru(n)
    end = timeit.default_timer()
    return end - start

def measure_time_splay(n):
    tree = SplayTree()
    start = timeit.default_timer()
    fibonacci_splay(n, tree)
    end = timeit.default_timer()
    return end - start

if __name__ == "__main__":
    ns = list(range(0, 1000, 50))
    times_lru = []
    times_splay = []

    for n in ns:
        time_lru = sum(measure_time_lru(n) for _ in range(5)) / 5
        time_splay = sum(measure_time_splay(n) for _ in range(5)) / 5
        times_lru.append(time_lru)
        times_splay.append(time_splay)

    # Таблиця результатів
    print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)'}")
    print("-" * 50)
    for n, lru_time, splay_time in zip(ns, times_lru, times_splay):
        print(f"{n:<10}{lru_time:<25.10f}{splay_time:.10f}")

    times_lru_us = [t * 1e6 for t in times_lru]
    times_splay_us = [t * 1e6 for t in times_splay]

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.plot(ns, times_lru_us, 'o-', color='blue', label='LRU Cache')
    plt.plot(ns, times_splay_us, 'o-', color='orange', label='Splay Tree')
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди * 1e-6)")
    plt.title("Порівняння продуктивності: LRU Cache vs Splay Tree")
    plt.legend()
    plt.grid(True)
    plt.show()
