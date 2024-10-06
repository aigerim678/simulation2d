
from entities import Grass, Rock, Tree, Herbivore, Predator
from map import Map


class Simulation():
    def __init__(self, map_obj):
        self.map = map_obj

    def next_turn(self):
        # Итерируемся по каждому существу на карте
        for position, entity in list(self.map.map.items()):
            if isinstance(entity, (Herbivore, Predator)):
                entity.make_move(self.map, position)
        self.render()

    def render(self):
        grid = [['--' for _ in range(self.map.width)] for _ in range(self.map.height)]
        for (x, y), entity in self.map.map.items():
            grid[y][x] = str(entity)
        for row in grid:
            print(' '.join(row))
        print("\n")

    def start_simulation(self, turns):
        for turn in range(turns):
            print(f"Turn {turn + 1}:")
            self.next_turn()


# Размеры карты
width, height = 10, 10

# Создаем карту
world_map = Map(width, height)

# Рандомно размещаем объекты
world_map.place_randomly(Rock, 3)     
world_map.place_randomly(Herbivore, 2)
world_map.place_randomly(Grass, 5)    
world_map.place_randomly(Predator, 2)     
instance = Simulation(world_map)
instance.start_simulation(10)