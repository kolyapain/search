import random

def min3(v1, v2, v3):
    if v1 < v2:
        if v1 < v3:
            return v1
    else:
        if v2 < v3:
            return v2
    return v3

def calculate(str_1, str_2):
    matrix = []
    for i in range(len(str_1) + 1):
        matrix.append([])
        for j in range(len(str_2) + 1):
            matrix[i].append(0)
    
    for i in range(1, len(str_1) + 1):
        matrix[i][0] = i
    for j in range(1, len(str_2) + 1):
        matrix[0][j] = j
    
    for j in range(1, len(str_2) + 1):
        for i in range(1, len(str_1) + 1):
            if str_1[i - 1] == str_2[j - 1]:
                cost = 0
            else:
                cost = 1
            
            matrix[i][j] = min3(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
    
    return matrix[-1][-1]

if __name__ == "__main__":
    print(calculate('sitting', 'kitten'))
    print(calculate('sunday', 'saturday'))
    print(calculate('exponential', 'polynomial'))
    print(calculate('gumbo', 'gambol'))
    print(calculate('item', 'item'))
