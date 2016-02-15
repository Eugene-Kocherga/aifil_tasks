def even_vector_divide(V, M):
    N = len(V)
    part_size = N//M
    remain_size = N%M
    return [V[shift*part_size+remain_size//2: (shift+1)*part_size+remain_size//2] for shift in range(M)]

if __name__ == "__main__":
    for sub_vector in even_vector_divide(range(100), 7):
        print(len(sub_vector), sub_vector)