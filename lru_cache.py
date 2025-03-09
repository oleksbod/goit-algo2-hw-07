import random
import time
from collections import OrderedDict

# ---------- LRU Cache Реалізація ---------- #
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return None
        
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:            
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:            
            self.cache.popitem(last=False)
    
    def invalidate_range(self, index):        
        keys_to_remove = []
        for key in self.cache.keys():
            L, R = key
            if L <= index <= R:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.cache[key]
    
    def clear(self):
        self.cache.clear()

# ---------- Функції без кешу ---------- #
def range_sum_no_cache(array, L, R):
    return sum(array[L:R + 1])

def update_no_cache(array, index, value):
    array[index] = value

# ---------- Функції з кешем ---------- #
def range_sum_with_cache(array, L, R, cache):
    cached_result = cache.get((L, R))
    if cached_result is not None:
        return cached_result
    result = sum(array[L:R + 1])
    cache.put((L, R), result)
    return result

def update_with_cache(array, index, value, cache):
    array[index] = value
    cache.invalidate_range(index)

# ---------- Генерація тестових даних ---------- #
def generate_test_data(N, Q):
    array = [random.randint(1, 1000) for _ in range(N)]
    queries = []
    for _ in range(Q):
        if random.random() < 0.7:  # 70% на Range, 30% на Update
            L = random.randint(0, N - 1)
            R = random.randint(L, N - 1)
            queries.append(('Range', L, R))
        else:
            index = random.randint(0, N - 1)
            value = random.randint(1, 1000)
            queries.append(('Update', index, value))
    return array, queries

# ---------- Виконання запитів без кешу ---------- #
def execute_without_cache(array, queries):
    arr_copy = array[:]
    for q in queries:
        if q[0] == 'Range':
            range_sum_no_cache(arr_copy, q[1], q[2])
        elif q[0] == 'Update':
            update_no_cache(arr_copy, q[1], q[2])

# ---------- Виконання запитів з кешем ---------- #
def execute_with_cache(array, queries, cache_capacity=1000):
    arr_copy = array[:]
    cache = LRUCache(cache_capacity)
    for q in queries:
        if q[0] == 'Range':
            range_sum_with_cache(arr_copy, q[1], q[2], cache)
        elif q[0] == 'Update':
            update_with_cache(arr_copy, q[1], q[2], cache)

def main():
    N = 100_000
    Q = 50_000
    print(f"Генерація масиву з {N} елементів та {Q} запитів...")
    array, queries = generate_test_data(N, Q)

    # Виконання без кешу
    print(f"Виконання запитів без кешу...")
    start = time.time()
    execute_without_cache(array, queries)
    no_cache_time = time.time() - start
    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")

    # Виконання з кешем
    print(f"Виконання запитів з LRU-кешем...")
    start = time.time()
    execute_with_cache(array, queries)
    cache_time = time.time() - start
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")

    # Порівняння
    print(f"--- РЕЗУЛЬТАТИ ---")
    print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
    print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")

if __name__ == "__main__":
    main()
