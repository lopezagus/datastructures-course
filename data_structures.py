from typing import Any, List, Optional, Union


class DoubleLinkedList:
    class _Node:
        __slots__ = '_element', '_next', '_prev'

        def __init__(self, element: Any, nxt, prv) -> None:
            """
            :param element: Any, element inside container
            :param nxt: None or Node object, next in list order
            :param prv: None or Node object, previous in list order
            """
            self._element = element
            self._next = nxt
            self._prev = prv

        @property
        def element(self):
            return self._element

        @element.setter
        def element(self, arg):
            self._element = arg

        @property
        def next(self):
            return self._next

        @next.setter
        def next(self, arg):
            if isinstance(arg, DoubleLinkedList._Node) or arg is None:
                self._next = arg
            else:
                raise TypeError('Invalid node assignment on next')

        @property
        def prev(self):
            return self._prev

        @prev.setter
        def prev(self, arg):
            if isinstance(arg, DoubleLinkedList._Node) or arg is None:
                self._prev = arg
            else:
                raise TypeError('Invalid node assignment on previous')

        def __repr__(self):
            return str(self._element)

        def __eq__(self, other):
            return self._element == other

        def __ne__(self, other):
            return self._element != other

        def __lt__(self, other):
            return self._element < other

        def __gt__(self, other):
            return self._element > other

        def __ge__(self, other):
            if isinstance(other, DoubleLinkedList._Node):
                return self._element >= other.element
            else:
                return self._element >= other

        def __le__(self, other):
            if isinstance(other, DoubleLinkedList._Node):
                return self._element <= other.element
            else:
                return self._element <= other

        def __del__(self):
            nxt = self.next
            prv = self.prev
            # Handle case where node is only one on the list (prv, nxt is None)
            if prv is None and nxt is None:
                # No switch is necessary
                pass
            # Handle case where node is head (prv is None)
            elif prv is None:
                nxt.prev = None
            # Handle case where node is tail (nxt is None)
            elif nxt is None:
                prv.next = None
            # Handle regular case where node has next and prev
            else:
                nxt.prev, prv.next = prv, nxt
            self._element = self.next = self.prev = None

        def get(self):
            return self._element

    def __init__(self, array: Optional[List] = None):
        self._head = None
        self._tail = None
        self._size = 0

        if isinstance(array, list):
            for x in array:
                self.append(x)

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, arg):
        if isinstance(arg, self._Node) or arg is None:
            self._head = arg
        else:
            raise TypeError('Invalid node assignment on head')

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, arg):
        if isinstance(arg, self._Node) or arg is None:
            self._tail = arg
        else:
            raise TypeError('Invalid node assignment on tail')

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        if self._size == 0:
            pass
        elif self._head:
            cursor = self._head
            while cursor is not None:
                yield cursor
                cursor = cursor.next

    def is_empty(self) -> bool:
        return self._size == 0

    # List interface
    def push(self, e: Any) -> None:
        """
        Creates a new "head" node at the beginning of the list with element "e"
        :param e: Any, element inside node's container
        """
        # Handle case where there is already a head node
        if self._head is not None:
            predecessor = self._head
            new = self._Node(e, nxt=predecessor, prv=None)
            predecessor._prev = new
            self._head = new
            self._size += 1

            # Handle case where the old head is the last element (new tail)
            if self._size == 2 and self._tail is None:
                self._tail = predecessor

        # Handle case where the list is empty
        elif self._size == 0:
            new = self._Node(e, nxt=None, prv=None)
            self._head = new
            self._size += 1

        # Handle case where there is unexpected error
        else:
            raise Exception('Unknown case')

    def append(self, e: Any) -> None:
        """
        Creates a new "tail" at the end of the list with element "e"
        :param e: Any, element inside node's container
        """
        # Handle case where there is already a tail node
        if self._tail is not None:
            predecessor = self._tail
            new = self._Node(e, nxt=None, prv=predecessor)
            self._tail = new
            self._size += 1
            predecessor._next = new

        # Handle case where list isn't empty and doesn't have a tail node yet
        elif self._tail is None and self._size == 1 and self._head:
            new = self._Node(e, nxt=None, prv=self._head)
            self._tail = new
            self._size += 1
            self._head._next = new

        # Handle case where the list is empty
        elif self._size == 0:
            new = self._Node(e, nxt=None, prv=None)
            self._head = new
            self._size += 1

        # Handle unexpected error
        else:
            raise Exception(f'Unknown case for append {e}')

    def insert_after(self, e: Any, node: _Node) -> None:
        """
        Inserts new element after specified node, if node is last on list, creates new tail
        :param e: Any, element inside node's container
        :param node: Node object for position reference in linked list
        """
        # Handle case where specified node is tail
        if node is self._tail:
            self.append(e)

        # Handle case where specified node is not tail
        elif isinstance(node, self._Node):
            # Handle case where node is head and no tail on the list (size 1)
            if node is self._head and self._head.next is None and self._size == 1:
                self.append(e)
            # Handle regular insert between nodes
            else:
                fwd = node.next
                new = self._Node(e, nxt=fwd, prv=node)
                self._size += 1
                # Reassign node order
                fwd._prev = new
                node._next = new

        # Handle unexpected error
        else:
            raise TypeError('Invalid node to insert after')

    def insert_before(self, e: Any, node: _Node) -> None:
        """
        Inserts new element before specified node, if node is first on list, creates new head
        :param e: Any, element inside node's container
        :param node: Node object for position reference in linked list
        """
        # Handle case where specified node is head
        if node is self._head:
            self.push(e)

        # Handle case where specified node is not head
        elif isinstance(node, self._Node):
            bef = node.prev
            new = self._Node(e, nxt=node, prv=bef)
            self._size += 1
            bef._next = new
            node._prev = new

        # Handle unexpected error
        else:
            raise Exception('Invalid node to insert before')

    def pop(self) -> _Node.element:
        """
        Returns and deletes the last element of the list
        """
        if self.tail:
            e = self.tail.get()
            # Handle case where there is a new tail
            if self.tail.prev and self._size > 2:
                successor = self.tail.prev
                del self._tail
                self.tail = successor
                self._size -= 1
            # Handle case where the tail is the last element after head
            if self.tail.prev and self._size == 2:
                del self._tail
                self.tail = None
                self._size -= 1
            return e
        elif self.tail is None and self._size == 1 and self.head:
            # Handle case where head is the only element
            e = self.head.get()
            del self._head
            self.head = None
            self._size -= 1
            return e
        else:
            raise ValueError('Linked list is empty')

    def pull(self) -> _Node.element:
        """
        Returns and deletes the first element of the list
        """
        if self.head:
            e = self.head.get()
            # Handle case where next element is not a tail
            if self.head.next and self._size > 2:
                successor = self.head.next
                successor.prev = None
                del self._head
                self.head = successor
                self._size -= 1
            # Handle case where next element is a tail (new head on linked list)
            if self.head.next and self._size == 2:
                successor = self.head.next
                successor.prev = None
                del self._head
                self._head = successor
                self._size -= 1
            # Handle case where head is the only element
            if self._size == 1:
                del self._head
                self._size -= 1
            return e
        else:
            raise ValueError('Linked list is empty')

    # def swap(self, n1: _Node, n2: _Node) -> None:
    #     """
    #     Swaps node positions
    #     :param n1: _Node type
    #     :param n2: _Node type
    #     """
    #     # Verify node integrity
    #     if not (isinstance(n1, self._Node) and isinstance(n2, self._Node)):
    #         raise TypeError('Invalid node parameters to swap')
    #     # Handle case where node 1 is tail
    #     elif n1.next is None:
    #         n2.next.prev = n1
    #         n2.prev.next = n1
    #         n1.next = n2.next
    #
    #         n1.prev.next = n2
    #         self.tail = n2

    # Getters
    def first(self):
        if self.head:
            return self.head.get()
        else:
            raise ValueError('List is empty or does not have a head')

    def last(self):
        if self.tail:
            return self.tail.get()
        else:
            raise ValueError('List is empty or does not have a tail')

    def get_median(self, start: _Node = None) -> _Node:
        """
        Returns the median node of the linked list
        """
        if start is None:
            start = self.head
        slow, fast = start, start.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def find(self, value: Any) -> _Node:
        """
        :param value: Any, value to be found inside a DLL node
        :return: Node object where value is found
        """
        if len(self) == 0:
            raise TypeError('List is empty')

        for x in self:
            if x.get() == value:
                return x

        raise ValueError('Value not found')

    # List reversals
    def reverse(self):
        """
        Reverses a linked list in O(n) time
        """
        new = DoubleLinkedList()
        for x in self:
            new.push(x)
        return new

    def reverse_rec(self, start: _Node):
        """
        Reverses a linked list recursively
        :param start: Node object to reverse
        """
        if len(self) > 999:
            raise RecursionError('List is too big, use standard reverse')
        if not isinstance(start, self._Node):
            raise TypeError('Reverse start is not a valid node object')
        cursor = start.next
        # Handle case where start node is head node and new tail node
        if cursor and start.prev is None:
            start.next = None
            start.prev = cursor
            self.tail = start
            self.reverse_rec(cursor)
        # Handle regular case where next and prev nodes are swapped
        elif cursor and start.prev:
            start.next = start.prev
            start.prev = cursor
            self.reverse_rec(cursor)
        # Handle base case where node is tail and new head node; recursive loop finished
        elif cursor is None and start.prev:
            start.next = start.prev
            start.prev = None
            self.head = start
        # Handle clase where start is the only node on the list
        elif start.prev is None and start.next is None:
            pass
        else:
            raise Exception('Unknown error')

    # Sorting utilities
    def _merge(self, l1: Union[None, _Node], l2: Union[None, _Node]) -> _Node:
        """
        Merges two ascending *sorted* linked lists
        :param l1: None, _Node
        :param l2: None, _Node
        :returns: merged _Node object
        """
        # If a node is none, list is sorted, return the other
        if l1 is None:
            # Tail assignment
            if l2 > self.tail:
                self.tail = l2
                return self.tail
            else:
                return l2
        elif l2 is None:
            # Tail assignment
            if l1 > self.tail:
                self.tail = l1
                return l1
            else:
                return l1

        # Compare min values of each list and merge remainder
        if l1 <= l2:
            l1.next = self._merge(l1.next, l2)
            l1.next.prev = l1
            l1.prev = None
            return l1
        else:
            l2.next = self._merge(l1, l2.next)
            l2.next.prev = l2
            l2.prev = None
            return l2

    def _merge_descending(self, l1: Union[None, _Node], l2: Union[None, _Node]):
        """
        Merges two descending *sorted* linked lists
        :param l1: None, _Node
        :param l2: None, _Node
        :returns: DoubleLinkedList
        """
        # If a node is none, list is sorted, return the other
        if l1 is None:
            # Tail assignment
            if l2 < self.tail:
                self.tail = l2
                return self.tail
            else:
                return l2
        elif l2 is None:
            # Tail assignment
            if l1 < self.tail:
                self.tail = l1
                return l1
            else:
                return l1
        # Compare max values of each list and merge remainder
        if l1 >= l2:
            l1.next = self._merge_descending(l1.next, l2)
            l1.next.prev = l1
            l1.prev = None
            return l1
        else:
            l2.next = self._merge_descending(l1, l2.next)
            l2.next.prev = l2
            l2.prev = None
            return l2

    def _inplace_merge(self, l1: _Node, l2: _Node, ascending: bool = True) -> _Node:
        """
        Merges two linked lists non recursively
        :param l1: first node of sublist 1
        :param l2: first node of sublist 2
        :returns: first node object of the merged linked lists
        """
        minimum = l1
        if ascending:
            while l1 and l2:
                # Handle case where elements are unsorted
                if l2 < l1:
                    # Point to next l2 element before swap
                    pointer = l2.next
                    # Swap
                    l2.next = l1
                    l2.prev = l1.prev
                    if l2.prev:
                        l2.prev.next = l2
                    else:
                        minimum = l2
                    l1.prev = l2
                    # Move loop to pointer
                    if pointer:
                        l2 = pointer
                    # Handle case where l2 is the last element
                    else:
                        # Tail assignment
                        while l1.next:
                            l1 = l1.next
                        self.tail = l1
                        break
                # Handle case where elements are sorted
                elif l1 <= l2:
                    # Move to next l1 sorted element
                    if l1.next:
                        l1 = l1.next
                    # Handle case where l1 is the last element
                    else:
                        l1.next = l2
                        l2.prev = l1
                        # Tail assignment
                        while l2.next:
                            l2 = l2.next
                        self.tail = l2
                        break
        else:
            while l1 and l2:
                # Handle case where elements are unsorted
                if l2 > l1:
                    # Point to next l2 element before swap
                    pointer = l2.next
                    # Swap
                    l2.next = l1
                    l2.prev = l1.prev
                    if l2.prev:
                        l2.prev.next = l2
                    else:
                        minimum = l2
                    l1.prev = l2
                    # Move loop to pointer
                    if pointer:
                        l2 = pointer
                    # Handle case where l2 is the last element
                    else:
                        # Tail assignment
                        while l1.next:
                            l1 = l1.next
                        self.tail = l1
                        break
                # Handle case where elements are sorted
                elif l1 >= l2:
                    # Move to next l1 sorted element
                    if l1.next:
                        l1 = l1.next
                    # Handle case where l1 is the last element
                    else:
                        l1.next = l2
                        l2.prev = l1
                        # Tail assignment
                        while l2.next:
                            l2 = l2.next
                        self.tail = l2
                        break
        return minimum

    # Sorting algorithms
    def _merge_sort(self, start: _Node, size: int, ascending=True, threshold: int = 50) -> Union[None, _Node]:
        """
        Returns a new double linked list sorted recursively
        :param start: linked list pointer
        :param size: int, keeps track of approximate size of list on recursive calls
        :param threshold: int, if list size <= threshold, start using insertion sort
        :param ascending: order of values
        :returns: starting node of sorted list
        """
        # Base case condition: no elements to be sorted
        if start is None or start.next is None:
            return start
        # Algorithm: Cut node's links, forcing them to be new lists a, b and sorting them recursively
        # Get first split list bounds
        a_head = start
        upper_bound = self.get_median(start=start)
        # Cut node's links
        b_head = upper_bound.next
        b_head.prev = None
        upper_bound.next = None

        # Sort new lists recursively or through insertion-sort if size <= threshold and merge
        if threshold > size:
            # Sort new sublists with insertion sort
            lower = self._insertion_sort(a_head, ascending)
            upper = self._insertion_sort(b_head, ascending)
        else:
            lower = self._merge_sort(a_head, int(size / 2), ascending)
            upper = self._merge_sort(b_head, int(size / 2), ascending)

        return self._inplace_merge(lower, upper, ascending)

    def _insertion_sort(self, start: _Node, ascending=True) -> Union[None, _Node]:
        """
        Sorts a double linked list starting from the provided node
        :param start: linked list start
        :param ascending: boolean, if false, list is sorted in descending order
        :returns: provided start node with all elements sorted
        """
        # Handle case where list is empty
        if len(self) == 0:
            raise ValueError('List is empty')
        # Handle case where head is the only node
        elif len(self) == 1:
            return start

        head = start
        if ascending:
            while start:
                cursor = start.next
                # Handle case where next value is already sorted
                if cursor and cursor.get() >= start.get():
                    start = cursor
                # Handle case where next value is not sorted
                elif cursor and cursor.get() < start.get():
                    # Get value and swap with sorted node
                    unsorted = cursor.get()
                    cursor.element = start.get()
                    start.element = unsorted

                    # Check with previous values
                    while start.prev and start.element < start.prev.get():
                        unsorted = start.get()
                        start.element = start.prev.get()
                        start.prev.element = unsorted

                        # Move backwards loop cursor
                        start = start.prev

                    # Once finished, move outer forward loop cursor
                    start = cursor
                # Handle case where cursor is None
                elif cursor is None:
                    break
        elif not ascending:
            while start:
                cursor = start.next
                # Handle case where next value is already sorted
                if cursor and cursor.get() <= start.get():
                    start = cursor
                # Handle case where next value is not sorted
                elif cursor and cursor.get() > start.get():
                    # Get value and swap with sorted node
                    unsorted = cursor.get()
                    cursor.element = start.get()
                    start.element = unsorted

                    # Check with previous values
                    while start.prev and start.element > start.prev.get():
                        unsorted = start.get()
                        start.element = start.prev.get()
                        start.prev.element = unsorted

                        # Move backwards loop cursor
                        start = start.prev

                    # Once finished, move outer forward loop cursor
                    start = cursor
                # Handle case where cursor is None
                elif cursor is None:
                    break
        return head

    def sort_values(self, method='merge', ascending=True):
        if method == 'merge':
            self.head = self._merge_sort(self.head, len(self), ascending)
            return self
        if method == 'insertion':
            self._insertion_sort(self.head, ascending)
            return self
