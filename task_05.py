import random
import abc
from math import sqrt, floor

class AbstractHashTable(abc.ABC):
    @abc.abstractmethod
    def insert(self, value):
        raise NotImplementedError()

    @abc.abstractmethod
    def search(self, value):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_collisions_amount(self):
        raise NotImplementedError()

    def _build_table(self, values):
        for value in values:
            self.insert(value)
        return


    @classmethod
    def find_prime(cls, n):
        def prime(x):
            if x % 2 == 0:
                return False
            elif any(x % i == 0 for i in range(3, int(sqrt(x)) + 1, 2)):
                return False
            else:
                return True

        prime_list = []
        i = 1
        while not prime_list:
            prime_list = [x for x in range(3 * n // (i + 1), 3 * n // i) if prime(x)]
            i += 1

        return random.choice(prime_list)

class LinkedList():
    class Node():
        def __init__(self, data, next):
            self.data = data
            self.next = next

        def __repr__(self):
            return "Node({})".format(self.data)

    def __init__(self):
        self.head = None
        self._length = 0

    def __len__(self):
        return self._length

    def __repr__(self):
        return "LinkedList(len={})".format(self._length)

    def insert(self, data):
        self.head = LinkedList.Node(data, self.head)
        self._length += 1

    def search(self, data):
        current = self.head
        while current is not None and current.data != data:
            current = current.next

        return current is not None

class ChainTable(AbstractHashTable):
    def __init__(self, values):
        self.size = ChainTable.find_prime(len(values))
        self._elements = [LinkedList() for _ in range(self.size)]
        self._build_table(iter(values))

    def insert(self, value):
        hash_value = self.hash_function(value)
        try:
            lst = self._elements[hash_value]
            lst.insert(value)
        except IndexError:
            print("YOU ARE DOING SOMETHING WRONG")

        return

    def search(self, value):
        hash_value = self.hash_function(value)
        lst = self._elements[hash_value]
        return lst.search(value)

    def get_collisions_amount(self):
        count = 0
        for lst in self._elements:
            if len(lst):
                count += len(lst) - 1

        return count

class ChainTableByDivision(ChainTable):
    def __init__(self, values):
        super().__init__(values)

    def hash_function(self, k):
        return k % self.size


class ChainTableByMultiplication(ChainTable):
    def __init__(self, values):
        self.random_float = random.uniform(0, 1)
        super().__init__(values)


    def hash_function(self, k):
        return floor(self.size * (k * self.random_float % 1))

class TableOverfilled(Exception):
    pass

class OpenAddressTable(AbstractHashTable):
    def __init__(self, values):
        self.size = OpenAddressTable.find_prime(len(values))
        self._elements = [None for i in range(self.size)]
        self.collisions = 0
        self._build_table(iter(values))

    def insert(self, value):
        i = 0
        while i < self.size:
            hash_value = self.hash_function(value, i)
            element = self._elements[hash_value]
            if not element:
                self.collisions += i
                self._elements[hash_value] = value
                return
            else:
                i += 1

        raise TableOverfilled()

    def search(self, value):
        i = 0
        hash_value = self.hash_function(value, i)
        element = self._elements[hash_value]
        while element and i < self.size:
            hash_value = self.hash_function(value, i)
            element = self._elements[hash_value]
            if element == value:
                return True
            else:
                i += 1

        return False

    def helper_hash_function(self, k):
        return k % self.size

    def get_collisions_amount(self):
        return self.collisions


class OpenAddressTableByLinearProbing(OpenAddressTable):
    def __init__(self, values):
        super().__init__(values)

    def hash_function(self, k, i):
        return (self.helper_hash_function(k) + i) % self.size

class OpenAddressTableByQuadraticProbing(OpenAddressTable):
    def __init__(self, values):
        self._c1 = 2
        self._c2 = 3
        super().__init__(values)

    def hash_function(self, k, i):
        return (self.helper_hash_function(k) +
                self._c1 * i + self._c2 * pow(i, 2)) % self.size

class OpenAddressTableByDoubleHashing(OpenAddressTable):
    def __init__(self, values):
        self._modulo_for_second_hf = \
            OpenAddressTableByQuadraticProbing.find_prime(len(values) // 2)
        super().__init__(values)

    def hash_function(self, k, i):
        def second_helper_hash_function(k):
            return self._modulo_for_second_hf - (k % self._modulo_for_second_hf)

        return (self.helper_hash_function(k) +
               i * second_helper_hash_function(k)) % self.size

class HashTable():
    HASH_TABLES = [ChainTableByDivision,
                   ChainTableByMultiplication,
                   OpenAddressTableByLinearProbing,
                   OpenAddressTableByQuadraticProbing,
                   OpenAddressTableByDoubleHashing]

    def __init__(self, hash_type, values):
        self._hash_table = HashTable.HASH_TABLES[hash_type - 1](values)
        self._values = values

    def get_collisions_amount(self):
        return self._hash_table.get_collisions_amount()

    def find_sum(self, s):
        for value in self._values:
            if self._hash_table.search(s - value):
                return value, s - value
        return None
