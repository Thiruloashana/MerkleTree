
import hashlib
    
class MerkleTreeNode:
    
    def __init__(self,value):
        self.left = None
        self.right = None
        self.value = value
        self.hashValue = getHashValue(value)


def buildTree(leaves,f):

    nodes = []
    for i in leaves:
        nodes.append(MerkleTreeNode(i))

    while len(nodes)!=1:
        temp = []
        for i in range(0,len(nodes),2):
            node1 = nodes[i]
            if i+1 < len(nodes):
                node2 = nodes[i+1]
            else:
                temp.append(nodes[i])
                break
            f.write("Left child : "+ node1.value + " | Hash : " + node1.hashValue +" \n")
            f.write("Right child : "+ node2.value + " | Hash : " + node2.hashValue +" \n")
            concatenatedHash = node1.hashValue + node2.hashValue
            parent = MerkleTreeNode(concatenatedHash)
            parent.left = node1
            parent.right = node2
            f.write("Parent(concatenation of "+ node1.value + " and " + node2.value + ") : " +parent.value + " | Hash : " + parent.hashValue +" \n")
            temp.append(parent)
        nodes = temp
    return nodes[0]

    

def buildTrees(leaves,f):
    f = open("merkle.trees.txt", "a")
    nodes = []
    for i in leaves:
        nodes.append(MerkleTreeNode(i))

    while len(nodes)!=1:
        temp = []
        for i in range(0,len(nodes),2):
            node1 = nodes[i]
            if i+1 < len(nodes):
                node2 = nodes[i+1]
            else:
                temp.append(nodes[i])
                break
            f.write("Left child : "+ node1.value + " | Hash : " + node1.hashValue +" \n")
            f.write("Right child : "+ node2.value + " | Hash : " + node2.hashValue +" \n")
            concatenatedHash = node1.hashValue + node2.hashValue
            parent = MerkleTreeNode(concatenatedHash)
            parent.left = node1
            parent.right = node2
            f.write("Parent(concatenation of "+ node1.value + " and " + node2.value + ") : " +parent.value + " | Hash : " + parent.hashValue +" \n")
            temp.append(parent)
        nodes = temp 
    f.write("Merkle Tree 2\n")
    f.close()
    return nodes[0]


