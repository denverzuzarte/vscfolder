def solve_lis_problem():
    def max_lis_length(l, r, k):
        """
        Find maximum LIS length for arrays of length k
        where a[i] must be in range [l[i], r[i]]
        """
        # Greedy approach: try to extend current sequence as much as possible
        lis_length = 0
        last_value = 0  # Start with 0 (smaller than any valid value)
        
        for i in range(k):
            # Try to extend current sequence
            # Choose the smallest value >= last_value that's in valid range
            next_value = max(l[i], last_value)
            
            if next_value <= r[i]:
                # We can extend the current sequence
                last_value = next_value
                if i == 0 or next_value >= last_value:
                    lis_length += 1
            else:
                # Can't extend, start new sequence
                last_value = l[i]
                lis_length += 1
        
        return lis_length
    
    def solve_optimized(l, r, n):
        """
        Optimized solution using the key insight:
        The maximum LIS length for length k is the number of positions
        where we can't continue the previous increasing sequence
        """
        results = []
        
        for k in range(1, n + 1):
            lis_length = 1  # At least one element
            last_value = l[0]  # Start with minimum possible value at position 0
            
            for i in range(1, k):
                # Check if we can continue the sequence
                needed_value = last_value  # We need at least this value
                
                if needed_value <= r[i]:
                    # We can continue the sequence
                    last_value = max(l[i], needed_value)
                else:
                    # Must start a new increasing subsequence
                    lis_length += 1
                    last_value = l[i]
            
            results.append(lis_length)
        
        return results
    
    # Read input
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        l = []
        r = []
        
        for i in range(n):
            li, ri = map(int, input().split())
            l.append(li)
            r.append(ri)
        
        # Solve for each k from 1 to n
        results = solve_optimized(l, r, n)
        
        # Output results
        for result in results:
            print(result, end=' ')
        print()  # New line after each test case

def test_with_example():
    """
    Test function with a sample case
    """
    print("Testing with example:")
    print("Input:")
    print("1")  # 1 test case
    print("3")  # n = 3
    print("1 2")  # l[0]=1, r[0]=2
    print("1 3")  # l[1]=1, r[1]=3  
    print("2 4")  # l[2]=2, r[2]=4
    
    # Manual calculation:
    # k=1: array [1 or 2] -> LIS length = 1
    # k=2: array [1-2, 1-3] -> best is [1,1] or [1,2] or [1,3] -> LIS length = 2
    # k=3: array [1-2, 1-3, 2-4] -> best is [1,1,2] or [1,2,2] etc -> LIS length = 3
    
    print("\nExpected output: 1 2 3")
    
    # Let's trace through the algorithm:
    l = [1, 1, 2]
    r = [2, 3, 4]
    n = 3
    
    print("\nTracing through algorithm:")
    for k in range(1, n + 1):
        print(f"\nFor k={k}:")
        lis_length = 1
        last_value = l[0]
        print(f"  Start: lis_length=1, last_value={last_value}")
        
        for i in range(1, k):
            needed_value = last_value
            print(f"  Position {i}: need >= {needed_value}, range is [{l[i]}, {r[i]}]")
            
            if needed_value <= r[i]:
                last_value = max(l[i], needed_value)
                print(f"    Can continue sequence, new last_value = {last_value}")
            else:
                lis_length += 1
                last_value = l[i]
                print(f"    Must start new sequence, lis_length = {lis_length}, last_value = {last_value}")
        
        print(f"  Final LIS length for k={k}: {lis_length}")

# Uncomment the line below to run the test
# test_with_example()

# Uncomment the line below to run the actual solution
# solve_lis_problem()