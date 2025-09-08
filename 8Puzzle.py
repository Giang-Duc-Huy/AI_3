import heapq

# Trạng thái đích
goal_state = [[1,2,3],
              [4,5,6],
              [7,8,0]]

# Các hướng di chuyển: lên, xuống, trái, phải
moves = [(-1,0),(1,0),(0,-1),(0,1)]

def find_pos(state, value):
    """Tìm vị trí (x,y) của 1 số trong ma trận"""
    for i in range(3):
        for j in range(3):
            if state[i][j] == value:
                return i, j
    return None

def heuristic_misplaced(state):
    """Heuristic 1: số ô sai chỗ"""
    h = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                h += 1
    return h

def heuristic_manhattan(state):
    """Heuristic 2: tổng khoảng cách Manhattan"""
    h = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                goal_i, goal_j = find_pos(goal_state, val)
                h += abs(i - goal_i) + abs(j - goal_j)
    return h

def state_to_tuple(state):
    """Chuyển từ ma trận sang tuple để lưu trong set"""
    return tuple([num for row in state for num in row])

def is_goal(state):
    return state == goal_state

def get_neighbors(state):
    """Sinh trạng thái kề"""
    neighbors = []
    x, y = find_pos(state, 0)  # tìm ô trống
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def greedy_best_first(start, heuristic):
    """Greedy Best First Search"""
    frontier = []
    heapq.heappush(frontier, (heuristic(start), start, []))
    visited = set()
    
    while frontier:
        h, state, path = heapq.heappop(frontier)
        if is_goal(state):
            return path + [state]
        visited.add(state_to_tuple(state))
        for neighbor in get_neighbors(state):
            if state_to_tuple(neighbor) not in visited:
                heapq.heappush(frontier, (heuristic(neighbor), neighbor, path + [state]))
    return None

def a_star(start, heuristic):
    """A* Search"""
    frontier = []
    heapq.heappush(frontier, (heuristic(start), 0, start, []))  # (f, g, state, path)
    visited = set()
    
    while frontier:
        f, g, state, path = heapq.heappop(frontier)
        if is_goal(state):
            return path + [state]
        visited.add(state_to_tuple(state))
        for neighbor in get_neighbors(state):
            if state_to_tuple(neighbor) not in visited:
                g_new = g + 1
                f_new = g_new + heuristic(neighbor)
                heapq.heappush(frontier, (f_new, g_new, neighbor, path + [state]))
    return None

def print_path(path):
    for step in path:
        for row in step:
            print(row)
        print("------")

# ------------------- TEST -------------------
start_state = [[2,8,3],
               [1,6,4],
               [7,0,5]]

print("Greedy Best-First Search (Manhattan):")
path = greedy_best_first(start_state, heuristic_manhattan)
print_path(path)

print("A* Search (Manhattan):")
path = a_star(start_state, heuristic_manhattan)
print_path(path)
