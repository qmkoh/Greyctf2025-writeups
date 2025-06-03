import sys
input = sys.stdin.readline

def main():
    n = int(input())
    categories = list(map(int, input().split()))
    
    satisfaction = {
        (0,1): 2,
        (1,2): 5,
        (0,2): 3,
        (1,0): 4,
        (2,0): 1,
        (2,1): 6
    }
    
    NEG_INF = -10**15
    dp = [NEG_INF]*3
    
    get_satis = satisfaction.get  # local ref to speed up
    
    for c in categories:
        new_dp = dp[:]
        if new_dp[c] < 0:
            new_dp[c] = 0  # start subsequence here if better
        
        for prev in range(3):
            prev_val = dp[prev]
            if prev_val != NEG_INF:
                val = prev_val + get_satis((prev,c), 0)
                if val > new_dp[c]:
                    new_dp[c] = val
        
        dp = new_dp
    
    print(max(dp))

if __name__ == "__main__":
    main()
