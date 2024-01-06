import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from flask import Flask, render_template, request
from io import BytesIO
import base64

app = Flask(__name__)

x = sp.symbols('x')
fx = None  # Initialize fx to be set by the user
x_0 = None  # Initialize x_0 to be set by the user
max_iter = None  # Initialize max_iter to be set by the user
tol = None  # Initialize tol to be set by the user

x_points = np.linspace(0, 30, 1000)

def gfunc(fx):
    x = sp.symbols('x')
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

def update(frame, ax):
    if frame < len(x_points):
        values = [gfunc(fx).subs(x, i) for i in x_points[:frame]]

        # Clear existing lines from the axes
        for line in ax.lines:
            line.remove()

        # Plot the updated data
        ax.plot(x_points[:frame], xfunc(x_points[:frame]), label='x')
        ax.plot(x_points[:frame], values, label='g(x)')
        ax.plot(x_points[:frame], x_axis(x_points[:frame]), label='x-axis')
        ax.legend()
        ax.set_title(f'Iteration: {frame}')

        # Save the updated plot as an image
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        return plot_data
    else:
        return None

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
        fig, ax = plt.subplots()
        ani = FuncAnimation(fig, update, frames=max_iter, fargs=(ax,), interval=500, blit=False)
        ani.save('static/plot.gif', writer='imagemagick')
        plt.close()
        return render_template('plot.html', plot_exists=True)
    return render_template('plot.html', plot_exists=False)

if __name__ == '__main__':
    app.run(debug=True)
