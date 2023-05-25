if __name__ == '__main__':
    from apriori import association_rules
    from data import read_dataset, split_dataset
    from evaluate import evaluate_recommendations

    # create the dataset
    transactions = read_dataset('data/retail.dat')
    train, test_data, user_items = split_dataset(transactions, 0.8)

    # generate the association rules
    min_support = 0.002
    min_confidence = 0.5
    rules = association_rules(train, min_support, min_confidence)

    # remove the rules with a confidence below min_confidence
    rules = [rule for rule in rules if rule[3] >= min_confidence]

    # evaluate
    precision, recall, f1_score = evaluate_recommendations(test_data,
                                                           user_items, rules,
                                                           top_n=5,
                                                           rank_method='product')
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 score:", f1_score)
