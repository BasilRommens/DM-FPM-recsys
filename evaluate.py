from recommendation import recommend_items


def evaluate_recommendations(test_data, user_items, rules, top_n=5,
                             rank_method='regular'):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    total_items = 0
    mrrs = 0
    count_persons = 0
    for user, input_items in test_data.items():
        # Get recommendations for the user based on the input items
        recommended_items = recommend_items(input_items, rules, top_n=top_n,
                                            rank_method=rank_method)
        recommended_items_s = set(recommended_items)

        # Assuming user_items is a dictionary with user IDs as keys and their associated items as values
        true_items = [user_items[user]]

        true_items = set(true_items)
        true_positives += len(recommended_items_s.intersection(true_items))
        false_positives += len(recommended_items_s - true_items)
        false_negatives += len(true_items - recommended_items_s)
        total_items += len(true_items)

        # calculate MRR
        for item in recommended_items:
            if item in true_items:
                mrrs += 1 / (recommended_items.index(item) + 1)
                break

        # count of persons with recommended items
        if len(recommended_items_s):
            count_persons += 1



    # Calculate precision, recall, and F1 score
    precision = true_positives / (true_positives + false_positives) \
        if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) \
        if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) \
        if (precision + recall) > 0 else 0

    # calculate MRR
    MRR = mrrs / len(test_data.items())

    # calculate HR
    HR = true_positives / count_persons

    # calculate ARHR
    ARHR = mrrs / count_persons

    return precision, recall, f1_score, MRR, HR, ARHR


if __name__ == '__main__':
    from apriori import association_rules

    input_items = {"A", "B"}
    user_items = []
    transactions = [
        {"A", "B", "C"},
        {"A", "B"},
        {"A", "C"},
        {"A"},
        {"B", "C"},
        {"B"},
        {"C"},
    ]
    min_support = 0.1
    min_confidence = 0.3
    rules = association_rules(transactions, min_support, min_confidence)
    test_data = {0: {"A"}}
    user_items = {0: {"A", "B"}}
    precision, recall, f1_score = evaluate_recommendations(test_data,
                                                           user_items, rules,
                                                           top_n=5)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 score:", f1_score)
