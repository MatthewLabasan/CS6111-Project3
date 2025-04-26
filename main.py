import sys
import csv
from collections import defaultdict
from itertools import combinations

def apriori(transactions, min_sup):
    """
    Apriori algorithm from Fast Algorithms for Mining Association Rules, Agrawal and Srikant in VLDB
    
    Args:
        transactions (list): List containing tuples holding each row of data, split and cleaned
        min_sup (float): Minimum support

    Returns:
        all_candidates (dict): Dictionary of frequent itemsets and their support
        
    """
    item_counts = defaultdict(int)
    n = len(transactions)

    # First pass: count support for individual items
    for transaction in transactions:
        for item in transaction:
            item_counts[(item,)]+=1
    L = []
    L1 = {}
    # Keep only items that meet minimum support
    for item, c in item_counts.items():
        if c / n >= min_sup:
            L1[item] = c
    
    L.append(L1)
    k = 2 # Iteration itemsetstarting size

    while True:
        # Get the list of frequent itemsets from the prev. iteration
        last_L = list(L[-1].keys())
        candidates = set()

        # Generate new candidate itemsets (of len + 1) from previous itemsets
        for i in range(len(last_L)):
            for j in range(i+1, len(last_L)):
                # Create new itemsets
                union = set(last_L[i]) | set(last_L[j])
                union_tuple = tuple(sorted(union)) 
                if len(union_tuple) != k: # Remove if too big
                     continue
                
                # Prune step
                prune = True
                for subset in combinations(union_tuple, k-1): 
                     if tuple(sorted(subset)) not in last_L:
                          prune = False
                          break
                if prune == True: # All subsets are frequent
                     candidates.add(union_tuple)
        
        # Get support counts for candidate itemsets (counts are more efficient)
        support_count = defaultdict(int)
        for transaction in transactions:
            items = set(transaction)
            for candidate in candidates:
                if set(candidate).issubset(items):
                    support_count[candidate]+=1
        
        # Keep candidates of size k that meet minimum support
        L_k = {}
        for candidate, count in support_count.items():
            if count / n >= min_sup:
                L_k[candidate] = count

        if not L_k:
            break

        k+=1
        L.append(L_k)
    
    # Normalize support values to percentages
    all_candidates = {}
    for l_k in L:
        for candidate, count in l_k.items():
            all_candidates[candidate] = count / n

    return all_candidates

def get_association_rules(candidates, min_conf):
    """
    Returns high-confidence association rules from frequent itemsets.

    Args:
        candidates (dict): Keys are frequent itemsets (as tuples)and values are their support values (between 0 and 1).
        min_conf (float): Minimum confidence threshold (between 0 and 1).

    Returns:
        rules (list(tuples)): Each tuple represents a rule in the format 
                            (left_side, right_side, support, confidence)
    """
    rules = []

    # Check each candidates confidence
    for candidate in candidates:
        # Skip itemsets with single item
        if len(candidate) < 2:
            continue

        # Get support of the full itemset (denominator of confidence)
        support = candidates[candidate]

        # Try every possible split of itemset into left and right sides
        for i in range(1, len(candidate)):
            for left_side in combinations(candidate, i):
                # Build right side
                right_side = set(candidate) - set(left_side)
                right_side = tuple(sorted(right_side))

                # Get the support of the left side (numerator of confidence)
                left_support = candidates.get(tuple(sorted(left_side)), 0)
                if left_support == 0:
                    continue

                # Calculate confidence
                conf = support / left_support
                if conf >= min_conf:
                    rules.append((left_side, right_side, support, conf))
    return rules

def print_results(frequent, rules, min_sup, min_conf):
    """
    Helper function to print results neatly.

    Args:
        frequent (dict): Dictionary where keys are frequent itemsets (tuples) and values are their support values.
        rules (list(tuples)): Each tuple represents a rule in the format 
                            (left_side, right_side, support, confidence)
        min_sup (float): Minimum support (between 0 and 1).
        min_conf (float): Minimum confidence (between 0 and 1).
    """
    print(f"==Frequent itemsets (min_sup={min_sup*100}%)")
    for item, support in sorted(frequent.items(), key = lambda x: (-x[1], x[0])):
        # Convert tuple to clean string
        item_str = ', '.join(item)
        print(f"[{item_str}], {support*100}%")
    print(f"==High-confidence association rules (min_conf={min_conf*100}%)")
    for lhs, rhs, support, conf in sorted(rules, key = lambda x: (-x[3], x[0])):
        # Convert tuples to clean strings
        lhs_str = ', '.join(lhs)
        rhs_str = ', '.join(rhs)
        print(f"[{lhs_str}]=>[{rhs_str}] (Conf: {conf*100}%, Supp: {support*100}%)")

def main():
    try:
        file_name = sys.argv[1]
        min_sup = float(sys.argv[2])
        min_conf = float(sys.argv[3])

        with open(file_name, 'r', newline='', encoding='utf-8') as data:
            read = csv.reader(data)
            transactions = []
            i = 0
            for line in read:
                i+=1
                stripped_items = [item.strip() for item in line if item.strip()]
                transactions.append(tuple(sorted(stripped_items)))
        if min_sup < 0 or min_sup > 1:
            raise ValueError(f"min_sup has to be between 0 and 1. input value:  {min_sup}")
        if min_conf < 0 or min_conf > 1:
            raise ValueError(f"min_conf has to be between 0 and 1. input value:  {min_conf}")
    except Exception as e:
        print(e)
        print("Usage : python3 main.py <data path> <min_sup> <min_conf>")
    candidates = apriori(transactions, min_sup)
    rules = get_association_rules(candidates, min_conf)
    print_results(candidates, rules, min_sup, min_conf)
if __name__ == "__main__":
    main()