# You are given two non-empty linked lists representing two non-negative integers.
# The digits are stored in reverse order, and each of their nodes contains a single digit.
# Add the two numbers and return the sum as a linked list.

# You may assume the two numbers do not contain any leading zero, except the number 0 itself.


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def add_two_numbers(l1, l2):
    def get_value(Node):
        value = ''
        while Node is not None:
            value += str(Node.val)
            Node = Node.next
        return int(value[::-1])

    summ = get_value(l1)+get_value(l2)

    temp = None
    for char in str(summ):
        new_node = ListNode(int(char))
        new_node.next = temp
        temp = new_node
    return new_node
