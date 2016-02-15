from collections import Counter

def range_factorization(N):
    primes = [2, 3, 5, 7, 11]
    result = dict()
    for num in range(1, N+1):
        num_remain = num
        local_result = Counter()
        for p in primes:
            if num_remain == 1:
                break
            if p**2 > num_remain:
                primes.append(num_remain)
                local_result[num_remain] += 1
                break
            while not num_remain%p:
                num_remain //= p
                local_result[p] += 1
        result[num] = local_result
    return result

def product(c):
    result = 1
    for k, v in c.items():
        result *= k**v
    return result

if __name__ == "__main__":
    result = range_factorization(100)
    for k in sorted(result):
        print(k, result[k], product(result[k]))