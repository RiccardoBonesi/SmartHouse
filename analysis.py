# import smarthouse
from main import *
import time_slice
import numpy as np
import itertools
import sklearn.metrics
import matplotlib.pyplot as plt

def predict(dataset, days, method):

    # truth_a, predict_a, accuracy_a
    return calculate(dataset, days, method)




def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True')
    plt.xlabel('Predicted label')


if __name__ == '__main__':
    np.set_printoptions(precision=2)

    # prova mia
    print("A - test 2 - no Time Slice")
    truth_a, predict_a, accuracy_a = predict(1,4,2) # dataset, days, method

    # cambia il tipo dell'array
    predict_a = predict_a.astype('uint8')


    print(sklearn.metrics.classification_report(truth_a, predict_a))
    conf_mat_a = sklearn.metrics.confusion_matrix(truth_a, predict_a)

    plt.figure(1)
    plot_confusion_matrix(
        conf_mat_a,
        list(map(str, range(max(truth_a)))),
        normalize=True
    )







    # # A - 3 giorni
    # print("=== A - 3 giorni ===")
    # truth_a, predict_a, accuracy_a = predict('A', days=3)   #truth_a e predict_a sono le frequenze
    # print(sklearn.metrics.classification_report(truth_a, predict_a))
    # conf_mat_a = sklearn.metrics.confusion_matrix(truth_a, predict_a)
    #
    # plt.figure(1)
    # plot_confusion_matrix(
    #     conf_mat_a,
    #     list(map(str, range(max(truth_a)))),
    #     normalize=True
    # )
    #
    # # B - 4 giorni
    # print("=== B - 4 giorni ===")
    # truth_b, predict_b, accuracy_b = predict('B', days=4)
    # print(sklearn.metrics.classification_report(truth_b, predict_b))
    # conf_mat_b = sklearn.metrics.confusion_matrix(truth_b, predict_b)
    #
    # plt.figure(2)
    # plot_confusion_matrix(
    #     conf_mat_b,
    #     list(map(str, range(max(truth_b)))),
    #     normalize=True
    # )
    #
    # # A - 3000 samples
    # print("=== A - 3000 samples ===")
    # truth_a, predict_a, accuracy_a = predict('A', n_samples=3000)
    # print(sklearn.metrics.classification_report(truth_a, predict_a))
    # conf_mat_a = sklearn.metrics.confusion_matrix(truth_a, predict_a)
    #
    # plt.figure(3)
    # plot_confusion_matrix(
    #     conf_mat_a,
    #     list(map(str, range(max(truth_a)))),
    #     normalize=True
    # )
    #
    # # A - 20000 samples
    # print("=== A - 20000 samples ===")
    # truth_a, predict_a, accuracy_a = predict('A', n_samples=20000)
    # print(sklearn.metrics.classification_report(truth_a, predict_a))
    # conf_mat_a = sklearn.metrics.confusion_matrix(truth_a, predict_a)
    #
    # plt.figure(4)
    # plot_confusion_matrix(
    #     conf_mat_a,
    #     list(map(str, range(max(truth_a)))),
    #     normalize=True
    # )
    #
    # # B - 3000 samples
    # print("=== B - 3000 samples ===")
    # truth_b, predict_b, accuracy_b = predict('B', n_samples=3000)
    # print(sklearn.metrics.classification_report(truth_b, predict_b))
    # conf_mat_b = sklearn.metrics.confusion_matrix(truth_b, predict_b)
    #
    # plt.figure(5)
    # plot_confusion_matrix(
    #     conf_mat_b,
    #     list(map(str, range(max(truth_b)))),
    #     normalize=True
    # )
    #
    #
    # # B - 20000 samples
    # print("=== B - 20000 samples ===")
    # truth_b, predict_b, accuracy_b = predict('B', n_samples=20000)
    # print(sklearn.metrics.classification_report(truth_b, predict_b))
    # conf_mat_b = sklearn.metrics.confusion_matrix(truth_b, predict_b)
    #
    # plt.figure(6)
    # plot_confusion_matrix(
    #     conf_mat_b,
    #     list(map(str, range(max(truth_b)))),
    #     normalize=True
    # )


    plt.show()
