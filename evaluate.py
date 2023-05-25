from recommendation import recommend_items


def evaluate_recommendations(test_data, user_items, rules, top_n=5,
                             rank_method='regular'):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    for user, true_items in test_data.items():
        # Assuming user_items is a dictionary with user IDs as keys and their associated items as values
        input_items = user_items[user]

        # Get recommendations for the user based on the input items
        recommended_items = set(
            recommend_items(input_items, rules, top_n=top_n,
                            rank_method=rank_method))
        true_items = set(true_items)
        true_positives += len(recommended_items.intersection(true_items))
        false_positives += len(recommended_items - true_items)
        false_negatives += len(true_items - recommended_items)

    # Calculate precision, recall, and F1 score
    precision = true_positives / (true_positives + false_positives) \
        if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) \
        if (true_positives + false_negatives) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) \
        if (precision + recall) > 0 else 0

    return precision, recall, f1_score


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
