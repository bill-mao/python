

#%%
#necessary import
import tensorflow as tf 
import numpy as np 
import matplotlib.pyplot as plt 

#%%
#linear regression

# training data : y = 0.5 * x + 0.1 + sigma(0, 0.01)
W_ref = 0.5
b_ref = 0.1
nData = 100
noise_mu = 0
noise_std = 0.1

X_train = np.linspace(-5, 9, nData)
Y_test = W_ref* X_train + b_ref
Y_train = Y_test + np.random.normal(noise_mu, noise_std, nData)

#%%
# plot the data using matplotlib
plt.figure(1)
plt.plot(X_train, Y_test, 'r', label = 'True data', )
plt.plot(X_train, Y_train, 'b', label= 'training data')
plt.axis('equal')
plt.legend(loc='lower right')
plt.show()

#%%
# write a tensorflow graph

X = tf.placeholder(tf.float32, name= 'input')
Y = tf.placeholder(tf.float32, name='output')
W = tf.Variable(np.random.randn(), name = 'weight')
b = tf.Variable(np.random.randn(), name= 'bias')

Y_pred = tf.add(tf.multiply(X,W), b)
loss = tf.reduce_mean(tf.square(Y-Y_pred))

learning_rate = 0.005
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)
training_epoch = 50
display_epoch = 5

#%%
# run the session

with tf.Session() as sess:
    sess.run(tf.initialize_all_variables())

    for epoch in range(training_epoch):
        W_temp = sess.run(W)
        b_temp = sess.run(b)
        loss_temp = sess.run(loss, feed_dict = {X:X_train, Y:Y_train})
        # pritn('epoch ')

    # final results
    
# Final results        
W_result = sess.run(W)
b_result = sess.run(b)            
print ("[Final: W, b] {:05.4f}, {:05.4f}".format(W_result, b_result))
print ("[Final: W, b] {:05.4f}, {:05.4f}".format(W_ref, b_ref))









