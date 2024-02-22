import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# Your data
x = [1, 2, 3, 4, 5]  # Example x data
y = [10, 20, 30, 40, 50]  # Example y data

# Define the logarithmic function
def log_func(x, a, b, c):
    return a * np.log(x + b) + c


# Provide initial guesses for parameters
initial_guess = [1, 1, 1]

# Set bounds if necessary
bounds = ([-np.inf, -np.inf, -np.inf], [np.inf, np.inf, np.inf])

# Fit the logarithmic function to the data
popt, pcov = curve_fit(log_func, x, y, p0=initial_guess, bounds=bounds, maxfev=10000)

# Plot the original data
plt.scatter(x, y, label="Original data")

# Plot the fitted curve
x_values = np.linspace(min(x), max(x), 100)
plt.plot(x_values, log_func(x_values, *popt), "r-", label="Fitted curve")

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Logarithmic Regression")
plt.legend()
plt.show()

print("Coefficients:", popt)
