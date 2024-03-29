import statistics
import string
# create matrix for animals
#Sharks, rays, amphibians
#sharks
#rays
#amphibians               

#function determines the lowest element in the matrix
def minVal(animal_matrix): 
    minVal = 999 #start minimum with first element
    for row in range(len(animal_matrix)): 
        for col in range(len(animal_matrix)): 
            if animal_matrix[row][col] != None:
                if (animal_matrix[row][col] < minVal): 
                    minVal = animal_matrix[row][col]
    return minVal

#function that returns leaves for shortest distances
def leavesReturn(matrix,short_dist): 
    related_leaves = list()
    all_leaves = list()
    breakFlag = False
    for row in range(len(matrix)):
        for col in range(len(matrix)): 
            if matrix[row][col] == short_dist:
                # print(matrix[row][col])
                related_leaves.append(row)
                related_leaves.append(col)
                all_leaves.append(related_leaves[:])
                all_leaves = all_leaves.copy() #make a copy of the list to unlink reference
                #related_leaves.clear()#clear the list
                breakFlag = True
                break
        if breakFlag == True:
            break
    # return all_leaves
    return related_leaves

#find average for each cell
def cellAverage(matrix, leaf_group, other_cell): 
    if leaf_group[0] != other_cell and leaf_group[1] != other_cell:
    #    print("Val at that cell", matrix[leaf_group[group][0]][other_cell])
        # # print("M0:", matrix[leaf_group[0]][other_cell], "M0:", matrix[other_cell][leaf_group[0]],"\n")
        # print("M1:", matrix[leaf_group[1]][other_cell], "M1:", matrix[other_cell][leaf_group[1]],"\n")
        Sum = noneTo0(matrix[leaf_group[0]][other_cell]) + noneTo0(matrix[other_cell][leaf_group[0]])+ \
              noneTo0(matrix[leaf_group[1]][other_cell]) + noneTo0(matrix[other_cell][leaf_group[1]])
        Sum /= 2
        return Sum
    else:
        return None

def noneTo0(value):
    if value == None: 
        value = 0
        return value
    else: 
        return value

#update the new matrix by putting None where ever needed 
def updateRow(matrix, leaf_group):
   row_list = list()
   #check the leaf_group and the next cells next to it and update new matrix
   #need to truncate matrix but only do the first row for averages
   for row in range(len(matrix)): 
       # traverse through the rows get the averages 
       avg = cellAverage(matrix, leaf_group, row)
       #append to a row list
       row_list.append(avg)
       #move all the None type to the left
       row_list.sort(key=lambda k: k!=None)
   return row_list

# place the new row value where the old one was
def makeMatrix(matrix,leaf_group,new_row,row_location): 
    #first delete a row and column from the old matrix
    new_matrix = delRowCol(matrix,leaf_group)
    #replace the old row with the new one
    del new_row[row_location]
    new_matrix[row_location] = new_row
    #reupdate the matrix to with None values
    new_matrix = updateMatrix(new_matrix)
    return new_matrix
    
# return the matrix with the delete row x col
def delRowCol(matrix, leaf_group):
    #delete the row and column with the highest index value
    delRow=leaf_group[0] if leaf_group[0]>leaf_group[1] else leaf_group[1]
    delCol=delRow
    for row in matrix: #delete the column from that row
        del row[delCol]
    del matrix[delRow]
    #update the matrix and put None where ever neccesary
    matrix = updateMatrix(matrix)
    return matrix

# return matrix where the same row|col are None
# ex. [A][A] == 1
def updateMatrix(matrix): 
    for row in range(len(matrix)): 
        for col in range(len(matrix)): 
            if row == col:
                matrix[row][col] = None
                # print(matrix)
    return matrix

# return the row location where to insert the new row
def whichRow(leaf_group):
    row_loc=leaf_group[0] if leaf_group[0]<leaf_group[1] else leaf_group
    return row_loc

# Update dictionary with a key and values for each taxa or leaf
def updateDict(dictionary, shortest_dist, leaf_list): 
    tmp_list = []
    #check to see if there is the same key in the dictionary
    if shortest_dist in dictionary:
        #if there is the same key then we make a nested list
        tmp_list.append(dictionary.get(shortest_dist))
        tmp_list.append(leaf_list)
        dictionary[shortest_dist] = tmp_list
    else: 
        #add a new leaf list to the dictionary
        dictionary[shortest_dist] = leaf_list

    return dictionary

# enumuerate all the values in rows of the matrix to become distinctive letters
# and return a list that has those letters to represent different species
def letToNum(matrix): 
    letter_list = list()
    for num_letter in zip(range(len(matrix)), string.ascii_uppercase):
        letter_list.append(num_letter[1])
    return letter_list

# check for which rows or specie can become combined as one cluster
# return the new list
def updateSpeciesList(species_list, matrix, shortest_dist):
    #create an empty list that will store two elements  for clusters
    cluster = list()
    isBreak = False

    # look for the first shorteset distance in the matrix
    for row in range(len(matrix)):
        for col in range(len(matrix)):
            if matrix[row][col] == shortest_dist:
                #add the row and colum to the list
                cluster.append(species_list[row])
                cluster.append(species_list[col])
                #delete the row values in the species list
                species_list.pop(col)
                species_list.pop(row)
                isBreak = True
                break
        if isBreak == True:
            break
    species_list.insert(row,cluster)
    return species_list

def main():
    # matrix = [[None,    9,    2,    4,    9,   10],
    #           [None, None,    9,    6,    2,   10],
    #           [None, None, None,    5,    9,   10],
    #           [None, None, None, None,    6,   10],
    #           [None, None, None, None, None,   10], 
    #           [None, None, None, None, None, None]]
    
    matrix = [[None,    1,    2,    4,    4,    4,   4],
              [None, None,    1,    3,    3,    3,   3],
              [None, None, None,    2,    2,    2,   2],
              [None, None, None, None,    0,    2,   2],
              [None, None, None, None, None,    2,   2],
              [None, None, None, None, None, None,   0],
              [None, None, None, None, None, None, None]]

    keepGoing = True
    leaf_list = []
    species_list = []

    species_list = letToNum(matrix)

    while(keepGoing == True): 

        #Step 1. Find the min value. But first check if the 
        shortest_dist = minVal(matrix)

        #Step 2. find the row x col that has that min value from the matrix
        leaf_list = leavesReturn(matrix, shortest_dist)
        
        #Step 3. Cluster species that have a short distance between them
        species_list = updateSpeciesList(species_list, matrix, shortest_dist)

        #Step 4. Calculate the average distance from the row x col (cluser value)
        #        Return the new row to be inserted
        new_row = updateRow(matrix,leaf_list)

        #Step 5. determine the locaton of where to place the new row
        row_loc = whichRow(leaf_list)

        #Step 6. Put the new row into the matrix and update the old matrix
        matrix = makeMatrix(matrix,leaf_list,new_row, row_loc) 
        
        #Step 7. Check if when we only have 2 clusters in the matrix
        keepGoing = False if len(matrix) <= 2 and len(matrix[0]) <= 2 else True

    print(species_list) 

if __name__ == "__main__":
    main()