def getHashValue(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()



def combined(value1,value2):
    combinedValue = value1+value2
    return combinedValue



def checkConsistency(leaves1,leaves2):
    i=0
    while i<len(leaves1):
        if leaves1[i]!=leaves2[i]:
            break
        i+=1
    if i < len(leaves1):
        return []
    f = open("merkle.trees.txt", "w")
    f.write("Merkle Tree 1 \n")
    root1 = buildTrees(leaves1,f)
    f.close()
    f = open("merkle.trees.txt", "a")
    root2 = buildTrees(leaves2,f)
    f.write("Merkle Tree 2 \n")
    f.close()
    op = []
    op.append(root1.hashValue)
    
    with open("merkle.trees.txt") as f:
        data = f.readlines()
    data1=[]
    data.pop(-1)
    data1=data1+data
    data1.pop(-1)
    print(data1)
   
    tree2Index = 0
    for i in range(len(data1)):
        if data[i].startswith("Merkle Tree 2"):
            tree2Index = i
    print("tree index\n")
    print(tree2Index)
    parentLines2 = []
    leftChildLines2 = []
    rightChildLines2 = []
    
    parentLines1 = []
    leftChildLines1 = []
    rightChildLines1 = []
    
    for i in range(tree2Index,len(data1)):
        if data[i].startswith("Parent("):
            parentLines2.append(data[i])
    
    for i in range(tree2Index,len(data1)):
        if data[i].startswith("Left"):
            leftChildLines2.append(data1[i])

    for i in range(tree2Index,len(data1)):
        if data[i].startswith("Right"):
            rightChildLines2.append(data1[i])  
            
    for i in range(0,tree2Index):
        if data[i].startswith("Parent("):
            parentLines1.append(data1[i])
    
    for i in range(0,tree2Index):
        if data[i].startswith("Left"):
            leftChildLines1.append(data1[i])

    for i in range(0,tree2Index):
        if data[i].startswith("Right"):
            rightChildLines1.append(data1[i]) 
            
    print("Leftchild 1\n")
    print(leftChildLines1)
    print("Rightchild 1\n")
    print(rightChildLines1)
    print("Parentchild 1\n")
    print(parentLines1)
    
    print("Leftchild 2\n")
    print(leftChildLines2)
    print("Rightchild 2\n")
    print(rightChildLines2)
    print("Parentchild 2\n")
    print(parentLines2)
    
    op = []
    flag = False
    for i in range(len(parentLines2)):
        if root1.hashValue in parentLines2[i]:
            flag = True
            break
    if flag:
        values = []    
        combinedHash = ''
        lc = root1.value
        while combinedHash != root2.hashValue:
            for i in range(len(leftChildLines2)):
                if lc in leftChildLines2[i].split(" ")[-6]:
                    rc = rightChildLines2[i].split(" ")[-6]
                    values.append(getHashValue(rc))
                    break
            combinedValue = combined(getHashValue(lc),getHashValue(rc))
            combinedHash = getHashValue(combinedValue)
            lc = combinedValue
            
        op.append(root1.hashValue)
        op+=values
        op.append(root2.hashValue)
                
    else:
        root1LeftChildValue = leftChildLines1[-1].split(" ")[-6]
        print("root1leftchild\n")
        print(root1LeftChildValue)
        root1RightChildValue = rightChildLines1[-1].split(" ")[-6]
        print("root1rightchild\n")
        print(root1RightChildValue)
        for i in range(len(leftChildLines2)):
            if leftChildLines2[i].split(" ")[-6]==root1RightChildValue:
                root1RightChildSiblingValue = rightChildLines2[i].split(" ")[-6]
                print(root1RightChildSiblingValue)
        
        values = []
        values.append(getHashValue(root1LeftChildValue))
        values.append(getHashValue(root1RightChildValue))
        values.append(getHashValue(root1RightChildSiblingValue))
        root1RightChildCombinedValue = combined(getHashValue(root1RightChildValue),getHashValue(root1RightChildSiblingValue))        
        combinedHash = ''
        lc = root1LeftChildValue
        rc = root1RightChildCombinedValue
        
        while combinedHash != root2.hashValue:
            combinedValue = combined(getHashValue(lc),getHashValue(rc))
            combinedHash = getHashValue(combinedValue)
            lc = combinedValue
            for i in range(len(leftChildLines2)):
                if lc in leftChildLines2[i].split(" ")[-6]:
                    rc = rightChildLines2[i].split(" ")[-6]
                    values.append(getHashValue(rc))
                    break
            
        op.append(root1.hashValue)
        op+=values
        op.append(root2.hashValue)
                
    return op


def parseFile():
    
    f = open("merkle.tree.txt","r")
    tree ={}
    
    for line in f:
        lineArray = line.split(" ")
        print(lineArray)
        if lineArray[0] == 'Parent(concatenation':
            tree[lineArray[6]] = lineArray[10]
        else:
            tree[lineArray[3]] = lineArray[7]
    
    return tree


def checkInclusion(inputString,tree):
    
    op = []
    
    for key,value in tree.items():
        if inputString in key:
            op.append(value)
            inputString = value
            print("inputsring: {0}".format(inputString))
    
    return op


x=True

while x==True:
    
    choice=input("\n\t\tEnter your choice\n\t\t1. Building Merkletree\n\t\t2. Check for Inclusion of a data\n\t\t3. Check for Consistency of data in 2 trees\n\t\t4. Exit\n")
    
    
    if choice=="1":
        
        inputString = input("Enter the transaction id's : ")
        leavesString = inputString[0:len(inputString)]
       
        leaves = leavesString.split(",")
     
        f = open("merkle.tree.txt", "w")
        root = buildTree(leaves,f)
        f.close()
            
            
    elif choice=="2":
        
        inputString = input("Enter the transaction id's : ")
        tree = parseFile()
        op = checkInclusion(inputString,tree)
        if(len(op)> 0):
            print("yes",op)
        else:
            print("no")
            
    
    elif choice=="3":
        
        inputString1 = input("Enter the transaction id's of tree 1 : ")
        inputString2 = input("Enter the transaction id's of tree 2 : ")
        leavesString1 = inputString1[0:len(inputString1)]
        leaves1 = leavesString1.split(",")
        leavesString2 = inputString2[0:len(inputString2)]
        leaves2 = leavesString2.split(",")

        op = checkConsistency(leaves1,leaves2)
        if len(op) > 0:
            print("Yes",op)
        else:
            print("No")
    
    elif choice=="4":
        x=False
    
