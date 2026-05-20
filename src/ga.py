import random
import logging
import inspect
import numpy as np
import pygame
FRAME_DT = 16
MAX_GAME_TIME = 1500000     
MIN_ACCEPT_TIME = 300000     
IDEAL_START_TIME = 600000    
IDEAL_END_TIME = 900000      
GENE_RANGES = [
    [3,    5,    8],      # 0  airplane_speed
    [10,   15,   25],     # 1  bullet_width
    [5,    10,   15],     # 2  bullet_height
    [6,    8,    12],     # 3  bullet_speed
    [700,  1100, 1500],   # 4  bullet_calm_time
    [1.5,  2.5,  4],      # 5  enemy_speed
    [1500, 2000, 3000],   # 6  enemy_calm_time
    [15,   20,   40],     # 7  airplane_bullet_atk
    [10,   15,   25],     # 8  enemy_bullet_width
    [5,    10,   15],     # 9  enemy_bullet_height
    [3,    5,    8],      # 10 enemy_bullet_speed
    [3000, 4000, 6000],   # 11 enemy_bullet_calm_time
    [30,   50,   80],     # 12 collision_atk
    [5,    10,   20],     # 13 enemy_bullet_atk
    [10,   20,   40],     # 14 enemy_hp
    [10,   20,   40],     # 15 enemy_max_hp
    [80,   100,  200],    # 16 airplane_max_hp

    # 技能成长参数
    [0.2,  0.4,  0.6],    # 17 collision_percent
    [200,  400,  600],    # 18 bullet_calm_time_add
    [0,    1,    2],      # 19 bullet_speed_sub
    [2,    4,    6],      # 20 airplane_bullet_atk_sub
    [5,    10,   15],     # 21 bullet_width_add
    [0.05, 0.1,  0.15],   # 22 lifesteal_add
    [1,    2,    3],      # 23 airplane_speed_add
    [10,   20,   30],     # 24 bullet_atk_add
    [50,   100,  150],    # 25 hp_add
    [50,   100,  150],    # 26 max_hp_add
    [0,    1,    2],      # 27 bullet_speed_add
    [50,   100,  150],    # 28 bullet_calm_time_sub
    [0.05, 0.1,  0.15],   # 29 hp_heal_add
    [0,    1,    2],      # 30 defence_add
    [100,  200,  300],    # 31 enemy_bullet_calm_time_add
    [0,    1,    2],      # 32 lower_enemy_bullet_speed_add
    [0,    1,    2],      # 33 xp_add_add

    # 等级成长参数
    [5,    10,   20],     # 34 enemy_hp_per_level
    [5,    10,   20],     # 35 enemy_max_hp_per_level
    [0.2,  0.4,  0.8],    # 36 enemy_speed_per_level
    [5,    15,   30],     # 37 enemy_calm_time_reduce
    [20,   50,   100],    # 38 enemy_bullet_calm_time_reduce
    [5,    10,   20],     # 39 airplane_max_xp_add
    [5,    10,   20],     # 40 airplane_max_hp_add
    [5,    10,   20],     # 41 airplane_hp_add
    [2,    5,    10],     # 42 airplane_bullet_atk_add
]
INT_GENE_INDEXES = {
    1, 2, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16,
    18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 30,
    31, 32, 33, 34, 35, 37, 38, 39, 40, 41, 42
}
def I(x):
    return int(round(x))

def load_gene(settings, gene):
    s = settings
    s.airplane_speed = gene[0]
    s.bullet_width = I(gene[1])
    s.bullet_height = I(gene[2])
    s.bullet_speed = gene[3]
    s.bullet_calm_time = I(gene[4])
    s.enemy_speed = gene[5]
    s.enemy_calm_time = I(gene[6])
    s.airplane_bullet_atk = I(gene[7])
    s.enemy_bullet_width = I(gene[8])
    s.enemy_bullet_height = I(gene[9])
    s.enemy_bullet_speed = gene[10]
    s.enemy_bullet_calm_time = I(gene[11])
    s.collision_atk = I(gene[12])
    s.enemy_bullet_atk = I(gene[13])
    s.enemy_hp = I(gene[14])
    s.enemy_max_hp = I(gene[15])
    s.airplane_max_hp = I(gene[16])
    s.collision_percent = gene[17]
    s.bullet_calm_time_add = I(gene[18])
    s.bullet_speed_sub = I(gene[19])
    s.airplane_bullet_atk_sub = I(gene[20])
    s.bullet_width_add = I(gene[21])
    s.lifesteal_add = gene[22]
    s.airplane_speed_add = I(gene[23])
    s.bullet_atk_add = I(gene[24])
    s.hp_add = I(gene[25])
    s.max_hp_add = I(gene[26])
    s.bullet_speed_add = I(gene[27])
    s.bullet_calm_time_sub = I(gene[28])
    s.hp_heal_add = gene[29]
    s.defence_add = I(gene[30])
    s.enemy_bullet_calm_time_add = I(gene[31])
    s.lower_enemy_bullet_speed_add = I(gene[32])
    s.xp_add_add = I(gene[33])
    s.enemy_hp_per_level = I(gene[34])
    s.enemy_max_hp_per_level = I(gene[35])
    s.enemy_speed_per_level = gene[36]
    s.enemy_calm_time_reduce = I(gene[37])
    s.enemy_bullet_calm_time_reduce = I(gene[38])
    s.airplane_max_xp_add = I(gene[39])
    s.airplane_max_hp_add = I(gene[40])
    s.airplane_hp_add = I(gene[41])
    s.airplane_bullet_atk_add = I(gene[42])
    
