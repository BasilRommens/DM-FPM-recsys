import os

import pandas as pd
from apriori import association_rules
from data import read_dataset, split_dataset, write_dataset
from evaluate import evaluate_recommendations


def task2_run():
    results_df = pd.DataFrame(
        {'min_support': [], 'min_confidence': [], 'rank_method': [],
         'combination_method': [], 'score_type': [], 'score': [], 'is_ndi': []})

    score_types = ['precision', 'recall', 'f1_score', 'MRR', 'HR', 'ARHR']
    for min_confidence in [0.001, 0.003, 0.005, 0.007, 0.01, 0.02, 0.05, 0.1]:
        min_support = 0.005
        # generate the association rules
        rules = association_rules(train, min_support, min_confidence)

        # evaluate
        for rank_method in ['regular', 'popularity', 'product', 'interest',
                            'all_confidence']:
            for combination_method in ['sum', 'max', 'min']:
                precision, recall, f1_score, MRR, HR, ARHR = \
                    evaluate_recommendations(test, user_items, rules, top_n=100,
                                             rank_method=rank_method,
                                             combination_method=combination_method)
                scores = [precision, recall, f1_score, MRR, HR, ARHR]
                results_df = pd.concat([results_df, pd.DataFrame(
                    {'min_support': [min_support] * 6,
                     'min_confidence': [min_confidence] * 6,
                     'rank_method': [rank_method] * 6,
                     'score_type': score_types,
                     'is_ndi': [True] * 6, 'score': scores,
                     'combination_method': [combination_method] * 6})])
    results_df.to_csv('results2.csv', index=False)


def task3_run():
    results_df = pd.DataFrame(
        {'min_support': [], 'min_confidence': [], 'rank_method': [],
         'combination_method': [], 'score_type': [], 'score': [], 'is_ndi': []})

    score_types = ['precision', 'recall', 'f1_score', 'MRR', 'HR', 'ARHR']
    for min_support in range(10, 200, 20):
        # min_support = 0.005
        min_confidence = 0.01
        # generate the association rules
        rules = association_rules(train, min_support, min_confidence,
                                  fname=f'data/bf-{min_support}.dat')

        # evaluate
        for rank_method in ['regular', 'popularity', 'product', 'interest',
                            'all_confidence']:
            for combination_method in ['sum', 'max', 'min']:
                precision, recall, f1_score, MRR, HR, ARHR = \
                    evaluate_recommendations(test, user_items, rules, top_n=100,
                                             rank_method=rank_method,
                                             combination_method=combination_method)
                scores = [precision, recall, f1_score, MRR, HR, ARHR]
                results_df = pd.concat([results_df, pd.DataFrame(
                    {'min_support': [min_support] * 6,
                     'min_confidence': [min_confidence] * 6,
                     'rank_method': [rank_method] * 6,
                     'score_type': score_types,
                     'is_ndi': [True] * 6, 'score': scores,
                     'combination_method': [combination_method] * 6})])
    results_df.to_csv('results2.csv', index=False)


if __name__ == '__main__':
    # create the dataset
    transactions = read_dataset('data/retail.dat')
    train, test, user_items = split_dataset(transactions, test_size=0.2)

    # write the train to data/retail-train.dat
    write_dataset(train, 'data/retail-train.dat')

    # ndi generation with both bf and df
    for ndi_type in ['bf', 'df']:
        for support in range(10, 200, 10):
            os.system(
                f'ndi/{ndi_type}/ndi data/retail-train.dat {support} 3 data/{ndi_type}-{support}.dat')
    task2_run()
    task3_run()
