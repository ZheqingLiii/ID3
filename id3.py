import csv
import math
import operator
import sys
import ast

# define a class holding csv data
class Data():
    def __init__(self, classifier):
        self.eg = []
        self.attr = []
        self.classIndex = None

class Node():
    def __init__(self, is_leaf, parent):
        self.is_leaf = True
        self.attr_index = None # index of its attribute
        self.parent = parent
        self.child1 = None
        self.child2 = None
        self.child3 = None
        self.value = None # value for parent attribute
        self.result = None # positive and negative by default



# read the data from csv file into 'dataset'
def readData(filename, dataset):
    # read file, split data into lines, and put into examples
    dataset.eg = [row.split(',') for row in open(filename).read().splitlines()]
    # put first row as attribute names
    dataset.attr = dataset.eg.pop(0)
    # assume the last one is the classifier
    dataset.classIndex = len(dataset.attr) - 1


####################################################
# Build the ID3 tree
def buildTree(dataset, node, flag):
    # find numer of positive examples
    count_pos = 0
    for rel in dataset.eg:
        if rel[-1] == p:
            count_pos += 1
    # if all positive examples

    if count_pos == len(dataset.eg):
        node.is_leaf = True
        node.result = p
        return node
    # if all negative examples
    elif count_pos == 0:
        node.is_leaf = True
        node.result = n
        return node
    else:
        node.is_leaf = False

    E_s = calc_Entropy_S(dataset)

    gain_val = [] # list of calculated gain values
    attr_gain = [] # list of attributes
    for attributes in dataset.attr:
        if attributes != dataset.attr[-1]: # eliminate the last class
            attr_gain.append(attributes)
            if flag == 1:
                gain_val.append(calc_gain_ratio(dataset, attributes, E_s))
            else:
                gain_val.append(calc_gain(dataset, attributes, E_s))
    # get max gain value and the corresponding attribute index

    max_index, max_gain = max(enumerate(gain_val), key=operator.itemgetter(1))
    node.attr_index = max_index

    # if the max gain is too small, stop growing the tree
    if max_gain <= 0.01:
        node.is_leaf = True
        node.result = classify_leaf(dataset)
        return node

    possible_values = get_possible_value(dataset, max_index)

    for values in possible_values:
        child_data = Data("") # set data for child node
        child_data.attr = dataset.attr
        for examples in dataset.eg:
            if examples[max_index] == values:
                child_data.eg.append(examples)

        child_node = Node(True, node) # set new child node
        child_node.value = values

        # build subtrees
        if node.child1 is None:
            node.child1 = child_node
            buildTree(child_data, node.child1, flag)
        elif node.child2 is None:
            node.child2 = child_node
            buildTree(child_data, node.child2, flag)
        elif node.child3 is None:
            node.child3 = child_node
            buildTree(child_data, node.child3, flag)
        else: print("More child shoud be added in the node class.")



###########################################################
# classify leaf based on number of p/n results
def classify_leaf(dataset):
    count_pos = 0
    count_neg = 0
    for rel in dataset.eg[-1]:
        if rel == p:
            count_pos += 1
        elif rel == n:
            count_neg += 1

    if count_pos >= count_neg:
        return p
    else:
        return n

###########################################################
# calculat gain ratio
def calc_gain_ratio(dataset, attribute, E_s):
    gain_value = calc_gain(dataset, attribute, E_s)
    if gain_value == 0: return 0
    
    attr_index = find_index(dataset, attribute)
    possible_value = get_possible_value(dataset, attr_index) # value names
    count_value = [] # number of values
    for val in possible_value:
        count_value.append(0)
    
    for i, value in enumerate(possible_value, 0):
        for example in dataset.eg:
            if example[attr_index] == value:
                count_value[i] +=1

    splitInfo = 0
    total = len(dataset.eg)
    for count in count_value:
        p = count / total
        splitInfo -= p * math.log2(p)
    gain_ratio = gain_value / splitInfo
    return gain_ratio



# find the index of the attribute
def find_index(dataset, attribute):
    attr_index = 0
    for i,val in enumerate(dataset.attr, 0):
        if attribute == val:
            attr_index = i
    return attr_index

# get list of possible values of the attribute
def get_possible_value(dataset, attr_index):
    val = []
    for example in dataset.eg:
        if example[attr_index] not in val:
            val.append(example[attr_index])
    return val



# find the information gain of an attribure
def calc_gain(dataset, attribute, E_s):
    gain = E_s
    attr_index = find_index(dataset, attribute)
    values = get_possible_value(dataset, attr_index) # possible values of the attribute

    for value in values:
        temp1 = temp2 = 0
        por = count_proportion(dataset, attr_index, value)
        
        P_pos = count_pos_por(dataset, attr_index, value)
        
        if P_pos != 0 and P_pos != 1:
            P_neg = 1 - P_pos
            temp1 -= P_pos * math.log2(P_pos)
            temp2 -= P_neg * math.log2(P_neg)
            gain -= por * (temp1 + temp2)
    return gain


