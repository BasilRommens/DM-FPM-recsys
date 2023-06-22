from itertools import chain, combinations, filterfalse

from tqdm import tqdm

from data import read_ndi


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def _join_set(itemsets, k):
    return set(
        [itemset1.union(itemset2)
         for itemset1 in itemsets
         for itemset2 in itemsets
         if len(itemset1.union(itemset2)) == k]
    )


def join_set(itemsets, k):
    new_itemsets = set()
    for itemset1 in itemsets:
        for itemset2 in itemsets:
            candidate = itemset1.union(itemset2)
            if len(candidate) != k:
                continue
            for item in candidate:
                subset = candidate - frozenset([item])
                if subset not in itemsets:
                    break
            new_itemsets.add(candidate)
    return new_itemsets


def itemsets_support(transactions, itemsets, min_support):
    support_count = {itemset: 0 for itemset in itemsets}
    for transaction in transactions:
        for itemset in itemsets:
            if itemset.issubset(transaction):
                support_count[itemset] += 1
    n_transactions = len(transactions)
    return {itemset: support / n_transactions for itemset, support in
            support_count.items() if
            support / n_transactions >= min_support}


def apriori(transactions, min_support):
    items = set(chain(*transactions))
    itemsets = [frozenset([item]) for item in items]
    itemsets_by_length = [set()]
    k = 1
    while itemsets:
        # get candidates with minimum support
        support_count = itemsets_support(transactions, itemsets, min_support)
        itemsets_by_length.append(set(support_count.keys()))
        itemsets = list(support_count.keys())
        k += 1

        # generate new candidates
        itemsets = join_set(itemsets, k)
        # print('og method')
        # itemsets = _join_set(itemsets, k)
    frequent_itemsets = set(chain(*itemsets_by_length))
    return frequent_itemsets, itemsets_by_length


def association_rules(transactions, min_support, min_confidence, fname=None):
    if fname is None:
        frequent_itemsets, itemsets_by_length = apriori(transactions,
                                                        min_support)
        print(len(frequent_itemsets))
    else:
        frequent_itemsets, itemsets_by_length = read_ndi(fname)

    rules = []
    for itemset in tqdm(frequent_itemsets):
        for subset in filterfalse(lambda x: not x, powerset(itemset)):
            antecedent = frozenset(subset)
            consequent = itemset - antecedent
            if not consequent:
                continue
            support_antecedent = len(
                [t for t in transactions if antecedent.issubset(t)]) / len(
                transactions)
            support_consequent = len(
                [t for t in transactions if consequent.issubset(t)]) / len(
                transactions)
            support_itemset = len(
                [t for t in transactions if itemset.issubset(t)]) / len(
                transactions)
            confidence = support_itemset / support_antecedent
            if confidence >= min_confidence:
                rules.append(
                    (antecedent, consequent, support_itemset, confidence,
                     support_antecedent, support_consequent))
    return rules


if __name__ == '__main__':
    import time

    # Example usage
    transactions = [
        {1, 2, 3, 4},
        {1, 2, 4},
        {1, 2},
        {2, 3, 4},
        {2, 3},
        {3, 4},
        {2, 4}
    ]
    transactions = transactions
    min_support = 3 / 7
    min_confidence = 0.5
    start = time.time()
    rules = association_rules(transactions, min_support, min_confidence)
    print(f'Time taken: {time.time() - start} seconds''')
    for antecedent, consequent, support, confidence in rules:
        print(
            f"{antecedent} => {consequent} (support={support:.2f}, confidence={confidence:.2f})")
