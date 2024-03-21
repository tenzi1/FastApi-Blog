import sys
import os

print("----------------------------")
print("file", __file__)
print("abs ", os.path.abspath(__file__))
print("dir", os.path.dirname(os.path.abspath(__file__)))
print("dor", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
