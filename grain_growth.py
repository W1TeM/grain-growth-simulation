import numpy as np
import matplotlib.pyplot as plt
import time
import argparse
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import copy

class GrainSimulation:
    """
    Simple simulation and vizualization of crystalization process based on Moore neighborhood. 
    Optimized with NumPy vectorization. Input is length and width of the field and number of 
    starting crystalization grains. 

    """
    def __init__(self, length: int, width: int, num_grains: int, pbc: bool, nucl_rate: int):
        
        self.length = length
        self.width = width
        self.num_grains = num_grains
        self.pbc = pbc
        self.nucl_rate = nucl_rate

        self.field_matr = np.zeros((self.length, self.width), dtype=np.int16)
        self.current_max_id = self.num_grains

        self.seed_grains()
    
        rand_colors = (np.random.rand(1000, 3) + 0.5) / 1.5
        self.my_cmap = ListedColormap(rand_colors)
        self.my_cmap.set_under('white')
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

    def evol_step_vectorized(self):
        empty_y, empty_x = np.where(self.field_matr == 0) #ищем все пустые клетки
        actual_nucl = min(self.nucl_rate, len(empty_y)) #смотрим сколько новых зародышей реально поместится
        if actual_nucl > 0:
        # Генерируем случайные индексы от 0 до количества пустых клеток
            random_indices = np.random.choice(len(empty_y), size=actual_nucl, replace=False)
    
            # Достаем конкретные координаты X и Y по этим случайным индексам
            chosen_y = empty_y[random_indices]
            chosen_x = empty_x[random_indices]
            # Создаем список новых ID (например: [51, 52, 53...])
            new_ids = np.arange(self.current_max_id + 1, self.current_max_id + 1 + actual_nucl)
    
            #Кладем список ID ровно в список выбранных координат!
            self.field_matr[chosen_y, chosen_x] = new_ids
    
            # Не забываем обновить счетчик для следующего такта
            self.current_max_id += actual_nucl


        #ищем соседей базовых
        left_neighb = np.roll(self.field_matr, 1, 1)
        right_neighb = np.roll(self.field_matr, -1, 1)
        top_neighb = np.roll(self.field_matr,  1, 0)
        bottom_neighb = np.roll(self.field_matr, -1, 0)
        #ищем соседей по диагонали
        top_left_neighb = np.roll(left_neighb, 1, 0)
        bottom_left_neighb = np.roll(left_neighb, -1, 0)
        top_right_neighb = np.roll(right_neighb, 1, 0)
        bottom_right_neighb = np.roll(right_neighb, -1, 0)

        if not self.pbc: #если включено условие жёстких границ, то нужно обрезать края матриц, чтоб не перелазило на другую сторону
            left_neighb[:, 0] = 0
            right_neighb[:, -1] = 0
            top_neighb[0, :] = 0
            bottom_neighb[-1, :] = 0
            top_left_neighb[0, :] = 0
            top_left_neighb[:, 0] = 0
            top_right_neighb[0, :] = 0
            top_right_neighb[:, -1] = 0
            bottom_left_neighb[-1, :] = 0
            bottom_left_neighb[ :, 0] = 0
            bottom_right_neighb[-1, :] = 0
            bottom_right_neighb[:, -1] = 0

        empty_mask = (self.field_matr == 0)

        all_neighb = [left_neighb, right_neighb, top_neighb, bottom_neighb,
                       top_left_neighb, top_right_neighb, bottom_left_neighb, bottom_right_neighb]
        
        random_dirs = np.random.randint(0, 8, size=(np.shape(self.field_matr)))
        chosen_neighb = np.choose(random_dirs, all_neighb)

        self.field_matr = np.where((empty_mask) & (chosen_neighb > 0), chosen_neighb, self.field_matr)

    def display(self):
        # Создаем визуальную матрицу и сразу ее рисуем
        vis_matr = np.where(self.field_matr == 0, 0, (self.field_matr % 1000) + 1)
        plt.imshow(vis_matr, cmap=self.my_cmap, vmin=0.5, vmax=1000.5)
        plt.show()

    def animate(self):
        fig, ax = plt.subplots()
        
        # Для самого первого кадра тоже нужна красивая матрица!
        vis_matr = np.where(self.field_matr == 0, 0, (self.field_matr % 1000) + 1)
        img = ax.imshow(vis_matr, cmap=self.my_cmap, vmin=0.5, vmax=1000.5)

        def update(frame):
            self.evol_step_vectorized()
            vis_matr = np.where(self.field_matr == 0, 0, (self.field_matr % 1000) + 1)
            img.set_data(vis_matr)
            
            if not (0 in self.field_matr):
                ani.event_source.stop()
            return [img]

        ani = animation.FuncAnimation(fig, update, interval=50, blit=False)
        plt.show()

    def save_gif(self, filename="grains.gif"):
        fig, ax = plt.subplots()
        
        vis_matr = np.where(self.field_matr == 0, 0, (self.field_matr % 1000) + 1)
        img = ax.imshow(vis_matr, cmap=self.my_cmap, vmin=0.5, vmax=1000.5)

        def frame_gen():
            i = 0
            while 0 in self.field_matr:
                yield i
                i += 1

        def update(frame):
            self.evol_step_vectorized()
            vis_matr = np.where(self.field_matr == 0, 0, (self.field_matr % 1000) + 1)
            img.set_data(vis_matr)
            return [img]

        ani = animation.FuncAnimation(fig, update, frames=frame_gen, interval=50, blit=False, cache_frame_data=False)
        ani.save(filename, writer='pillow', fps=15)

        
if __name__ == '__main__':
    #парсим параметры CLI при запуске скрипта, чтобы с клавиатуры не вводить
    parser = argparse.ArgumentParser(description='Fast Grain Growth Simulation')
    parser.add_argument('--length', type=int, default=200, help='Length of the grid')
    parser.add_argument('--width', type=int, default=200, help='Width of the grid')
    parser.add_argument('--grains', type=int, default=50, help='Number of starting grains')
    parser.add_argument('--mode', choices=['static', 'animate', 'save'], default = 'animate', help='Mode of vizualization')
    parser.add_argument('--file_name', default='grains.gif', type=str, help='Name of your file')
    parser.add_argument('--pbc', action='store_true')
    parser.add_argument('--nucl_rate', type=int, default=0, help='How much new grains will be geberated in each simulations step')

    args = parser.parse_args()
    if args.length <= 0 or args.width <= 0 or args.grains <= 0:
        parser.error("Size of field and number of grains must be positive numbers")
    my_sim = GrainSimulation(args.length, args.width, args.grains, args.pbc, args.nucl_rate)

    start_time = time.time()

    if args.mode == 'animate':
        my_sim.animate()
    elif args.mode == 'static':
        while 0 in my_sim.field_matr:
            my_sim.evol_step_vectorized()
        my_sim.display()
        
    else:
        my_sim.save_gif(args.file_name)

    end_time = time.time()
    print(end_time - start_time)
    

   