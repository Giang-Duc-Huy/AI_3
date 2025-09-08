import heapq, random

# Heuristic 
def heuristic(board):
    """Đếm số cặp quân hậu tấn công nhau trong board"""
    N = len(board)
    queens = [(r, c) for r in range(N) for c in range(N) if board[r][c] == 1]
    conflicts = 0
    for i in range(len(queens)):
        for j in range(i + 1, len(queens)):
            r1, c1 = queens[i]
            r2, c2 = queens[j]
            if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                conflicts += 1
    return conflicts

def get_successors(board, row):
    """Thêm 1 queen vào hàng row"""
    N = len(board)
    successors = []
    for col in range(N):
        new_board = [r[:] for r in board]
        new_board[row][col] = 1
        successors.append(new_board)
    return successors

# Greedy Best-First Search
def greedy_best_first(N):
    empty_board = [[0] * N for _ in range(N)]
    pq = []
    heapq.heappush(pq, (heuristic(empty_board), 0, empty_board))
    
    while pq:
        h, row, board = heapq.heappop(pq)
        if row == N and h == 0:
            return board
        for succ in get_successors(board, row):
            heapq.heappush(pq, (heuristic(succ), row + 1, succ))
    return None

# A* Search

def a_star(N):
    empty_board = [[0] * N for _ in range(N)]
    pq = []
    heapq.heappush(pq, (heuristic(empty_board), 0, empty_board))
    
    while pq:
        f, row, board = heapq.heappop(pq)
        if row == N and heuristic(board) == 0:
            return board
        for succ in get_successors(board, row):
            g2 = row + 1
            h2 = heuristic(succ)
            f2 = g2 + h2
            heapq.heappush(pq, (f2, g2, succ))
    return None

# ACO cho N-Queens
def conflicts_vec(board):
    N = len(board)
    cnt = 0
    for i in range(N):
        for j in range(i+1, N):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                cnt += 1
    return cnt

def aco_nqueens(N, num_ants=20, max_iter=200, alpha=1, beta=2, rho=0.5, Q=100):
    pheromone = [[1.0 for _ in range(N)] for _ in range(N)]
    best_solution = None
    best_conflicts = float("inf")

    for _ in range(max_iter):
        solutions = []
        for _ in range(num_ants):
            board = []
            for row in range(N):
                probs = []
                for col in range(N):
                    tau = pheromone[row][col] ** alpha
                    eta = 1.0 / (1 + conflicts_vec(board + [col])) if board else 1
                    probs.append(tau * (eta ** beta))
                s = sum(probs)
                probs = [p/s for p in probs]

                r = random.random()
                cumulative = 0
                for col in range(N):
                    cumulative += probs[col]
                    if r <= cumulative:
                        board.append(col)
                        break
            solutions.append(board)

        # Bay hơi pheromone
        for i in range(N):
            for j in range(N):
                pheromone[i][j] *= (1 - rho)

        # Cập nhật pheromone theo lời giải
        for board in solutions:
            c = conflicts_vec(board)
            if c < best_conflicts:
                best_conflicts = c
                best_solution = board
            if c == 0:
                return board
            for row, col in enumerate(board):
                pheromone[row][col] += Q / (1 + c)

    return best_solution

# Hàm in bàn cờ

def print_board_matrix(board):
    N = len(board)
    for r in range(N):
        print(" ".join("Q" if board[r][c] == 1 else "." for c in range(N)))
    print()

def print_board_vector(board):
    N = len(board)
    for r in range(N):
        print(" ".join("Q" if board[r] == c else "." for c in range(N)))
    print()

# =============================
# Main
# =============================
if __name__ == "__main__":
    N = 8
    
    print("=== Greedy Best-First Search ===")
    sol1 = greedy_best_first(N)
    if sol1: print_board_matrix(sol1)
    else: print("No solution found\n")

    print("=== A* Search ===")
    sol2 = a_star(N)
    if sol2: print_board_matrix(sol2)
    else: print("No solution found\n")

    print("=== Ant Colony Optimization ===")
    sol3 = aco_nqueens(N)
    if sol3: print_board_vector(sol3)
    else: print("No solution found\n")
