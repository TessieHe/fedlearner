import os
import argparse

import numpy as np
import tensorflow as tf


def process_data(X, y, role, verify_example_ids):
    X = X.reshape(X.shape[0], -1)
    X = np.asarray([X[i] for i, yi in enumerate(y) if yi in (2, 3)])
    y = np.asarray([[y[i] == 3] for i, yi in enumerate(y) if yi in (2, 3)],
                   dtype=np.int32)
    if role == 'leader':
        data = np.concatenate((X[:, :X.shape[1]//2], y), axis=1)
    elif role == 'follower':
        data = X[:, X.shape[1]//2:]
    else:
        data = np.concatenate((X, y), axis=1)

    if verify_example_ids:
        data = np.concatenate(
            [[[i] for i in range(data.shape[0])], data], axis=1)
    return data

def make_data(args):
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    if not os.path.exists('data'):
        os.makedirs('data')
    np.savetxt(
        'data/leader_train.csv',
        process_data(x_train, y_train, 'leader', args.verify_example_ids),
        delimiter=',')
    np.savetxt(
        'data/follower_train.csv',
        process_data(x_train, y_train, 'follower', args.verify_example_ids),
        delimiter=',')
    np.savetxt(
        'data/local_train.csv',
        process_data(x_train, y_train, 'local', False),
        delimiter=',')

    np.savetxt(
        'data/leader_test.csv',
        process_data(x_test, y_test, 'leader', args.verify_example_ids),
        delimiter=',')
    np.savetxt(
        'data/follower_test.csv',
        process_data(x_test, y_test, 'follower', args.verify_example_ids),
        delimiter=',')
    np.savetxt(
        'data/local_test.csv',
        process_data(x_test, y_test, 'local', False),
        delimiter=',')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='FedLearner Tree Model Trainer.')
    parser.add_argument('--verify-example-ids',
                        type=bool,
                        default=False,
                        help='If set to true, the first column of the '
                             'data will be treated as example ids that '
                             'must match between leader and follower')
    make_data(parser.parse_args())
