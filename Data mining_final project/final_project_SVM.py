import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn import svm, metrics

image = np.load("/Users/wengshiquan/Desktop/cs634/test/test_image.npy") #18724
label = np.load("/Users/wengshiquan/Desktop/cs634/test/test_label.npy")

train_image, test_image = image[:16000], image[16000:]
train_label, test_label = label[:16000], label[16000:]

train_image_1d = np.reshape(train_image, (16000, 28*28))
test_image_1d = np.reshape(test_image, (2724, 28*28))

# print(train_image_1d.shape, test_image_1d.shape) #(529114, 784) (18724, 784)
print("Start")
classifier = svm.SVC(gamma="auto", C=100)
classifier.fit(train_image_1d, train_label)
predicted = classifier.predict(test_image_1d)
print(predicted.shape)
print("Confusion Matrix\n", confusion_matrix(test_label, predicted))
print("Report\n", classification_report(test_label, predicted))
print("Score : ", metrics.accuracy_score(test_label, predicted))
print("Finished")
