import numpy as np
import matplotlib.pyplot as plt
import time

class GrainSimulation:
    """
    Simple simulation and vizualization of crystalization process based on Moore neighborhood. 
    Optimized with NumPy vectorization. Input is length and width of the field and number of 
    starting crystalization grains. 

    """
    def __init__(self, length: int, width: int, num_grains: int):
        
        self.length = length
        self.width = width
        self.num_grains = num_grains
        
        self.field_matr = np.zeros((self.length, self.width), dtype=np.int8)

        self.seed_grains()
    
    def seed_grains(self):  # с ввода получаем сколько зёрен нам надо, и раскидываем их по рандомным координатам сетки
        if self.num_grains > self.field_matr.size:  # проверяем хватит ли места в сетке
            print("Error. Grid is too small for your ambitions. Make bigger grid.")

        i = 1 # начинаем с 1 потому что ID = 0 это пустота

        while i <= self.num_grains:
            x_coord = np.random.randint(0, self.length)
            y_coord = np.random.randint(0, self.width)

            if (self.field_matr[x_coord, y_coord] == 0):  # проверяем что позиция пуста и ставим туда зерно с уникальным ID
                self.field_matr[x_coord, y_coord] = i
                i += 1

    # def evol_step(self):
    #     new_field = np.copy(self.field_matr)
    #     length = new_field.shape[0]
    #     width = new_field.shape[1]

    #     for x in range(length):
    #         for y in range(width):
    #             if self.field_matr[x, y] == 0:
    #                 left = self.field_matr[x - 1, y]
    #                 right = self.field_matr[(x + 1) % length, y]
    #                 top = self.field_matr[x, y - 1]
    #                 bottom = self.field_matr[x, (y + 1) % width]

    #                 neighbors = [left, right, top, bottom]

    #                 active_neighbors = [i for i in neighbors if i > 0]

    #                 if len(active_neighbors) != 0:
    #                     new_field[x, y] = np.random.choice(active_neighbors)
    #     self.field_matr = new_field
    
    def evol_step_vectorized(self):
        left_neighb = np.roll(self.field_matr, 1, 1)
        right_neighb = np.roll(self.field_matr, -1, 1)
        top_neighb = np.roll(self.field_matr,  1, 0)
        bottom_neighb = np.roll(self.field_matr, -1, 0)

        top_left_neighb = np.roll(left_neighb, 1, 0)
        bottom_left_neighb = np.roll(left_neighb, -1, 0)
        top_right_neighb = np.roll(right_neighb, 1, 0)
        bottom_right_neighb = np.roll(right_neighb, -1, 0)

        empty_mask = (self.field_matr == 0)

        all_neighb = [left_neighb, right_neighb, top_neighb, bottom_neighb,
                       top_left_neighb, top_right_neighb, bottom_left_neighb, bottom_right_neighb]
        
        random_dirs = np.random.randint(0, 8, size=(np.shape(self.field_matr)))
        chosen_neighb = np.choose(random_dirs, all_neighb)

        self.field_matr = np.where((empty_mask) & (chosen_neighb > 0), chosen_neighb, self.field_matr)

    def display(self): 
        plt.imshow(self.field_matr)
        plt.show()



if __name__ == '__main__':
    my_sim = GrainSimulation(2000, 2000, 100)
    start_time = time.time()
    while 0 in my_sim.field_matr:
        my_sim.evol_step_vectorized()
    end_time = time.time()
    print(end_time - start_time)
    my_sim.display()