import os 
import unittest
import timeit

# Unit testing framework for Floyd's Alogrithm
class UnitTestFloyd(unittest.TestCase):

    graphTest = graph_1

    # Test 1: To confirm the variable type is a list using Boolean
    def test1_list(self):
        print("Is the variable type in graph list?")
        result = True
        if isinstance(self.graphTest, list):
            for i in self.graphTest:
                if not isinstance(i, list):
                    result = False
                    break
        else:
            result = False
        self.assertTrue(result, "The graph is not of type list")
        print("Yes, the type is list.\n")

    # Test 2: To confirm the items are integers using Boolean
    def test2_integer(self):
        print("Are all the graph items integers?")
        result = True
        matrix_size = len(self.graphTest)
        for i in range(matrix_size):
            for k in range(matrix_size):
                try:
                    int(self.graphTest[i][k])
                except ValueError:
                    result = False
        self.assertTrue(result, "Not all the item is an integer.")
        print("Yes, all the graph items are integers.\n")

unittest.main(exit=False)

# Performance test to verify the application on the speed of recursive code

Recursive_floyd_graph1= timeit.Timer(
    lambda: recursive_floyd(graph_1)).repeat(repeat=100000, number=1)
Recursive_floyd_graph2 = timeit.Timer(
    lambda: recursive_floyd(graph_2)).repeat(repeat=100000, number=1)
Recursive_average = (1000 * (sum(Recursive_floyd_graph1) / len(Recursive_floyd_graph1) + (
        sum(Recursive_floyd_graph2) / len(Recursive_floyd_graph2)))) / 2
print("The time taken is", Recursive_average, "ms for the recursion.")