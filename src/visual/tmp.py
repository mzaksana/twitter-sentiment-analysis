# Muammar Zikri Aksana
# multi-3-hidden-layer
import numpy as np  
import matplotlib.pyplot as plt

# 42 penentuan seed random
np.random.seed(42)

# np.random.randn(700, 2) : 2 untuk 2 dimensi
cat_images = np.random.randn(700, 2) + np.array([0, -3])  
mouse_images = np.random.randn(700, 2) + np.array([3, 3])  
dog_images = np.random.randn(700, 2) + np.array([-3, 3])
# 
feature_set = np.vstack([cat_images, mouse_images, dog_images])

labels = np.array([0]*700 + [1]*700 + [2]*700)
# matrix zero
one_hot_labels = np.zeros((2100, 3))

for i in range(2100):  
    one_hot_labels[i, labels[i]] = 1

plt.figure(figsize=(10,7))  
plt.scatter(feature_set[:,0], feature_set[:,1], c=labels, cmap='plasma', s=100, alpha=0.5)  
# plt.show()

def sigmoid(x):  
    return 1/(1+np.exp(-x))

def sigmoid_der(x):  
    return sigmoid(x) *(1-sigmoid (x))

def softmax(A):  
    expA = np.exp(A)
    return expA / expA.sum(axis=1, keepdims=True)

instances = feature_set.shape[0]  
attributes = feature_set.shape[1]  
hidden_nodes = 4  
output_labels = 3


wh = np.random.rand(attributes,hidden_nodes)  
bh = np.random.randn(hidden_nodes)

wh2 = np.random.rand(hidden_nodes,hidden_nodes)  
bh2 = np.random.randn(hidden_nodes)

wh3 = np.random.rand(hidden_nodes,hidden_nodes)  
bh3 = np.random.randn(hidden_nodes)

wo = np.random.rand(hidden_nodes,output_labels)  
bo = np.random.randn(output_labels)  
lr = 10e-4

error_cost = []

for epoch in range(50000):  
############# feedforward

    # Phase 1
    zh = np.dot(feature_set, wh) + bh
    ah = sigmoid(zh)

    # Phase 2
    zh2 = np.dot(ah, wh2) + bh2
    ah2 = sigmoid(zh2)

    # Phase 3
    zh3 = np.dot(ah2, wh3) + bh3
    ah3 = sigmoid(zh3)

    # Phase 4
    zo = np.dot(ah3, wo) + bo
    ao = softmax(zo)
    # print(ao)

########## Back Propagation

########## Phase 1
    # d : derivativ 
    # titik balik function ; turunan function
    dcost_dzo = ao - one_hot_labels # a3 -delta
    dzo_dwo = ah3

    dcost_wo = np.dot(dzo_dwo.T, dcost_dzo)
    dcost_bo = dcost_dzo

########## Phases 2
    dzo_dah3 = wo
    dcost_dah3 = np.dot(dcost_dzo , dzo_dah3.T)
    dah_dzh3 = sigmoid_der(zh3)
    dzh_dwh3 = ah2
    dcost_wh3 = np.dot(dzh_dwh3.T, dah_dzh3 * dcost_dah3)
    
    dcost_bh3 = dcost_dah3 * dah_dzh3
    # z = dcost_dah2 * dah_dzh2

########## Phases 3

    dzo_dah2 = wh3
    dcost_dah2 = np.dot(dah_dzh3 *dcost_dah3, dzo_dah2.T)
    dah_dzh2 = sigmoid_der(zh2)
    dzh_dwh2 = ah
    dcost_wh2= np.dot(dzh_dwh2.T, dah_dzh2 * dcost_dah2)
    
    dcost_bh2 = dcost_dah2 * dah_dzh2
    # z = dcost_dah * dah_dzh

########## Phases 4

    dzo_dah = wh2
    dcost_dah = np.dot(dah_dzh2 *dcost_dah2, dzo_dah.T)
    dah_dzh = sigmoid_der(zh)
    dzh_dwh = feature_set
    dcost_wh= np.dot(dzh_dwh.T, dah_dzh * dcost_dah)
    
    dcost_bh = dcost_dah * dah_dzh

    # Update Weights ================

    wh3 -= lr * dcost_wh3
    bh3 -= lr * dcost_bh3.sum(axis=0)
    
    wh2 -= lr * dcost_wh2
    bh2 -= lr * dcost_bh2.sum(axis=0)

    wh -= lr * dcost_wh
    bh -= lr * dcost_bh.sum(axis=0)
    # print("wh "+ str(wh))
    # print("bh "+ str(bh))

    wo -= lr * dcost_wo
    bo -= lr * dcost_bo.sum(axis=0)
    # print("wh "+ str(wo))
    # print("bo "+ str(bo))

    if epoch % 250 == 0:
        loss = np.sum(-one_hot_labels * np.log(ao))
        print('Loss function value: ', loss)
        error_cost.append(loss)


# print('wh = '+str(wh))
# print('bh = '+str(bh))

# print('wh2 = '+str(wh2))
# print('bh2 = '+str(bh2))
# print('wo = '+str(wo))
# print('bo = '+str(bo))

input_data= np.random.randn(1,2)
print("input")
print(input_data)
input_data=[[2.86357106, 2.45766953]]
zh=np.dot(input_data,wh)+bh
ah=sigmoid(zh)

zh2=np.dot(ah,wh2)+bh2
ah2=sigmoid(zh2)

zh3=np.dot(ah2,wh3)+bh3
ah3=sigmoid(zh3)

zo=np.dot(ah3,wo)+bo
out=softmax(zo)

print("out")
print(out)

