"""
  FIR Animation program - Low Pass Cutoff Frequency Sweep
  Written by Electro707
  
  This program takes a low pass filter, and animates the magnitude response of the filter
  with varing cutoff frequencies for the same tap number.
"""
import sympy
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set to true to export a video instead of showing the animation.
EXPORT_VIDEO = False

# The sampling rate
sr = 8E3
# The number of taps
taps = 19
# The number of animation frames
ANIMATION_NUM_FRAMES = 10 * 60


def get_mag_angle(eq):
  """
    Function that takes a number and returns the magnitude and phase 
  """
  return numpy.abs(eq), numpy.degrees(numpy.angle(eq))

def hz_e(b_coef, o):
  """
    Function to calculate the response of the filter for a given b coefficients
    and a normalized frequency (between 0 and pi)
  """
  sum = 0
  for key in b_coef:
      sum += b_coef[key]*numpy.exp(-o*1j*key)
  return sum

def get_freq_from_interval(interval: int):
  """
    Helper function to get the frequency from a animation interval.
  """
  return (interval/ANIMATION_NUM_FRAMES)*(sr/2)

def calculate_response(lp_freq: float, tap:int = taps):
  """
    Function to calculate the response of the filter with a given number of 
    taps and cutoff frequency
  """
  omega_c = 2*numpy.pi*lp_freq/sr
  m = (tap-1)//2
  h = {0: omega_c/numpy.pi}
  for i in range(1, m+1):
      h[i] = numpy.sin(omega_c*i)/(i*numpy.pi)
      h[-i] = h[i]

  b = {}
  for i in range(0, len(h)):
      b[i] = h[i-m]

  data = {}
  for i in numpy.linspace(0, float(numpy.pi), 300):
      data[i*sr/(2*numpy.pi)] = get_mag_angle(hz_e(b, i))[0]
  return data

def animate(frame_number):
  """
    Animation function MatPlotLib uses to do the plotting
  """
  print("Making frame %d out of %d" % (frame_number, ANIMATION_NUM_FRAMES))
  data = calculate_response(get_freq_from_interval(frame_number)).copy()
  
  x, y = zip(*sorted(data.items()))
  ln.set_data(x, y)
  plt.title("Low Pass Filter (%d taps) for %dHz" % (taps, get_freq_from_interval(frame_number)))
  
# Create the plot
fig, ax = plt.subplots()
ax.set_xlabel('$Frequency (Hz)$')
ax.set_ylabel('$Amplitude (V/V)$')
ax.set_xlim(0, 4000)
ax.set_ylim(0, 1.2)
ln, = ax.plot([])

# Animate the plot
anim = animation.FuncAnimation(fig, animate, frames=ANIMATION_NUM_FRAMES, interval=1)
if EXPORT_VIDEO:
    writermp4 = animation.FFMpegWriter(fps=60)
    anim.save('LowPassChangingFeq1.mp4', writer=writermp4, dpi=300)
    print("Exported video")
else:
    plt.show()
