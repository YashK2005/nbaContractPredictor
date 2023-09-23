import copy
import numpy as np
from data_visualizer import gradient_descent_input_fetcher, gradient_descent_output_fetcher, new_gradient_descent_input_fetcher
import math
 
x = gradient_descent_input_fetcher()
#x = new_gradient_descent_input_fetcher()
y = gradient_descent_output_fetcher()
#y = np.sqrt(gradient_descent_output_fetcher())
b_init = 1000
w_init = np.array([100000]*len(x[0]))

def predict(x, w, b): 
    """
    single predict using linear regression
    Args:
      x (ndarray): Shape (n,) example with multiple features
      w (ndarray): Shape (n,) model parameters   
      b (scalar):             model parameter 
      
    Returns:
      p (scalar):  prediction
    """
    p = np.dot(x, w) + b     
    return p    

def compute_cost(X, y, w, b): 
    """
    compute cost
    Args:
      X (ndarray (m,n)): Data, m examples with n features
      y (ndarray (m,)) : target values
      w (ndarray (n,)) : model parameters  
      b (scalar)       : model parameter
      
    Returns:
      cost (scalar): cost
    """
    m = X.shape[0]
    cost = 0.0
    for i in range(m):                                
        f_wb_i = np.dot(X[i], w) + b           #(n,)(n,) = scalar (see np.dot)
        cost = cost + (f_wb_i - y[i])**2       #scalar
    cost = cost / (2 * m)                      #scalar    
    return cost

def compute_gradient(X, y, w, b): 
    """
    Computes the gradient for linear regression 
    Args:
      X (ndarray (m,n)): Data, m examples with n features
      y (ndarray (m,)) : target values
      w (ndarray (n,)) : model parameters  
      b (scalar)       : model parameter
      
    Returns:
      dj_dw (ndarray (n,)): The gradient of the cost w.r.t. the parameters w. 
      dj_db (scalar):       The gradient of the cost w.r.t. the parameter b. 
    """
    m,n = X.shape           #(number of examples, number of features)
    dj_dw = np.zeros((n,))
    dj_db = 0.

    for i in range(m):                             
        err = (np.dot(X[i], w) + b) - y[i]   
        for j in range(n):                         
            dj_dw[j] = dj_dw[j] + err * X[i, j]    
        dj_db = dj_db + err                        
    dj_dw = dj_dw / m                                
    dj_db = dj_db / m                                
        
    return dj_db, dj_dw

def gradient_descent(X, y, w_in, b_in, cost_function, gradient_function, alpha, num_iters): 
    """
    Performs batch gradient descent to learn theta. Updates theta by taking 
    num_iters gradient steps with learning rate alpha
    
    Args:
      X (ndarray (m,n))   : Data, m examples with n features
      y (ndarray (m,))    : target values
      w_in (ndarray (n,)) : initial model parameters  
      b_in (scalar)       : initial model parameter
      cost_function       : function to compute cost
      gradient_function   : function to compute the gradient
      alpha (float)       : Learning rate
      num_iters (int)     : number of iterations to run gradient descent
      
    Returns:
      w (ndarray (n,)) : Updated values of parameters 
      b (scalar)       : Updated value of parameter 
      """
    
    # An array to store cost J and w's at each iteration primarily for graphing later
    J_history = []
    w = copy.deepcopy(w_in)  #avoid modifying global w within function
    b = b_in
    
    for i in range(num_iters):

        # Calculate the gradient and update the parameters
        dj_db,dj_dw = gradient_function(X, y, w, b)   ##None

        # Update Parameters using w, b, alpha and gradient
        w = w - alpha * dj_dw               ##None
        b = b - alpha * dj_db               ##None
      
        # Save cost J at each iteration
        if i<100000:      # prevent resource exhaustion 
            J_history.append( cost_function(X, y, w, b))

        # Print cost every at intervals 10 times or as many iterations if < 10
        if i% math.ceil(num_iters / 10) == 0:
            print(f"Iteration {i:4d}: Cost {J_history[-1]:8.2f}   ")
        
    return w, b, J_history #return final w,b and J history for graphing

def zscore_normalize_features(X):
    """
    computes  X, zcore normalized by column
    
    Args:
      X (ndarray (m,n))     : input data, m examples, n features
      
    Returns:
      X_norm (ndarray (m,n)): input normalized by column
      mu (ndarray (n,))     : mean of each feature
      sigma (ndarray (n,))  : standard deviation of each feature
    """
    # find the mean of each column/feature
    mu     = np.mean(X, axis=0)                 # mu will have shape (n,)
    # find the standard deviation of each column/feature
    sigma  = np.std(X, axis=0)                  # sigma will have shape (n,)
    # element-wise, subtract mu for that column from each example, divide by std for that column
    X_norm = (X - mu) / sigma      

    return (X_norm, mu, sigma)
 
#alpha = 0.11

alpha = 0.11
iterations = 50000
x_norm, x_mu, x_sigma = zscore_normalize_features(x)
beal = x_norm[0]
curry = x_norm[10]
giannis = x_norm[13]
w_final, b_final, J_hist = gradient_descent(x_norm, y, w_init, b_init, compute_cost, compute_gradient, alpha, iterations)

bradley_beal = np.dot(beal, w_final) + b_final #brad beal
steph_curry = np.dot(curry, w_final) + b_final
giannis_ant = np.dot(giannis, w_final) + b_final

print(bradley_beal, steph_curry, giannis_ant)


print(w_final)
print(b_final)


''' using regulary salary, with normalized inputs
[ 2933000.96906488  3264778.45856615  3098118.61707276 -5192769.48781442
 -3251325.55720699  6488795.99919314  4705624.14117378 -6210304.91660523
   682729.02243221 -4055139.34174136  1413322.80528916 -3196762.41911576
   181342.38078732    71197.95634416 -4125886.3393388  -6129531.8312161
 15624428.58261674 -9390496.3809164   2026029.05173935 -3189002.95968927
  2967352.3099323    618654.25955234  5585852.36041301  5063076.91100247
  1925245.77552662  3673273.40392662 -2937151.88491306   833254.00331187]
12767957.222222222
'''

''' using root(salary), with normalized features
[  390.72064611   238.12755141  3624.65646033  -948.39765071
   175.78904129   813.75745805  1948.67085185  -906.40245749
 -3983.3510269   -311.86211767   476.71580505  -476.23618038
  -359.31860575   107.32005396  -339.86031271  -101.10936683
  4580.58745366  -642.84688027   779.17347563  -441.293291
   849.75528133   309.17192921 -4236.10936175   350.70672411
  -162.15478743   483.0859285     23.00219498   154.94896443]
3195.6652170231278
'''
