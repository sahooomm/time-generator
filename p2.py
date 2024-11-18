import numpy as np
from scipy.optimize import minimize_scalar

# Cost function: f(x, y) = x^2 - 2xy + 2y^2 + 2x
def cost_function(x, y):
    return x - y + 2*x**2 + 2*x*y + y**2

# Gradient of the cost function
def gradient(x, y):
    grad_x = 1 + 4*x + 2*y
    grad_y = -1 + 2*x + 2*y
    return grad_x, grad_y

# Cauchy (steepest descent) algorithm with tolerance
def cauchy_algorithm(x, y, iterations, tolerance=1e-6):
    for i in range(iterations):
        grad_x, grad_y = gradient(x, y)

        # Objective to find optimal step size (alpha)
        def objective(alpha):
            new_x = x - alpha * grad_x
            new_y = y - alpha * grad_y
            return cost_function(new_x, new_y)

        # Find the best alpha
        alpha = minimize_scalar(objective).x

        # Update x and y
        new_x = x - alpha * grad_x
        new_y = y - alpha * grad_y

        # Check for convergence (based on tolerance)
        if np.sqrt((new_x - x)*2 + (new_y - y)*2) < tolerance:
            print(f"Convergence reached at iteration {i+1}")
            break

        x, y = new_x, new_y

        print(f"Iteration {i+1}: x = {x:.4f}, y = {y:.4f}, cost = {cost_function(x, y):.4f}")

    return x, y

# Initial values and parameters
x_init, y_init = 1.0, 1.0
iterations = 50
tolerance = 1e-6

# Run the Cauchy algorithm
optimal_x, optimal_y = cauchy_algorithm(x_init, y_init, iterations, tolerance)

print(f"\nOptimal solution: x = {optimal_x}, y = {optimal_y}")