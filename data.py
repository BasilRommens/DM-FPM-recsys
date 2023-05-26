import numpy as np


def read_dataset(file_name):
    # the row on which the data starts is the transaction id
    # the rest of the row is the items in the transaction
    with open(file_name, 'r') as f:
        dataset = [set(line.strip().split()) for line in f.readlines()]

    return dataset


def read_ndi(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()[1:]

    ls_of_freq_itemsets = [set(line.split(" (")[0].split()) for line in lines]

    # convert the frequent itemsets to integers instead of strings
    new_ls_of_freq_itemsets = []
    for freq_itemset in ls_of_freq_itemsets:
        new_ls_of_freq_itemsets.append(set([int(item) for item in freq_itemset]))

    # create a set of same length itemsets
    itemsets_by_length = dict()
    for itemset in new_ls_of_freq_itemsets:
        if len(itemset) not in itemsets_by_length:
            itemsets_by_length[len(itemset)] = list()
        itemsets_by_length[len(itemset)].append(itemset)

    itemsets_by_length = list(itemsets_by_length.values())

    return new_ls_of_freq_itemsets, itemsets_by_length


def split_dataset(data_set: list, test_size):
    assert 0 < test_size < 1
    n_test_els = int(len(data_set) * test_size)
    n_train_els = len(data_set) - n_test_els

    # get the training dataset
    train_data = data_set[:n_train_els]

    # set the random choice seed to be the same for each run
    np.random.seed(42)

    # create the test dataset
    # get the last element of each of the test dataset elements
    user_items = dict()
    user_item_indices = [0 for _ in range(len(data_set[n_train_els:]))]
    for i, test_el in enumerate(data_set[n_train_els:]):
        if len(test_el) > 1:
            item_index = np.random.randint(0, len(test_el))
            user_item_indices[i] = item_index
            user_items[i] = sorted(list(test_el))[item_index]

    # remove the last element of each of the test dataset elements
    test_data = dict()
    for i, test_el in enumerate(data_set[n_train_els:]):
        if len(test_el) > 1:
            test_data[i] = test_el - set(
                sorted(list(test_el))[user_item_indices[i]])

    return train_data, test_data, user_items


if __name__ == '__main__':
    # transactions = read_dataset('data/retail.dat')
    # print(transactions)
    #
    # train, test_data, user_items = split_dataset(transactions, 0.2)
    # print(train)
    # print(test_data)
    # print(user_items)
    frequent_itemsets, itemsets_by_length = read_ndi("data/bf-190.dat")
    print(frequent_itemsets)
    print(itemsets_by_length)
