# import smarthouse
from main import *
import time_slice
import numpy as np
import itertools
import sklearn.metrics
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support as score

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

    for method in [1,2]:
        for j in [1,2]:
            if method == 1:
                if(j==1):
                    precisionmatrix = np.zeros(9)
                    recallmatrix = np.zeros(9)
                    fscorematrix = np.zeros(9)
                else:
                    precisionmatrix = np.zeros(10)
                    recallmatrix = np.zeros(10)
                    fscorematrix = np.zeros(10)
            else:
                if(j==1):
                    precisionmatrix = np.zeros(10)
                    recallmatrix = np.zeros(10)
                    fscorematrix = np.zeros(10)
                else:
                    precisionmatrix = np.zeros(11)
                    recallmatrix = np.zeros(11)
                    fscorematrix = np.zeros(11)
            for i in [1,2,3,4,5]:
                truth_a, predict_a, accuracy_a = predict(j,i,method) # dataset, days, method
                # cambia il tipo dell'array
                if method == 1:
                    if (j == 1):
                        truth_a = np.append([0, 1, 2, 3, 4, 5, 6, 7, 8], truth_a)

                        predict_a = predict_a.astype('uint8')
                        predict_a = np.append([0, 1, 2, 3, 4, 5, 6, 7, 8], predict_a)
                    else:
                        truth_a = np.append([0, 1, 2, 3, 4, 5, 6, 7, 8,9], truth_a)

                        predict_a = predict_a.astype('uint8')
                        predict_a = np.append([0, 1, 2, 3, 4, 5, 6, 7, 8,9], predict_a)
                else:
                    if (j == 1):
                        truth_a = np.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], truth_a)

                        predict_a = predict_a.astype('uint8')
                        predict_a = np.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], predict_a)
                    else:
                        truth_a = np.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10], truth_a)

                        predict_a = predict_a.astype('uint8')
                        predict_a = np.append([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10], predict_a)

                precision, recall, fscore, support = score(predict_a, truth_a)
                precisionmatrix = numpy.vstack([precisionmatrix, precision])
                recallmatrix = numpy.vstack([recallmatrix, recall])
                fscorematrix = numpy.vstack([fscorematrix, fscore])
                conf_mat_a = sklearn.metrics.confusion_matrix(truth_a, predict_a)
                print(sklearn.metrics.classification_report(truth_a, predict_a))
                plt.figure(num=None, figsize=(8, 6), dpi=80)
                plot_confusion_matrix(
                    conf_mat_a,
                    list(map(str, range(max(truth_a)))),
                    normalize=True
                )
                plt.savefig('confusionMatrix'+str(method)+str(j)+str(i)+'.png')
                plt.show()

            precisionmatrix = numpy.delete(precisionmatrix, (0), axis=0)
            fscorematrix = numpy.delete(fscorematrix, (0), axis=0)
            recallmatrix = numpy.delete(recallmatrix, (0), axis=0)

            meanprec = precisionmatrix.mean(0)
            meanfscore = fscorematrix.mean(0)
            meanrecall = recallmatrix.mean(0)



