import numpy as np

def gradient_descent(f, df, x0, alpha, tol=1e-6, max_iter=1000):
    """
    Perform gradient descent optimization to minimize a function.

    Parameters:
    - f: The function to minimize.
    - df: The derivative (gradient) of the function.
    - x0: The starting point (initial guess).
    - alpha: The fixed step size (learning rate).
    - tol: Tolerance for the stopping criterion.
    - max_iter: Maximum number of iterations.

    Returns:
    - x: The optimal value for x.
    - history: A list of x values at each iteration (for visualization purposes).
    """

    x = x0
    history = [x0]  # Store the history of x values

    for i in range(max_iter):
        gradient = df(x)  # Compute the gradient at x
        new_x = x - alpha * gradient  # Update x using gradient descent rule
        history.append(new_x)

        # Check for convergence
        if np.abs(new_x - x) < tol:
            print(f"Converged in {i+1} iterations.")
            break

        x = new_x

    return x, history

# Example usage
if __name__ == "__main__":
    # Define a sample function and its derivative
    f = lambda x: (x - 2)**2  # Function: (x - 2)^2
    df = lambda x: 2 * (x - 2)  # Derivative: 2 * (x - 2)

    # Initial guess, step size, and tolerance
    x0 = 10
    alpha = 0.1

    # Run gradient descent
    optimal_x, history = gradient_descent(f, df, x0, alpha)

    print(f"The optimal value of x is: {optimal_x}")
