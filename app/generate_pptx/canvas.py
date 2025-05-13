import matplotlib.pyplot as plt
import numpy as np


def crear_canvas(x_min=-10, x_max=10, y_min=-10, y_max=10, step=1):
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    ax.axhline(y=0, color='black', lw=1)
    ax.axvline(x=0, color='black', lw=1)

    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    ax.set_xticks(np.arange(x_min, x_max + step, step))
    ax.set_yticks(np.arange(y_min, y_max + step, step))

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_aspect('equal', adjustable='box')

    return fig, ax
