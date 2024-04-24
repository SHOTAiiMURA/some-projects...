test_list = [1,2,3,4,5,6 ]


#def insert(self, index, data):
#    if index < 0 or index > len(self.array):

print("The Original list: ", test_list)

temp = test_list[0]
for i in range(len(test_list)-1):
    test_list[i] = test_list[i+1]
test_list[-1] = temp

# Printing result
print("The list after shift is : ", test_list)