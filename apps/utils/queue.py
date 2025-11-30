class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        """Agregar elemento al final de la cola"""
        self.items.append(item)

    def dequeue(self):
        """Sacar el primer elemento de la cola"""
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def peek(self):
        """Ver el primer elemento sin sacarlo"""
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
    
    def ver_cola(self):
        # Devuelve copia de la lista interna para no modificar la cola
        return list(self.items)
