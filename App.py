class Nodes:
    def __init__(self, data):
        self.data = data
        self.next = None


print = int(input("What"))
node1 = Nodes(1)
node2 = Nodes(2)
node3 = Nodes(3)
node4 = Nodes(4)

node1.next = node2
node2.next = node3
node3.next = node4

count = 0
c = node1
while c:
    print(c.data, end=" -> ")
    count += 1
    c = c.next
    if c == None:
        print("None")

print(count)