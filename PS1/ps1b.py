###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_top_down(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #TOP-DOWN SOLUTION
    min_eggs = target_weight
    
    #base case
    if target_weight in egg_weights:
        return 1
    
    #test to see if we've already calculated this weight
    try:
        return memo[target_weight]
    
    #if it's not calculated and stored in memo already
    except KeyError:
        for egg in egg_weights:
            if egg<target_weight:
                egg_count = 1 + dp_top_down(egg_weights, target_weight-egg, memo)
                if egg_count < min_eggs:
                    min_eggs = egg_count
                    memo[target_weight] = min_eggs
        return min_eggs
        

            
def dp_bottom_up(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    #BOTTOM_UP SOLUTION    
    for weight in range(1,target_weight+1):
        
        if weight in egg_weights:
            memo[weight] = 1
            
        else: 
            egg_count = weight
            memo[weight] = weight
            for egg in egg_weights:
                if egg < weight and memo[weight - egg] + 1 < egg_count:
                    egg_count = memo[weight - egg] + 1
                    memo[weight] = egg_count
        
    return memo[target_weight]
    

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (5, 10, 25)
    n = 45
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output (with top-down dp):", dp_top_down(egg_weights, n))
    print("Actual output (with bottom-up dp):", dp_bottom_up(egg_weights, n))
    print()