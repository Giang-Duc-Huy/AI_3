import heapq
import random

# Trạng thái đích
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]

moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def find_pos(state, value):
    for i in range(3):
        for j in range(3):
            if state[i][j] == value:
                return i, j
    return None


def heuristic_manhattan(state):
    h = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                gi, gj = find_pos(goal_state, val)
                h += abs(i - gi) + abs(j - gj)
    return h


def state_to_tuple(state):
    return tuple(num for row in state for num in row)


def is_goal(state):
    return state == goal_state


def get_neighbors(state):
    neighbors = []
    x, y = find_pos(state, 0)
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors


def inversion_count(state):
    flat = [num for row in state for num in row if num != 0]
    inv = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inv += 1
    return inv


def is_solvable(state):
    return inversion_count(state) % 2 == 0


def generate_random_solvable():
    arr = list(range(9))
    while True:
        random.shuffle(arr)
        st = [arr[0:3], arr[3:6], arr[6:9]]
        if is_solvable(st) and st != goal_state:
            return st


def greedy_best_first(start, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start), start, []))
    visited = set()
    while frontier:
        h, state, path = heapq.heappop(frontier)
        if is_goal(state):
            return path + [state]
        visited.add(state_to_tuple(state))
        for neighbor in get_neighbors(state):
            t = state_to_tuple(neighbor)
            if t not in visited:
                heapq.heappush(frontier, (heuristic(neighbor), neighbor, path + [state]))
    return None


def a_star(start, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start), 0, start, []))
    visited = set()
    while frontier:
        f, g, state, path = heapq.heappop(frontier)
        if is_goal(state):
            return path + [state]
        visited.add(state_to_tuple(state))
        for neighbor in get_neighbors(state):
            t = state_to_tuple(neighbor)
            if t not in visited:
                g_new = g + 1
                f_new = g_new + heuristic(neighbor)
                heapq.heappush(frontier, (f_new, g_new, neighbor, path + [state]))
    return None


def print_path(path):
    if path is None:
        print("No solution found.")
        return
    for step in path:
        for row in step:
            print(row)
        print("------")
    print("Solution length:", len(path) - 1)


# ------------------- MAIN -------------------
print("=== 8 Puzzle Solver ===")

start_state = [[2, 8, 3],
               [1, 6, 4],
               [7, 0, 5]]

print("Start state:")
for r in start_state:
    print(r)
print("Inversions:", inversion_count(start_state))

if not is_solvable(start_state):
    print("⚠️ This puzzle is UNSOLVABLE. Generating random solvable puzzle...")
    start_state = generate_random_solvable()
    for r in start_state:
        print(r)
    print("Inversions:", inversion_count(start_state))

print("\nGreedy Best-First Search (Manhattan):")
path = greedy_best_first(start_state, heuristic_manhattan)
print_path(path)

print("\nA* Search (Manhattan):")
path = a_star(start_state, heuristic_manhattan)
print_path(path)