# proportation of the value in dataset
def count_proportion(dataset, attr_index, value):
    count = 0
    for examples in dataset.eg:
        if examples[attr_index] == value:
            count += 1
    return count/len(dataset.eg)

# proportation of the positive results of that value
def count_pos_por(dataset, attr_index, value):
    count = 0
    count_pos = 0
    for example in dataset.eg:
        if value == example[attr_index]:
            count += 1
            if example[-1] == p:
                count_pos += 1
    return count_pos / count
    

# calcutale Entropy(S)
def calc_Entropy_S(dataset):
    entropy = 0
    pos = 0
    total = len(dataset.eg)
    for eg in dataset.eg:
        if eg[-1] == p:
            pos+=1

    P_positive = pos / total
    P_negative = 1 - P_positive

    if (P_positive != 0) and (P_negative != 0):
        entropy -= P_positive * math.log2(P_positive)
        entropy -= P_negative * math.log2(P_negative)
    return entropy



###################################################
# calculate accuracy of 'testdata'
def test_acc(root, testdata):
    right = 0
    rel = [] # store test results
    # get test results
    for i,example in enumerate(testdata.eg, 0):
        rel.append(test_rel(example,root))
        if example[-1] == rel[i]:
            right += 1
    acc = right / len(testdata.eg)
    return acc

# print calculated accuracy and output testing results
def test_output(root, testdata):
    right = 0
    rel = []
    for i,example in enumerate(testdata.eg, 0):
        rel.append(test_rel(example,root))
        if example[-1] == rel[i]:
            right += 1
    # output results
    with open('result.csv', 'w') as result:
        header = ",".join(str(x) for x in testdata.attr) #convert list into string
        result.write(header)
        for i,example in enumerate(testdata.eg,0):
            example[-1] = rel[i]
            exg = ",".join(str(x) for x in example) #convert list into string
            result.write(exg+'\n')
    print("Outputted in result.csv")
    acc = right / len(testdata.eg)
    print("Test accuracy: " + str(acc * 100) + "%")


# get the test result of each examples, n/p
def test_rel(example, node):
    if node == None:
        print('TypeError: NoneType')
        return
    elif node.is_leaf == True:
        return node.result
    else:
        if node.child1 is not None:
            node1 = node.child1
            if example[node.attr_index] == node1.value:
                return test_rel(example, node.child1)
        if node.child2 is not None:
            node2 = node.child2
            if example[node.attr_index] == node2.value:
                return test_rel(example, node.child2)
        if node.child3 is not None:
            node3 = node.child3
            if example[node.attr_index] == node3.value:
                return test_rel(example, node.child3)
        else:
            return n

###################################################
# Reduced Error Pruning
def pruneTree(root, node, valdata, best_acc):
    if node.is_leaf == False:
        if node.child1 is not None:
            acc = pruneTree(root, node.child1, valdata, best_acc)
            if node.is_leaf == True:
                return acc
        if node.child2 is not None:
            acc = pruneTree(root, node.child2, valdata, best_acc)
            if node.is_leaf == True:
                return acc
        if node.child3 is not None:
            acc = pruneTree(root, node.child3, valdata, best_acc)
            if node.is_leaf == True:
                return acc
        return acc
    else:
        # if it's a leaf node, reset its parent node
        node.parent.is_leaf = True
        node.parent.result = p
        acc_p = test_acc(root, valdata)
        node.parent.result = n
        acc_n = test_acc(root, valdata)
        
        # compare which value gets better accuracy
        if best_acc <= acc_n and acc_n >= acc_p:
            return acc_n
        elif best_acc <= acc_p and acc_p >= acc_n:
            node.parent.result = p
            return acc_p
        else:
            # if not, change parent node back
            node.parent.is_leaf = False
            node.parent.result = None
            return best_acc


###################################################
def main():
    args = ast.literal_eval(str(sys.argv))
    # set two possible results
    global p, n
    if '-w' in args:
        p = 'won'
        n = 'nowin'
    else: # default value
        p = 'positive'
        n = 'negative'

    # Reading training data
    dataset = Data("")
    readData('train.csv', dataset)
    
    print("Building tree...")
    root = Node(True, None)
    if '-r' in args: # use gain ratio
        buildTree(dataset, root, 1)
    else: # use gain information
        buildTree(dataset, root, 0)

    # Reading testing data
    testdata = Data("")
    readData('test.csv', testdata)
    # Testing data
    test_output(root,testdata)

    if '-p' in args:
        print("Pruning tree...")
        # Reading validating data
        valdata = Data("")
        readData('validate.csv', valdata)
        pre_acc = test_acc(root, valdata) # accuracy on validation data before pruning
        print("Pre-pruning validate accuracy: " + str(pre_acc * 100) + "%")
        post_acc = pruneTree(root, root, valdata, pre_acc)
        print("Post-pruning validate accuracy: " + str(post_acc * 100) + "%")

        # check accuracy on testing data and output the results after pruning
        # testdata_p = Data("")
        # readData('test.csv', testdata_p)
        # test_output(root,testdata_p)

if __name__ == "__main__":
    main()
