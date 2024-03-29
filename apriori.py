from itertools import chain, combinations, filterfalse

from tqdm import tqdm

from data import read_ndi


def powerset(iterable):
    # generate a powerset of the iterable
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def _join_set(itemsets, k):
    # old join of set
    return set(
        [itemset1.union(itemset2)
         for itemset1 in itemsets
         for itemset2 in itemsets
         if len(itemset1.union(itemset2)) == k]
    )


def join_set(itemsets, k):
    new_itemsets = set()

    # iterate over all the possible combinations of the sets
    for itemset1 in itemsets:
        for itemset2 in itemsets:
            # generate a condidate of length k
            candidate = itemset1.union(itemset2)
            if len(candidate) != k:
                continue

            # check if all the subsets of candidate are in itemsets
            too_little_itemset = False  # check for subset not in itemsets
            for item in candidate:
                subset = candidate - frozenset([item])
                if subset not in itemsets:
                    too_little_itemset = True
                    break

            # if all the subsets of candidate are in itemsets, add candidate
            if not too_little_itemset:
                new_itemsets.add(candidate)

    return new_itemsets


def itemsets_support(transactions, itemsets, min_support):
    # calculate the support of the itemsets

    # support count per itemset
    support_count = {itemset: 0 for itemset in itemsets}

    # iterate over all transactions to add to the count if the itemset is
    # a subset of the transaction
    for transaction in transactions:
        for itemset in itemsets:
            if itemset.issubset(transaction):
                support_count[itemset] += 1

    # the number of transactions
    n_transactions = len(transactions)

    # convert the support to the percentage support
    return {itemset: support / n_transactions for itemset, support in
            support_count.items() if
            support / n_transactions >= min_support}


def apriori(transactions, min_support):
    # perform the apriori algorithm
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
        # calculate the maximum support in the itemset only possible from
        # singletons
        max_support = float('-inf')
        for singleton in itemset:
            singleton = frozenset({singleton})
            singleton_support = len(
                [t for t in transactions if singleton.issubset(t)])
            max_support = singleton_support if singleton_support > max_support else max_support

        # generate all the possible antecedents and consequents
        for subset in filterfalse(lambda x: not x, powerset(itemset)):
            antecedent = frozenset(subset)
            consequent = itemset - antecedent
            if not consequent:  # skip if no consequent
                continue

            # calculate the support and the confidences
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
            all_confidence = support_itemset / max_support

            # store the supports and the confidences if confidence is above
            # the minimum confidence
            if confidence >= min_confidence:
                rules.append(
                    (antecedent, consequent, support_itemset, confidence,
                     support_antecedent, support_consequent, all_confidence))
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
