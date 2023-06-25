def recommend_items(input_items, rules, top_n=5, rank_method='regular',
                    combination_method='sum'):
    recommendations = {}
    for antecedent, consequent, support, confidence, support_antecedent, support_consequent, all_confidence in rules:
        if antecedent.issubset(input_items) and not consequent.issubset(
                input_items):
            for item in consequent:
                if item not in input_items:
                    if item not in recommendations:
                        recommendations[item] = []
                    recommendations[item].append((confidence, support,
                                                  support_antecedent,
                                                  support_consequent,
                                                  all_confidence))

    if combination_method == 'sum':  # average all the item rules
        recommendations = {
            item: (
            sum(conf for conf, _, _, _, _ in item_rules) / len(item_rules),
            sum(sup for _, sup, _, _, _ in item_rules) / len(item_rules),
            sum(sup_ant for _, _, sup_ant, _, _ in item_rules) / len(
                item_rules),
            sum(sup_con for _, _, _, sup_con, _ in item_rules) / len(
                item_rules),
            sum(all_conf for _, _, _, _, all_conf in item_rules) / len(
                item_rules
            ))
            for item, item_rules in recommendations.items()
        }
    elif combination_method == 'max':  # max all the item rules
        recommendations = {
            item: (max(conf for conf, _, _, _, _ in item_rules),
                   max(sup for _, sup, _, _, _ in item_rules),
                   max(sup_ant for _, _, sup_ant, _, _ in item_rules),
                   max(sup_con for _, _, _, sup_con, _ in item_rules),
                   max(all_conf for _, _, _, _, all_conf in item_rules))
            for item, item_rules in recommendations.items()
        }
    elif combination_method == 'min':  # min all the item rules
        recommendations = {
            item: (min(conf for conf, _, _, _, _ in item_rules),
                   min(sup for _, sup, _, _, _ in item_rules),
                   min(sup_ant for _, _, sup_ant, _, _ in item_rules),
                   min(sup_con for _, _, _, sup_con, _ in item_rules),
                   min(all_conf for _, _, _, _, all_conf in item_rules))
            for item, item_rules in recommendations.items()
        }

    descending = True
    if rank_method == 'regular':  # sort by confidence then support
        sorted_recommendations = sorted(recommendations.items(),
                                        key=lambda x: (x[1][0], x[1][1]),
                                        reverse=descending)
    elif rank_method == 'product':  # sort by product of confidence and support
        sorted_recommendations = sorted(recommendations.items(),
                                        key=lambda x: x[1][0] * x[1][1],
                                        reverse=descending)
    elif rank_method == 'popularity':  # sort by support
        sorted_recommendations = sorted(recommendations.items(),
                                        key=lambda x: x[1][1],
                                        reverse=descending)
    elif rank_method == 'interest':  # sort by interest
        sorted_recommendations = sorted(recommendations.items(),
                                        key=lambda x: x[1][1] / (
                                                x[1][2] * x[1][3]),
                                        reverse=descending)
    elif rank_method == 'all_confidence':  # sort by all confidence
        sorted_recommendations = sorted(recommendations.items(),
                                        key=lambda x: x[1][4],
                                        reverse=descending)

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
