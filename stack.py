class Stack:

    def __init__(self, items=None):
        if items is not None:
            if isinstance(items, list):
                self.__items = items
                self.length = len(items)
            else:
                raise TypeError("items must be a list") 
        else:
            self.__items = []
            self.length = 0

    def push(self, item):
        self.__items.append(item)
        self.length += 1

    def pop(self):
        if self.length == 0:
            raise IndexError("Stack is empty")
        self.length -= 1
        return self.__items.pop()

    def peek(self):
        if self.length == 0:
            return None
        return self.__items[self.length-1]

    def size(self) -> int:
        return self.length
    
    def is_empty(self) -> bool:
        return self.length == 0

    def __iter__(self):
        return iter(self.__items)

    def __str__(self) -> str:
        return f"Stack: {[x for x in self.__items]}"

    def __repr__(self) -> str:
        return f"Stack: {[x for x in self.__items]}"

    def __len__(self) -> int:
        return self.length

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Stack):
            return False
        return self.__items == __o.__items