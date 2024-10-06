from random import randint

from entities import Grass, Rock, Tree, Herbivore, Predator

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = {}

    def is_occupied(self, position, entity_type):
        entity = self.map.get(position)  # Получаем объект на позиции
        return isinstance(entity, entity_type)
    
    def move_entity(self, old_pos, new_pos):
        self.map[new_pos] = self.map[old_pos]
        del self.map[old_pos]

    def remove_entity(self, position):
        """Удаление сущности с карты (травоядное или траву)"""
        if position in self.map:
            del self.map[position]

    def place_randomly(self, entity, count):
        for _ in range(count):
            while True:
                # Генерируем случайные координаты
                x = randint(0, self.width - 1)
                y = randint(0, self.height - 1)
                position = (x, y)
                
                # Проверяем, что клетка не занята
                if not self.is_occupied(position, (Grass, Rock, Tree, Predator, Herbivore)):
                    self.map[position] = entity()
                    break
            
    def get_neighbors(self, position):
        """Возвращает список соседних клеток"""
        x, y = position
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (x + dx, y + dy)
            if 0 <= new_pos[0] < self.width and 0 <= new_pos[1] < self.height:
                neighbors.append(new_pos)
        return neighbors
    
