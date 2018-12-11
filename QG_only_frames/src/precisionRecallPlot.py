import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import numpy as np


def precision_recall_plot_one_variable(array, step, i, plot_name):
    array.sort(key=lambda array: array[i])
    min = array[0][i]
    max = array[len(array) - 1][i]
    thresholds = []
    precisions = []
    recalls = []
    threshold = 0
    while threshold <= 100:
        threshold_i = min + (max - min) * (threshold/100)
        true_positive = 0.0
        false_positive = 0.0
        true_negative = 0.0
        false_negative = 0.0
        for question in array:
            if question[i] < threshold_i and question[0] == 'bad':
                true_negative += 1
            if question[i] < threshold_i and question[0] == 'good':
                false_negative += 1
            if question[i] > threshold_i and question[0] == 'bad':
                false_positive += 1
            if question[i] > threshold_i and question[0] == 'good':
                true_positive += 1
        if (true_positive + false_positive) == 0:
            break
        thresholds.append(threshold)
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        precisions.append(precision)
        recalls.append(recall)
        threshold += step

    list_x_new = np.linspace(0, threshold, 1000)
    list_y_smooth = spline(thresholds, precisions, list_x_new)
    list_z_smooth = spline(thresholds, recalls, list_x_new)
    plt.plot(list_x_new, list_y_smooth, '-', label='Precision')
    plt.plot(list_x_new, list_z_smooth, '--', label='Recall')
    plt.axis([0, 100, 0, 1.1])
    plt.legend()
    plt.xlabel('Threshold')
    plt.title(plot_name)


def precision_recall_plot_two_variables(array, step, i, j, plot_name):
    array.sort(key=lambda array: array[i])
    mini = array[0][i]
    maxi = array[len(array) - 1][i]
    array.sort(key=lambda array: array[j])
    minj = array[0][j]
    maxj = array[len(array) - 1][j]
    thresholds = []
    precisions = []
    recalls = []
    threshold = 0.0
    while threshold <= 100:
        threshold_i = mini + (maxi - mini) * (threshold/100)
        threshold_j = minj + (maxj - minj) * (threshold/100)
        true_positive = 0.0
        false_positive = 0.0
        true_negative = 0.0
        false_negative = 0.0
        for question in array:
            if (question[i] < threshold_i or question[j] < threshold_j) and question[0] == 'bad':
                true_negative += 1
            if (question[i] < threshold_i or question[j] < threshold_j) and question[0] == 'good':
                false_negative += 1
            if question[i] > threshold_i and question[j] > threshold_j and question[0] == 'bad':
                false_positive += 1
            if question[i] > threshold_i and question[j] > threshold_j and question[0] == 'good':
                true_positive += 1
        if (true_positive + false_positive) == 0:
            break
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        precisions.append(precision)
        recalls.append(recall)
        thresholds.append(threshold)
        threshold += step

    list_x_new = np.linspace(0, threshold, 1000)
    list_y_smooth = spline(thresholds, precisions, list_x_new)
    list_z_smooth = spline(thresholds, recalls, list_x_new)
    plt.plot(list_x_new, list_y_smooth, '-', label='Precision')
    plt.plot(list_x_new, list_z_smooth, '--', label='Recall')
    plt.axis([0, 100, 0, 1.1])
    plt.legend()
    plt.xlabel('Threshold')
    plt.title(plot_name)


def precision_recall_plot_three_variables(array, step, i, j, z, plot_name):
    array.sort(key=lambda array: array[i])
    mini = array[0][i]
    maxi = array[len(array) - 1][i]
    array.sort(key=lambda array: array[j])
    minj = array[0][j]
    maxj = array[len(array) - 1][j]
    array.sort(key=lambda array: array[z])
    minz = array[0][z]
    maxz = array[len(array) - 1][z]
    thresholds = []
    precisions = []
    recalls = []
    threshold = 0.0
    while threshold <= 100:
        threshold_i = mini + (maxi - mini) * (threshold/100)
        threshold_j = minj + (maxj - minj) * (threshold/100)
        threshold_z = minz + (maxz - minz) * (threshold/100)
        true_positive = 0.0
        false_positive = 0.0
        true_negative = 0.0
        false_negative = 0.0
        for question in array:
            if (question[i] < threshold_i or question[j] < threshold_j or question[z] < threshold_z) and question[0] == 'bad':
                true_negative += 1
            if (question[i] < threshold_i or question[j] < threshold_j or question[z] < threshold_z) and question[0] == 'good':
                false_negative += 1
            if question[i] > threshold_i and question[j] > threshold_j and question[z] > threshold_z and question[0] == 'bad':
                false_positive += 1
            if question[i] > threshold_i and question[j] > threshold_j and question[z] > threshold_z and question[0] == 'good':
                true_positive += 1
        if (true_positive + false_positive) == 0 :
            break
        precision = true_positive / (true_positive + false_positive)
        recall = true_positive / (true_positive + false_negative)
        precisions.append(precision)
        recalls.append(recall)
        thresholds.append(threshold)
        threshold += step

    list_x_new = np.linspace(0, threshold, 1000)
    list_y_smooth = spline(thresholds, precisions, list_x_new)
    list_z_smooth = spline(thresholds, recalls, list_x_new)
    plt.plot(list_x_new, list_y_smooth, '-', label='Precision')
    plt.plot(list_x_new, list_z_smooth, '--', label='Recall')
    plt.axis([0, 100, 0, 1.1])
    plt.legend()
    plt.xlabel('Threshold')
    plt.title(plot_name)

