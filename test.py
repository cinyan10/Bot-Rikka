original_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

# Define the size of each sublist
chunk_size = 20

# Use a list comprehension to create sublists
sublists = [original_list[i:i+chunk_size] for i in range(0, len(original_list), chunk_size)]

# Print the sublists
for sublist in sublists:
    print(sublist)
