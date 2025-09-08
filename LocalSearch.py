from simpleai.search import SearchProblem
from simpleai.search.local import hill_climbing, simulated_annealing, genetic
import random



# Định nghĩa N-Queens Problem

class NQueensProblem(SearchProblem):
    def __init__(self, N):
        self.N = N
        # trạng thái: danh sách [col0, col1, ..., colN-1] (hàng i đặt hậu ở cột col[i])
        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))
        super().__init__(initial_state)

    def actions(self, state):
        """Mỗi action = (row, new_col) => di chuyển hậu ở hàng row sang cột new_col"""
        actions = []
        for row in range(self.N):
            for col in range(self.N):
                if state[row] != col:
                    actions.append((row, col))
        return actions

    def result(self, state, action):
        """Trả về state mới sau khi áp dụng action"""
        row, col = action
        new_state = list(state)
        new_state[row] = col
        return tuple(new_state)

    def value(self, state):
        """Giá trị = số cặp hậu KHÔNG tấn công nhau (càng cao càng tốt)"""
        return self.max_pairs() - self.conflicts(state)

  
    # Helper

    def conflicts(self, state):
        cnt = 0
        for i in range(self.N):
            for j in range(i + 1, self.N):
                if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                    cnt += 1
        return cnt

    def max_pairs(self):
        """Số cặp hậu tối đa (N choose 2)"""
        return self.N * (self.N - 1) // 2

    def generate_random_state(self):
        """Cần cho GA, SA"""
        return tuple(random.randint(0, self.N - 1) for _ in range(self.N))

# In bàn cờ
def print_board(state):
    N = len(state)
    for r in range(N):
        print(" ".join("Q" if state[r] == c else "." for c in range(N)))
    print()

# Main

if __name__ == "__main__":
    N = 8
    problem = NQueensProblem(N)

    print("=== Hill Climbing ===")
    result_hc = hill_climbing(problem)
    print_board(result_hc.state)
    print("Conflicts:", problem.conflicts(result_hc.state))

    print("=== Simulated Annealing ===")
    result_sa = simulated_annealing(problem)
    print_board(result_sa.state)
    print("Conflicts:", problem.conflicts(result_sa.state))

    print("=== Genetic Algorithm ===")
    result_ga = genetic(problem, population_size=200, mutation_chance=0.2)
    print_board(result_ga.state)
    print("Conflicts:", problem.conflicts(result_ga.state))
