def read_dataset(file_name):
    # the row on which the data starts is the transaction id
    # the rest of the row is the items in the transaction
    with open(file_name, 'r') as f:
        dataset = [set(line.strip().split()) for line in f.readlines()]

    return dataset


def split_dataset(data_set: list, test_size):
    assert 0 < test_size < 1
    n_test_els = int(len(data_set) * test_size)
    n_train_els = len(data_set) - n_test_els

    # get the training dataset
    train_data = data_set[:n_train_els]

    # remove the last element of each of the test dataset elements
    test_data = {i: list(test_el)[:-1] \
                 for i, test_el in enumerate(data_set[n_train_els:]) if len(test_el) > 1}
    # take only the last element of each of the test dataset elements to be the one to
    # predict
    user_items = {i: list(test_el)[-1] \
                  for i, test_el in enumerate(data_set[n_train_els:]) if len(test_el) > 1}

    return data_set[:n_train_els], test_data, user_items


if __name__ == '__main__':
    transactions = read_dataset('data/retail.dat')
    print(transactions)

    train, test_data, user_items = split_dataset(transactions, 0.2)
    print(train)
    print(test_data)
    print(user_items)