class GeneticAlgorithm:
    def __init__(self, pop_size=60):
        self.pop_size = pop_size
        self.gene_length = len(GENE_RANGES)
        self.population = []
        self.fitnesses = []
    def init_population(self):
        self.population = []
        base_gene = [gr[1] for gr in GENE_RANGES]
        self.population.append(base_gene)
        for _ in range(self.pop_size - 1):
            gene = []
            for low, _, high in GENE_RANGES:
                gene.append(random.uniform(low, high))
            self.population.append(gene)
        self.fitnesses = [0] * self.pop_size

    def calculate_fitness(self, game_ctx):
        t = game_ctx.survive_time
        kills = game_ctx.count_tool.all_name.get("enemy_death", 0)
        if t < MIN_ACCEPT_TIME:
            time_score = t / MIN_ACCEPT_TIME * 10
        elif t < IDEAL_START_TIME:
            time_score = 10 + (t - MIN_ACCEPT_TIME) / (IDEAL_START_TIME - MIN_ACCEPT_TIME) * 50
        elif t <= IDEAL_END_TIME:
            time_score = 60
        else:
            time_score = max(
                0,
                60 * (1 - (t - IDEAL_END_TIME) / (MAX_GAME_TIME - IDEAL_END_TIME))
            )
        kill_score = min(kills / 120 * 40, 40)
        if t < MIN_ACCEPT_TIME:
            kill_score *= t / MIN_ACCEPT_TIME
        too_long_penalty = 0
        if t >= MAX_GAME_TIME:
            too_long_penalty = 15
        total = time_score + kill_score - too_long_penalty
        total = max(total, 0)
        logging.info(
            f"存活时间:{t}ms | 击杀:{kills} | "
            f"时间分:{time_score:.1f} | 击杀分:{kill_score:.1f} | "
            f"惩罚:{too_long_penalty:.1f} | 总分:{total:.1f}"
        )
        return total

    def selection(self):
        new_population = []
        tournament_size = min(5, self.pop_size)
        for _ in range(self.pop_size):
            aspirant_indices = random.sample(range(self.pop_size), tournament_size)
            best_idx = max(aspirant_indices, key=lambda i: self.fitnesses[i])
            new_population.append(self.population[best_idx].copy())
        return new_population

    def crossover(self, pop):
        new_pop = []
        for i in range(0, len(pop), 2):
            p1 = pop[i]
            p2 = pop[i + 1] if i + 1 < len(pop) else pop[i]
            if random.random() < 0.7:
                c1 = []
                c2 = []
                for g1, g2 in zip(p1, p2):
                    if random.random() < 0.5:
                        c1.append(g1)
                        c2.append(g2)
                    else:
                        c1.append(g2)
                        c2.append(g1)
                new_pop += [c1, c2]
            else:
                new_pop += [p1.copy(), p2.copy()]
        return new_pop[:self.pop_size]

    def mutation(self, pop):
        for gene in pop:
            for idx in range(self.gene_length):
                if random.random() < 0.03:
                    low, _, high = GENE_RANGES[idx]
                    gene[idx] += random.gauss(0, (high - low) * 0.05)
                    gene[idx] = float(np.clip(gene[idx], low, high))
        return pop

    def evolve(self, elite_gene=None):
        selected = self.selection()
        crossed = self.crossover(selected)
        mutated = self.mutation(crossed)
        if elite_gene is not None:
            mutated[0] = elite_gene.copy()
        self.population = mutated

def update_game_ctx(game_ctx, update_arg_count):
    if update_arg_count >= 2:
        game_ctx.update(game_ctx.sim_time, FRAME_DT)
    else:
        game_ctx.update(game_ctx.sim_time)

def run_one_game(game_ctx, gene, gen, run, update_arg_count):
    seed = gen * 1000 + run
    random.seed(seed)
    np.random.seed(seed)
    load_gene(game_ctx.settings, gene)
    game_ctx.reset_game(
        0,
        target_state="play",
        auto_mode=True,
        reset_settings=False
    )
    while not game_ctx.game_over and game_ctx.survive_time < MAX_GAME_TIME:
        pygame.event.pump()
        update_game_ctx(game_ctx, update_arg_count)
    return game_ctx

