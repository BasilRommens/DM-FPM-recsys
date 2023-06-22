import pandas as pd

if __name__ == '__main__':
    from apriori import association_rules
    from data import read_dataset, split_dataset, write_dataset
    from evaluate import evaluate_recommendations

    # create the dataset
    transactions = read_dataset('data/retail.dat')
    train, test, user_items = split_dataset(transactions, test_size=0.2)

    # write the train to data/retail-train.dat
    # write_dataset(train, 'data/retail-train.dat')
    results_df = pd.DataFrame(
        {'min_support': [], 'min_confidence': [], 'rank_method': [],
         'score_type': [], 'score': [], 'is_ndi': []})

    score_types = ['precision', 'recall', 'f1_score', 'MRR', 'HR', 'ARHR']
    for min_confidence in [0, 0.003, 0.005, 0.007, 0.01, 0.02, 0.05, 0.1]:
        min_support = 0.005
        # generate the association rules
        rules = association_rules(train, min_support, min_confidence)
                                  # fname='data/bf-150.dat')

        # evaluate
        for rank_method in ['regular', 'product', 'popularity', 'interest']:
            precision, recall, f1_score, MRR, HR, ARHR = \
                evaluate_recommendations(test, user_items, rules, top_n=20,
                                         rank_method=rank_method)
            scores = [precision, recall, f1_score, MRR, HR, ARHR]
            results_df = pd.concat([results_df, pd.DataFrame(
                {'min_support': [min_support] * 6,
                 'min_confidence': [min_confidence] * 6,
                 'rank_method': [rank_method] * 6, 'score_type': score_types,
                 'is_ndi': [False] * 6, 'score': scores})])
    results_df.to_csv('results.csv')
