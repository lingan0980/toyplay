# -*- coding: utf-8 -*-


"""
@version: 1.0
@author: clark
@file: tree.py
@time: 2017/7/2 15:56
@change_time:
1.2017/7/2 15:56
"""
import numpy as np


class Tree(object):

    def __init__(self, max_num_leaves):
        self.max_leaves = max_num_leaves

        self.num_leaves = 0

        # used fo non-leaf node
        self.left_child = [-1] * (self.max_leaves - 1)
        self.right_child = [-1] * (self.max_leaves - 1)
        self.split_feature_index = [-1] * (self.max_leaves - 1)
        self.threshold_in_bin = [-1] * (self.max_leaves - 1)      # threshold in bin
        self.threshold = [-1] * (self.max_leaves - 1)
        self.split_gain = [0] * (self.max_leaves - 1)

        self.internal_values = [0] * (self.max_leaves - 1)
        self.internal_counts = [0] * (self.max_leaves - 1)

        # used for leaf node
        self.leaf_parent = [-1] * self.max_leaves
        self.leaf_values = [0] * self.max_leaves
        self.leaf_counts = [0] * self.max_leaves

        self.leaf_depth = [0] * self.max_leaves            # depth for leaves

        # root is in the depth 0
        self.leaf_depth[0] = 0
        self.num_leaves = 1
        self.leaf_parent[0] = -1
        return

    def counts_of_leaf(self, leaf):
        return self.leaf_counts[leaf]

    def output_of_leaf(self, leaf):
        return self.leaf_values[leaf]

    def split(self, leaf, split_info):
        """
        :param best_leaf: the index of best leaf
        :param best_split_info: split info
        :return:
        """
        new_node_idx = self.num_leaves - 1

        parent = self.leaf_parent[leaf]
        if parent >= 0:
            if self.left_child[parent] == -leaf - 1:
                self.left_child[parent] = new_node_idx
            else:
                self.right_child[parent] = new_node_idx

        self.split_feature_index[new_node_idx] = split_info.feature_index
        self.threshold_in_bin[new_node_idx] = split_info.threshold_bin
        self.threshold[new_node_idx] = split_info.threshold
        self.split_gain[new_node_idx] = split_info.gain

        self.left_child[new_node_idx] = -leaf - 1
        self.right_child[new_node_idx] = -self.num_leaves - 1

        self.leaf_parent[leaf] = new_node_idx
        self.leaf_parent[self.num_leaves] = new_node_idx

        self.internal_values[new_node_idx] = self.leaf_values[leaf]
        self.internal_counts[new_node_idx] = self.leaf_counts[leaf]

        self.leaf_values[leaf] = split_info.left_output
        self.leaf_values[self.num_leaves] = split_info.right_output

        self.leaf_counts[leaf] = split_info.left_count
        self.leaf_counts[self.num_leaves] = split_info.right_count

        self.leaf_depth[self.num_leaves] = self.leaf_depth[leaf] + 1
        self.leaf_depth[leaf] += 1

        self.num_leaves += 1
        return self.num_leaves - 1

    def depth_of_leaf(self, leaf):
        return self.leaf_depth[leaf]

    def predict_prob(self, X):
        num_data, num_feature = X.shape

        predict_y = np.zeros((num_data,))

        for num_idx in xrange(num_data):
            predict_y[num_idx] = self.predict(X[num_idx, :])

        return predict_y

    def predict(self, feature_values):
        """
            根据当前的prediction对应到相应的子节点，根据子节点中数据的比例，得到相应的结果
            遍历树对应到相应的节点, 根据self.split_feature_index和self.threshold来划分到他的左右子节点，直到其中的节点是负数，即叶子节点为止
        :return:
        """
        score = 0.0
        current_node = 0

        while current_node >= 0:
            left_child_node = self.left_child[current_node]
            right_child_node = self.right_child[current_node]

            feature_index = self.split_feature_index[current_node]
            if feature_index < 0:
                break

            feature_value = feature_values[feature_index]
            threshold = self.threshold[current_node]

            if feature_value <= threshold:
                current_node = left_child_node
            else:
                current_node = right_child_node

            if current_node < 0:
                score = self.leaf_values[~current_node]
                break

        return score

    def show(self):
        print "start-------------------"
        print "left_child", self.left_child
        print "right_child", self.right_child
        print "leaf_parent", self.leaf_parent
        print "split_feature_index", self.split_feature_index
        print "threshold_in_bin", self.threshold_in_bin
        print "threshold", self.threshold
        print "split_gain", self.split_gain
        print "interval_values", self.internal_values
        print "internal_counts", self.internal_counts
        print "leaf_counts", self.leaf_counts
        print "leaf_values", self.leaf_values
        print "leaf_depth", self.leaf_depth
        print "end----------------------"
        return


if __name__ == '__main__':
    pass
