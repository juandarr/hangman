from utils import Matrix
from random import random
from math import exp, log
import copy
'''
Neural network implementation using sigmoid as activation function.
Features:
    - Feed forward
    - Training with back propagation
'''

class NeuralNetworks:

    def __init__(self,input, output):
        self.size = [input,output]
        self.hidden_size = []
        self.init_weights()
        self.activations = []

    '''
    Implementation of sigmoid activation function for a input vector prod
    '''
    @staticmethod    
    def sigmoid(prod):
        for i in range(len(prod.matrix[0])):
            prod.matrix[0][i] = 1/(1+exp(-prod.matrix[0][i]))
        return prod

    '''
    Add hidden layer of dimension 'dimension'
    '''
    def add(self, dimension):
        self.hidden_size.append(dimension)
        self.init_weights()

    '''
    Weight initialization given the input, output and hidden layers size
    '''
    def init_weights(self):
        self.theta = []
        layers_range = [self.size[0]]+ self.hidden_size + [self.size[-1]]
        for i in range(len(layers_range)-1):
            self.theta.append(Matrix([[random() for m in range(layers_range[i] + 1)] for n in range(layers_range[i+1])]))

    def getSize(self):
        return [self.size[0]]+ self.hidden_size + [self.size[-1]]

    '''
    Feed forward algorithm.
    Representation of data is one column (vector) per sample
    '''
    def feed_forward(self,x):
        output_data = Matrix(x).transpose()
        self.activations =[]
        for i in range(len(self.theta)):
            self.activations.append(output_data)
            input_data = Matrix(output_data.matrix.copy()).transpose()
            for j in range(len(input_data.matrix)):
                input_data.matrix[j] = [1] + input_data.matrix[j]
            output_data = self.sigmoid(self.theta[i] * input_data.transpose())
        self.activations.append(output_data)
        return output_data
    '''
    Cost function: cross entropy
    Includes a regularization term to avoid overfitting
    '''
    def cost_function(self, x, y, lambda_r=0, g = []):
        cost = 0
        if g != []:
            self.theta[g[0]].matrix[g[1]][g[2]] += g[3]
        for m in range(len(x)):
            self.feed_forward([x[m]])
            for k in range(self.size[-1]):
                cost += y[m][k]*(log(self.activations[-1].matrix[k][0])) + (1-y[m][k])*(log(1-self.activations[-1].matrix[k][0]))
        cost /= (-1/len(x))
        if g != []:
            self.theta[g[0]].matrix[g[1]][g[2]] -= g[3]

        regularization_term  = 0
        if lambda_r !=0:
            for l in range(len(self.theta)):
                for j in range(1,len(self.theta[l].matrix)):
                    for i in range(1,len(self.theta[l].matrix[0])):
                        regularization_term += (self.theta[l].matrix[j][i])**2
            regularization_term /= (lambda_r/(2*len(x)))
        print(cost)
        return (cost+regularization_term)

    '''
    Backpropagation algorithm with regulatization term to avoid overfitting. 
    Given an input x, output y and lambda_r regularization factor calculates de derivatives of the cost function for one iteration
    '''
    def back_propagation(self, x , y , lambda_r=0):
        Delta = [[[0 for i in range(len(self.activations[l].matrix))] for j in range(len(self.activations[l+1].matrix))] for l in range(len(self.activations)-1)]
        for m in range(len(x)):
            deltas = []
            self.feed_forward([x[m]])
            deltas.append((self.activations[-1]-Matrix([y[m]]))) 

            for l in range(len(self.theta)-1, 0, -1):
                deltas.insert(0,Matrix((self.theta[l].transpose()*deltas[0]).matrix[1:][:]).pw_prod(self.activations[l]).pw_prod(Matrix([1]*len(self.activations[l].matrix))-self.activations[l]))
         
            for l in range(len(self.activations)-1):
                for j in range(len(self.activations[l+1].matrix)):
                    for i in range(len(self.activations[l].matrix)):
                        Delta[l][j][i] += (self.activations[l].matrix[i][0]*deltas[l].matrix[j][0])
        
        D = [[[0 for i in range(len(self.activations[l].matrix))] for j in range(len(self.activations[l+1].matrix))] for l in range(len(self.activations)-1)]
        for l in range(len(self.activations)-1):
            for j in range(len(self.activations[l+1].matrix)):
                for i in range(len(self.activations[l].matrix)):
                    if j==0:
                        D[l][j][i] = (1/len(x))*Delta[l][j][i]
                    else:
                        D[l][j][i] = (1/len(x))*Delta[l][j][i] +lambda_r * self.theta[l].matrix[j][i]
        return D
    '''
    Compute the gradient matrices for each weight matrix from layer i to layer j
    '''
    def gradient_compute(self, x, y, delta):
        gradient_theta = copy.deepcopy(self.theta)
        for l in range(len(gradient_theta)):
            for j in range(len(gradient_theta[l].matrix)):
                for i in range(len(gradient_theta[l].matrix[j])):
                    gradient_theta[l].matrix[j][i] = (self.cost_function(x,y,0, [l,j,i,delta]) - self.cost_function(x,y,0,[l,j,i,-delta]))/(2*delta)
        return gradient_theta


if __name__=='__main__':
    nn = NeuralNetworks(2,1)
    #print('\nNAND gate')
    #nn.theta.matrix[0] = [20,-15,-15]
    #print('\nNOR gate')
    #nn.theta.matrix[0] = [10,-15,-15]
    #print('\nOR gate')
    #nn.theta.matrix[0] = [-15,20,20]
    print('\nAND gate')
    #nn.theta[0].matrix[0] = [-15,10,10]
    x = [[0,0],[0,1],[1,0],[1,1]]
    y = [[0],[0],[0],[1]]
    nn.add(5)
    print('Network size: {}'.format(nn.getSize()))
    print([(i[0],i[1]) for i in x])
    y_p = nn.feed_forward(x)
    print('Expected output: ', y)
    print('Predicted output: ',y_p)
    D_numeric = nn.gradient_compute(x,y, 0.001)
    D = nn.back_propagation(x, y , 0.0)
    for l in range(len(D)):
        for j in range(len(D[l])):
            for i in range(len(D[l][j])):
                if l==1:
                    D[l][j][i] *= 16.0
    print('D Matrices: ', D)
    print('D numeric matrices: ', D_numeric)
  
    
    #print(nn.cost_function(x,y,0.02))
    #for i in range(len(nn.activations)):
    #    print(i, nn.activations[i])
