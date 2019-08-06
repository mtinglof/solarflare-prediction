import torch

class Neural_Network(torch.nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Neural_Network, self).__init__()
        self.inputSize = input_size
        self.outputSize = 2
        self.hiddenSize = hidden_size
        self.Tanh = torch.nn.Tanh()
        
    def forward(self, X):
        self.z = torch.matmul(X, self.W1) 
        self.z2 = self.Tanh(self.z) 
        self.z3 = torch.matmul(self.z2, self.W2)
        output = self.Tanh(self.z3) 
        return output
    
    def setWeights(self, W):
        self.W1 = W[0]
        self.W2 = W[1]