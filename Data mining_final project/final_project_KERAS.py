import numpy as np
from keras import models, layers
from keras.layers import Dense
from keras.utils import to_categorical
import matplotlib.pyplot as plt
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.utils import to_categorical
from keras import losses, backend, optimizers, metrics
import os
import h5py
import matplotlib.pyplot as plt
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.metrics import roc_curve, auc, roc_auc_score, precision_recall_curve, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from keras.callbacks import EarlyStopping, ModelCheckpoint

train = np.load("/Users/wengshiquan/Desktop/cs634/train/train_image.npy")
label = np.load("/Users/wengshiquan/Desktop/cs634/train/train_label.npy")
test = np.load("/Users/wengshiquan/Desktop/cs634/test/test_image.npy")
test_label = np.load("/Users/wengshiquan/Desktop/cs634/test/test_label.npy")

print('train ', train.shape)
print("label ", label.shape)
print("test ", test.shape)
print("test_label", test_label.shape)

train_image = train[:423291]
train_label = label[:423291]
val_image = train[423291:]
val_label = label[423291:]

print('train ', train_image.shape)
print("train_label ", train_label.shape)
print("val ", val_image.shape)
print("val_label", val_label.shape)

train_image_1d = np.reshape(train_image, (423291, 28*28))
val_image_1d = np.reshape(val_image, (105823, 28*28))
test_image_1d = np.reshape(test, (18724, 28*28))

print('train_1d ', train_image_1d.shape)
print("val_1d ", val_image_1d.shape)

train_label, val_label, test_label = to_categorical(train_label), to_categorical(val_label), to_categorical(test_label)

def build_model(): #building model
	network = models.Sequential()
	network.add(Dense(500, activation = 'relu', input_shape=(28 * 28,)))
	network.add(Dense(200, activation='relu'))
	network.add(Dropout(0.5))
	network.add(Dense(200, activation='relu'))
	network.add(Dropout(0.5))
	network.add(Dense(200, activation='relu'))
	network.add(Dropout(0.4))
	network.add(Dense(200, activation='relu'))
	network.add(Dropout(0.4))
	network.add(Dense(10, activation='sigmoid'))
	network.compile(loss = "categorical_crossentropy", optimizer = optimizers.adam(lr= 0.001), metrics = ['accuracy'])
	return network

def build_loaded_model(): #build model again and append parameters into it
	model = Sequential()
	model.add(Dense(500, activation='relu', input_shape=(28*28,)))
	model.add(Dense(200, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(200, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(200, activation='relu'))
	model.add(Dropout(0.4))
	model.add(Dense(200, activation='relu'))
	model.add(Dropout(0.4))
	model.add(Dense(10, activation='sigmoid'))
	model.compile(loss = "categorical_crossentropy", optimizer = optimizers.adam(lr= 0.001), metrics = ['accuracy'])
	model.load_weights('best_model/best_model.hdf5',by_name=True)
	return model

def run_model(loaded_model, test_image_1d, test_label): #run model for testing data
	accuracy = loaded_model.evaluate(test_image_1d, test_label)
	pred = loaded_model.predict(test_image_1d)
	#input to confusion_matrix must be an array of int not one hot encodings
	matrix = confusion_matrix(test_label.argmax(axis=1), pred.argmax(axis=1))
	print("Confusion Matrix")
	print(matrix)
	tp = np.diag(matrix)
	print("True Positive : ", tp)
	FalsePositive = []
	for i in range(10):
		FalsePositive.append(sum(matrix[:,i]) - matrix[i,i])
	print("False Positive : ", FalsePositive)
	FalseNegative = []
	for i in range(10):
		FalseNegative.append(sum(matrix[i,:]) - matrix[i,i])
	print("False Negative : ", FalseNegative)
	TrueNegative = []
	for i in range(10):
		temp = np.delete(matrix, i, 0)   # delete ith row
		temp = np.delete(temp, i, 1)  # delete ith column
		TrueNegative.append(sum(sum(temp)))
	print("True Negative : ", TrueNegative)
	print("ROC AUC Score : ", roc_auc_score(test_label, pred))
	print("Accuracy : ", accuracy[1])

keras_model = build_model()
filepath = 'best_model/best_model.hdf5'
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
earlyStopping=EarlyStopping(monitor='val_loss', patience=50, mode='min')
keras_model.fit(train_image_1d, train_label, validation_data =(val_image_1d, val_label) ,epochs=500,  batch_size=128, callbacks = [checkpoint, earlyStopping])

accuracy = keras_model.evaluate(test_image_1d, test_label)
pred = keras_model.predict(test_image_1d)

pred_data = h5py.File('best_model/pred.hdf5', 'w')
pred_data.create_dataset('pred', data = pred, compression_opts=9, compression = 'gzip')
	
loaded_model = build_loaded_model()
run_model(loaded_model, test_image_1d, test_label)
print("finished")




