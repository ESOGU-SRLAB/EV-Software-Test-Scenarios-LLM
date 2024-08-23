import sys

sys.path.append(r"E:/Kodlar/alnsesogutest_v3")

from AlnsObjects.Solution import Solution
from AlnsObjects.Route import Route
from DataObjects.ChargeStation import ChargeStation
from DataObjects.Customer import Customer
from DataObjects.Target import Target
from readProblemInstances import readProblemInstances

import xml.etree.ElementTree as ET
import numpy as np

file = r"E:/Kodlar/alnsesogutest_v3/SchneiderData/newesogu-r40-ds1.xml"
def array_to_solution(routes):
    
    tree = ET.parse(file)
    root = tree.getroot()
    distance_matrix_tag = 'DijkstraMatrix'
    distance_matrix_data = root.find(distance_matrix_tag).text
    matrix_lines = distance_matrix_data.splitlines()
    distance_matrix = np.array([[int(x) for x in line.split()] for line in matrix_lines])
    
    points = root.find("Points")
    total_solution = 0        
    
    for route in routes:
        left = None
        right = None
        route_solution = 0
        for index in range(1,len(route)):
            
            left = index-1 
            right = index
            
            for point in points:
                left_item = route[left].replace(" ", "")
                
                if point.attrib["Name"] == left_item :
                    left_index = int(point.attrib["No"]) - 1
                    
                right_item = route[right].replace(" ", "")
                if point.attrib["Name"] == right_item :
                    right_index = int(point.attrib["No"]) - 1    
                    
            print(f"{route[left]}({left_index}) - {route[right]}({right_index}) \t: {distance_matrix[left_index][right_index]}")        
            route_solution += distance_matrix[left_index][right_index]
            if "cs" in route[index]  :
                
                print("---------part----------", "+|", route_solution, "|")
                
        total_solution += route_solution
        
    print("Total Solution : ", total_solution)

def get_Solution(routes, problem_instance):
    
    unserved_customers = []
    served_customers = []

    solution = Solution(unserved_customers, served_customers, routes, problem_instance)
    return solution

def string_to_array(string_data):

    cleaned_data = string_data.strip("[]").replace("], ", "]|").split("|")
    final_data = [[item.strip(" '[]") for item in row.split(",")] for row in cleaned_data]

    return final_data

my_solution = "[cs5, 42A, 122, 60B/2, cs1, 12, 11, cs5, ]"
my_solution = string_to_array(my_solution)
print(my_solution)
array_to_solution(my_solution)
