from abc import ABC, abstractmethod
from collections import deque
from random import choice, randint

class Entity(ABC):
    pass


class Grass(Entity):
    def __str__(self):
        return '🌱'
        

class Rock(Entity):
    def __str__(self):
        return '⬛️'

class Tree(Entity):
    def __str__(self):
        return '🌲'

class Creature(Entity):
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.hp = 5

    @abstractmethod
    def make_move():
        pass


class Herbivore(Creature):
    def __str__(self):
        return '🦒'

    def make_move(self, map_obj, position):
        # Ищем ближайшую траву
        target = find_closest(map_obj, position, Grass)
        if target:
            new_position = move_towards(position, target)
            if new_position != position and not map_obj.is_occupied(new_position, (Rock, Tree, Herbivore, Predator)):
                # Проверяем, что на новой позиции трава, а не хищник
                if isinstance(map_obj.map.get(new_position), Grass):
                    # Травоядное "съедает" траву
                    map_obj.remove_entity(new_position)
                map_obj.move_entity(position, new_position)
        else:
            # Если нет цели, движемся случайно
            new_position = move_randomly(map_obj, position)
            if new_position != position and not map_obj.is_occupied(new_position, (Rock, Tree, Herbivore, Predator)):
                map_obj.move_entity(position, new_position)

class Predator(Creature):
    def __str__(self):
        return '🐻'

    def make_move(self, map_obj, position):
        # Ищем ближайшего травоядного
        target = find_closest(map_obj, position, Herbivore)
        if target:
            new_position = move_towards(position, target)
            if new_position != position and not map_obj.is_occupied(new_position, (Grass, Rock, Tree, Predator)):
                # Если на новой позиции травоядное, хищник его съедает
                if isinstance(map_obj.map.get(new_position), Herbivore):
                    map_obj.remove_entity(new_position)
                map_obj.move_entity(position, new_position)
        else:
            # Если нет цели, движемся случайно
            new_position = move_randomly(map_obj, position)
            if new_position != position:
                map_obj.move_entity(position, new_position)
        



def find_closest(map_obj, start, target_type):
    queue = deque([start])  # очередь для BFS
    visited = {start}

    while queue:
        x, y = queue.popleft()

        # Если нашли объект нужного типа
        if isinstance(map_obj.map.get((x, y)), target_type):
            return (x, y)

        for neighbor in map_obj.get_neighbors((x, y)):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return None

def move_towards(start, target):
    x1, y1 = start
    x2, y2 = target

    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):  # Двигаемся по X
        return (x1 + (1 if dx > 0 else -1), y1)
    elif abs(dy) > abs(dx):  # Двигаемся по Y
        return (x1, y1 + (1 if dy > 0 else -1))
    else:  # Если расстояние одинаковое по обеим осям, выбираем случайное направление
        if randint(0, 1) == 0:
            return (x1 + (1 if dx > 0 else -1), y1)
        else:
            return (x1, y1 + (1 if dy > 0 else -1))

def move_randomly(map_obj, position):
    """Случайное движение, если цели нет"""
    neighbors = map_obj.get_neighbors(position)
    # Выбираем случайного соседа, который не занят
    random_neighbor = choice([pos for pos in neighbors if not map_obj.is_occupied(pos, (Herbivore, Predator, Grass, Tree, Rock))])
    return random_neighbor

