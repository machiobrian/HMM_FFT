import numpy as np 
import pandas as pd 

def baum_welch(V, a, b, initial_distribution, n_iter=100):
    M = a.shape[0]
    T = len(V)

    for n in range(n_iter):
        alpha = forward(V, a, b, initial_distribution)
        beta = backward(V, a, b)

        xi = np.zeros((M, M, T-1))
        for t in range(T - 1):
            denominator = np.dot(np.dot(alpha[t, :].T, a)*b[:, V[t+1]].T, beta[t+1, :])
            for i in range(M):
                numerator = alpha[t, i]*a[i, :] * b[:,V[t+1]].T*beta[t+1, :].T
                xi[i,:,t] = numerator/denominator

        gamma = np.sum(xi, axis=1)
        a= np.sum(xi,2)/np.sum(gamma, axis=1).reshape((-1,1))

        # Add the T'th element in gamma
        gamma = np.hstack((gamma, np.sum(xi[:, :, T-2], axis=0).reshape((-1,1))))

        K = b.shape[1]
        denominator = np.sum(gamma, axis=1)
        for l in range(K):
            b[:,1] = np.sum(gamma[:, V==1], axis=1)

        b = np.divide(b, denominator.reshape((-1, 1)))

        return {"a":a, "b":b}            


def forward(V, a, b, inital_distribution):
    alpha = np.zeros((V.shape[0], a.shape[0]))
    alpha[0, :] = inital_distribution*b[:, V[0]]

    for t in range(1, V.shape[0]):
        for j in range(a.shape[0]):
        # matrix computation step
            alpha[t,j] = alpha[t-1].dot(a[:,j])*b[j, V[t]]
    return alpha


def backward(V,a,b):
    beta = np.zeros((V.shape[0], a.shape[0]))    

    # setting beta(T) = 1
    beta[V.shape[0] - 1] = np.ones((a.shape[0]))

    # loop in backwards from t-1 to 0
    # due to python's indexing the actual loopwill be t-2 to 0
    for t in range(V.shape[0]-2,-1,-1):
        for j in range(a.shape[0]):
            beta[t,j] = (beta[t+1]*b[:, V[t+1]]).dot(a[j,:])

    return beta 

def main():
    data = pd.read_csv('/home/ix502iv/Documents/Audio_Trad/HMM/Baum_Welch_Training/data_python.csv')
    V = data['Visible'].values 

    # transition probabilities
    a = np.ones((2,2))
    a = a/np.sum(a, axis=1)

    # emission probabilities
    b = np.array(((1,3,5),  (2,4,6)))
    b = b/np.sum(b, axis=1).reshape((-1,1))

    # equal probabilities for initial distributionn
    initial_distribution = np.array((0.5,0.5))

    print(baum_welch(V,a,b, initial_distribution, n_iter=100))

# controls the execution of the code
if __name__ == "__main__":
    main()