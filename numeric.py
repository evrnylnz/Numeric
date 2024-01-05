import sympy as sp
from sympy import symbols
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

x = sp.symbols('x')
fx = None  # Initialize fx to be set by the user
x_0 = None  # Initialize x_0 to be set by the user
max_iter = None  # Initialize max_iter to be set by the user
tol = None  # Initialize tol to be set by the user

x_points = np.linspace(0, 30, 1000)

def gfunc(fx):
    x = symbols('x')
    gx = fx + x
    return gx

def xfunc(x):
    return x

def x_axis(x):
    return x - x

def run_optimization(fx, x_0, max_iter, tol):
    result = []
    for i in range(1, max_iter + 1):
        x_val = float(gfunc(fx).subs(x, x_0))
        d = abs(x_val - x_0)
        result.append((i, x_val, d))
        if d < tol:
            break
        x_0 = x_val
    return result

@app.route('/', methods=['GET', 'POST'])
def index():
    global fx, x_0, max_iter, tol
    if request.method == 'POST':
        fx = sp.sympify(request.form['fx'])
        x_0 = float(request.form['x_0'])
        max_iter = int(request.form['max_iter'])
        tol = float(request.form['tol'])
        result = run_optimization(fx, x_0, max_iter, tol)
        return render_template('index.html', result=result)
    return render_template('index.html', result=None)

@app.route('/plot')
def plot():
    global fx
    if fx is not None:
        values = [gfunc(fx).subs(x, i) for i in x_points]
        plt.plot(x_points, xfunc(x_points), x_points, values, x_points, x_axis(x_points))
        plt.savefig('static/plot.png')
        plt.close()
        return render_template('plot.html')
    return "Please set the function first."

if __name__ == '__main__':
    app.run(debug=True)
