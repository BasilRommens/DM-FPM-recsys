def recommend_items(input_items, rules, top_n=5, rank_method='regular'):
    recommendations = {}
    for antecedent, consequent, support, confidence in rules:
        if antecedent.issubset(input_items) and not consequent.issubset(
                input_items):
            for item in consequent:
                if item not in input_items:
                    if item not in recommendations:
                        recommendations[item] = []
                    recommendations[item].append((confidence, support))

    recommendations = {
        item: (sum(conf for conf, _ in item_rules) / len(item_rules),
               sum(sup for _, sup in item_rules) / len(item_rules))
        for item, item_rules in recommendations.items()
    }

    if rank_method == 'regular':  # sort by confidence then support
        sorted_recommendations = sorted(recommendations.items(),
                                        key=lambda x: (x[1][0], x[1][1]),
                                        reverse=True)
    elif rank_method == 'product':  # sort by product of confidence and support
        sorted_recommendations = sorted(recommendations.items(),
                                        key=lambda x: x[1][0] * x[1][1],
                                        reverse=True)
    elif rank_method == 'popularity':  # sort by support
        sorted_recommendations = sorted(recommendations.items(),
                                        key=lambda x: x[1][1],
                                        reverse=True)

    for item, _ in sorted_recommendations:
        print(item)
    return [item for item, _ in sorted_recommendations[:top_n]]


if __name__ == '__main__':
    from apriori import association_rules

    input_items = {"A", "B"}
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
    recommended_items = recommend_items(input_items, rules)
    print("Recommended items:", recommended_items)
