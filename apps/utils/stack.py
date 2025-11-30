class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)  # Agregar acción al final

    def pop(self):
        if not self.is_empty():
            return self.items.pop()  # Sacar última acción
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]  # Ver la última acción
        return None

    def is_empty(self):
        return len(self.items) == 0
