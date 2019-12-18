import numpy as np
import sys

model = np.load(sys.argv[1])
class_labels = model['class_labels']
wh = model['weight_h_1']
bh = model['bias_h_1']
wh2 = model['weight_h_2']
bh2 = model['bias_h_2']
wh3 = model['weight_h_3']
bh3 = model['bias_h_3']
wo = model['weight_h_o']
bo = model['bias_h_o']


def sigmoid(x):
	return 1 / (1 + np.exp(-x))


def sigmoid_der(x):
	return sigmoid(x) * (1 - sigmoid(x))


def softmax(A):
	expA = np.exp(A)
	return expA / expA.sum(axis=1, keepdims=True)


def test(fitur):
	zh = np.dot(fitur, wh) + bh
	ah = sigmoid(zh)

	zh2 = np.dot(ah, wh2) + bh2
	ah2 = sigmoid(zh2)

	zh3 = np.dot(ah2, wh3) + bh3
	ah3 = sigmoid(zh3)

	zo = np.dot(ah3, wo) + bo
	result = softmax(zo)
	print("classify \t\t : ", result)


input_data = [[0, 0, 0, 0, 0, 0, 0, 0]]
print("input \t\t : ", input_data)
print("class labels \t\t : ", class_labels)
test(input_data)

input_data = [[0, 0, 2, 0, 0, 0, 0, 0]]
print("input \t\t : ", input_data)
print("class labels \t\t : ", class_labels)
test(input_data)

input_data = [[0, 0, 0, 0, 0, -2, 0, 0]]
print("input \t\t : ", input_data)
print("class labels \t\t : ", class_labels)
test(input_data)


