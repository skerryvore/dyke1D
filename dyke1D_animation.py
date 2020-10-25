"""
Animation of thermal evolution of dyke intrusion in 1D

                             Roderick Brown 25/10/2020
"""

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation
from scipy import special

# Define some style parameters and cmap
def setup_style():
    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 20,}
    mycmap = matplotlib.cm.get_cmap('rainbow_r')
    return font, mycmap

# Set up the figure, the axis, and the plot element we want to animate
def setup_plot():
    fig = plt.figure(figsize=[7,5])
    ax = plt.axes(xlim=(0, 5), ylim=(0, 1400))
    ax.set_ylabel('Temperature [°C]',fontsize=18)
    ax.set_xlabel('Dimensionless Distance [D]',fontsize=18)
    line, = ax.plot([], [], lw=2)
    line0, = ax.plot([], [], lw=2)
    time_stamp = ax.text(2.,1200, '',fontdict=font)
    D_stamp = ax.text(2.,1000, '',fontdict=font)

    return fig,ax,line,line0,time_stamp,D_stamp

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    line0.set_data([], [])
    return line,line0

# animation function.  This is called sequentially
def dyketemps(i):

    T0 = 100.0        # ambient temperature
    Ti = 1400.0       # intrusion temperature
    D = 500.          # dyke half-width, full width is 2D
    cappa = 1.25E-6   # thermal diffusivity
    secmy = 3.16e13   # seconds/myr

# set the distances at which to calcuate the Ts
    distances = np.linspace(0, D*5, 100)
    x = distances/D # dimensionless distance

# set the time
    timemy=0.000005*i      # Set time step for animation in Myr
    time=timemy*secmy        # time in seconds
    t = (time*cappa)/(D*D)   # dimensionless time

    colour=mycmap(timemy/0.01) # adjust colour to value between 0 and 1

# Get the temperatures at each distance for timestep
    Tempt = T0 + ((Ti-T0)/2)*(special.erf( (1+x)/(2*np.sqrt(t)) ) \
        + special.erf( (1-x)/(2*np.sqrt(t))))

# Get temps at start, bit clunky, but easy :-)
    Temp0 = T0 + ((Ti-T0)/2)*(special.erf( (1+x)/(2*np.sqrt(0.000001)) ) \
        + special.erf( (1-x)/(2*np.sqrt(0.000001))))

# Plot initial temps at start
    line0.set_data(x,Temp0)
    line0.set_linestyle('-')
    line0.set_linewidth(3)
    line0.set_color('k')

# Plot temps at timestep
    line.set_data(x,Tempt)
    line.set_linestyle('-')
    line.set_linewidth(3)
    line.set_color(colour)

#    draw time stamp and width
    time_stamp.set_text(f'time={timemy*1000.:.2f} kyr')
    D_stamp.set_text(f'half-width,D={D:.0f} m')
    return line,line0,time_stamp,D_stamp

def draw_animation(fig,ax):
# Call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, dyketemps, init_func=init,
                    frames=4000, interval=10, repeat=False, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#    anim.save('dyke_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
# Setup style options
    font,mycmap = setup_style()
# Setup the plot
    fig,ax,line,line0,time_stamp,D_stamp = setup_plot()
# Draw the animation
    draw_animation(fig,ax)