def log_best_gene(best_gene, best_fitness):
    logging.info("\n" + "=" * 60)
    logging.info("🎯 历史最优数值（直接复制到 Settings）🎯")
    logging.info(f"历史最优分数: {best_fitness:.2f}")
    logging.info("=" * 60)
    logging.info(f"self.airplane_speed = {best_gene[0]:.2f}")
    logging.info(f"self.bullet_width = {I(best_gene[1])}")
    logging.info(f"self.bullet_height = {I(best_gene[2])}")
    logging.info(f"self.bullet_speed = {best_gene[3]:.2f}")
    logging.info(f"self.bullet_calm_time = {I(best_gene[4])}")
    logging.info(f"self.enemy_speed = {best_gene[5]:.2f}")
    logging.info(f"self.enemy_calm_time = {I(best_gene[6])}")
    logging.info(f"self.airplane_bullet_atk = {I(best_gene[7])}")
    logging.info(f"self.enemy_bullet_width = {I(best_gene[8])}")
    logging.info(f"self.enemy_bullet_height = {I(best_gene[9])}")
    logging.info(f"self.enemy_bullet_speed = {best_gene[10]:.2f}")
    logging.info(f"self.enemy_bullet_calm_time = {I(best_gene[11])}")
    logging.info(f"self.collision_atk = {I(best_gene[12])}")
    logging.info(f"self.enemy_bullet_atk = {I(best_gene[13])}")
    logging.info(f"self.enemy_hp = {I(best_gene[14])}")
    logging.info(f"self.enemy_max_hp = {I(best_gene[15])}")
    logging.info(f"self.airplane_max_hp = {I(best_gene[16])}")
    logging.info(f"self.collision_percent = {best_gene[17]:.2f}")
    logging.info(f"self.bullet_calm_time_add = {I(best_gene[18])}")
    logging.info(f"self.bullet_speed_sub = {I(best_gene[19])}")
    logging.info(f"self.airplane_bullet_atk_sub = {I(best_gene[20])}")
    logging.info(f"self.bullet_width_add = {I(best_gene[21])}")
    logging.info(f"self.lifesteal_add = {best_gene[22]:.2f}")
    logging.info(f"self.airplane_speed_add = {I(best_gene[23])}")
    logging.info(f"self.bullet_atk_add = {I(best_gene[24])}")
    logging.info(f"self.hp_add = {I(best_gene[25])}")
    logging.info(f"self.max_hp_add = {I(best_gene[26])}")
    logging.info(f"self.bullet_speed_add = {I(best_gene[27])}")
    logging.info(f"self.bullet_calm_time_sub = {I(best_gene[28])}")
    logging.info(f"self.hp_heal_add = {best_gene[29]:.2f}")
    logging.info(f"self.defence_add = {I(best_gene[30])}")
    logging.info(f"self.enemy_bullet_calm_time_add = {I(best_gene[31])}")
    logging.info(f"self.lower_enemy_bullet_speed_add = {I(best_gene[32])}")
    logging.info(f"self.xp_add_add = {I(best_gene[33])}")
    logging.info(f"self.enemy_hp_per_level = {I(best_gene[34])}")
    logging.info(f"self.enemy_max_hp_per_level = {I(best_gene[35])}")
    logging.info(f"self.enemy_speed_per_level = {best_gene[36]:.2f}")
    logging.info(f"self.enemy_calm_time_reduce = {I(best_gene[37])}")
    logging.info(f"self.enemy_bullet_calm_time_reduce = {I(best_gene[38])}")
    logging.info(f"self.airplane_max_xp_add = {I(best_gene[39])}")
    logging.info(f"self.airplane_max_hp_add = {I(best_gene[40])}")
    logging.info(f"self.airplane_hp_add = {I(best_gene[41])}")
    logging.info(f"self.airplane_bullet_atk_add = {I(best_gene[42])}")
    logging.info("=" * 60)

def run_ga(game_ctx):
    ga = GeneticAlgorithm(pop_size=10)
    ga.init_population()
    generations = 3
    runs_per_gene = 1
    best_gene = None
    best_fitness = -1
    update_arg_count = len(inspect.signature(game_ctx.update).parameters)
    for gen in range(generations):
        print(f"\n===== 第 {gen + 1} 代 =====")
        logging.info(f"\n===== 第 {gen + 1} 代 =====")
        for i in range(ga.pop_size):
            gene = ga.population[i]
            scores = []
            for run in range(runs_per_gene):
                run_one_game(
                    game_ctx,
                    gene,
                    gen,
                    run,
                    update_arg_count
                )
                score = ga.calculate_fitness(game_ctx)
                scores.append(score)
            avg_score = sum(scores) / len(scores)
            ga.fitnesses[i] = avg_score
            if avg_score > best_fitness:
                best_fitness = avg_score
                best_gene = gene.copy()
            logging.info(f"个体 {i} 平均分: {avg_score:.2f}")
        logging.info(f"第 {gen + 1} 代结束，历史最优分: {best_fitness:.2f}")
        ga.evolve(elite_gene=best_gene)
    log_best_gene(best_gene, best_fitness)
    return best_gene