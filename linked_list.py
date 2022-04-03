class Node:
    def __init__(self, data= None, next_node= None):
        self.data = data
        self.next_node = next_node

class LinkedList:
    def __init__(self):
        self.head = None
        self.last_node= None 

    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print(None)
        while node:
            ll_string += f" {str(node.data)} ->"
            node = node.next_node
        ll_string += " None"   
        print(ll_string)

    def to_arr(self):
        arr = []

        if self is None:
            return arr
        
        node = self.head
        while node:
            arr.append(node.data)
            node = node.next_node
        return arr

    def insert_beginning(self, data):
        if self.head is None:
           self.head = Node(data, None)
           self.last_node = self.head
        new_node = Node(data, self.head)
        self.head = new_node

    def insert_ending(self, data):
        if self.head is None:
            self.insert_beginning(data)
        
        # # if last node is None
        # if self.last_node is None:
        #     print("last node is None")
        #     node = self.head

        #     # while node.next_node: 
        #     #     print(f"at node: {node.data}")
        #     #     node = node.next_node

        #     node.next_node = Node(data, None)
        #     self.last_node = node.next_node
        # # if the last node is an existing node
        # else:
        self.last_node.next_node = Node(data, None)
        self.last_node = self.last_node.next_node

    def get_user_id(self, user_id):
        node = self.head
        while node:
            if node.data["id"] is int(user_id):
                return node.data
            node = node.next_node
        return None


# ll3 = LinkedList()
# ll3.insert_beginning("5")
# ll3.insert_beginning("4")
# ll3.insert_beginning("3")
# ll3.insert_beginning("2")
# ll3.insert_beginning("1")

# ll3.insert_ending("6")
# ll3.insert_ending("7")

# ll3.print_ll()