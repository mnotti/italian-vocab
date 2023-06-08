import unittest
from max_heap import MaxHeap, Node

class MaxHeapTestCase(unittest.TestCase):
    def setUp(self):
        self.heap = MaxHeap()

    def test_insert_and_extract_max(self):
        self.heap.insert("Apple", 3)
        self.heap.insert("Banana", 5)
        self.heap.insert("Orange", 2)
        self.heap.insert("Mango", 4)

        max_element = self.heap.extract_max()
        self.assertEqual(max_element, "Banana")

    def test_reinsert_at_different_priority(self):
        self.heap.insert("Apple", 3)
        self.heap.insert("Banana", 5)
        self.heap.insert("Orange", 2)
        self.heap.insert("Mango", 4)

        max_element = self.heap.extract_max()
        self.assertEqual(max_element, "Banana")

        self.heap.insert("Banana", 1)
        max_element = self.heap.extract_max()
        self.assertEqual(max_element, "Mango")

    def test_extract_all_elements(self):
        self.heap.insert("Apple", 3)
        self.heap.insert("Banana", 5)
        self.heap.insert("Orange", 2)
        self.heap.insert("Mango", 4)

        elements = []
        while True:
            element = self.heap.extract_max()
            if element is None:
                break
            elements.append(element)

        expected_elements = ["Banana", "Mango", "Apple", "Orange"]
        self.assertEqual(elements, expected_elements)

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
