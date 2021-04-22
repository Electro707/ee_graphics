"""
  FIR Animation program - Number of Taps
  Written by Electro707
  
  This program takes a low pass filter, and animates the magnitude response of the filter
  with diffrent taps, showing that the filter becomes more accurate the more taps are added.
"""
import sympy
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# The low pass filter's cutoff frequency
lp_f = 800
# The sampling rate
sr = 8E3
# The number of animation frames
ANIMATION_NUM_FRAMES = 20 * 60

# A pre-calculated value for the normalized cutoff frequency
omega_c = 2*numpy.pi*lp_f/sr

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

# Data for animation
next_frame_data = None
current_frame_data = None
current_frame_num = None

def calculate_response(tap):
  """
    Function to calculate the response of the filter with a given number of 
    taps
  """
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
  global next_frame_data, current_frame_data, current_frame_num
  current_interval = frame_number // 20
  if current_frame_num is None or current_frame_num != current_interval or frame_number == 0:
    current_frame_num = current_interval
    if next_frame_data is not None:
      current_frame_data = next_frame_data.copy()
    else:
      current_frame_data = calculate_response((current_interval*2)+3).copy()
    next_frame_data = calculate_response(((current_interval+1)*2)+3).copy()
    data = current_frame_data
  else:
    data = current_frame_data
    
    #for d_k in current_frame_data:
      #data[d_k] = current_frame_data[d_k] + (frame_number-(current_interval*20)) * (next_frame_data[d_k] - current_frame_data[d_k]) / (20)
  print("Frame %d out of %d. Tap %d" % (frame_number, ANIMATION_NUM_FRAMES, (current_interval*2)+3))
  
  x, y = zip(*sorted(data.items()))
  ln.set_data(x, y)
  ax.relim()   
  ax.autoscale_view()
  plt.title("Low Pass Filter for Tap#%d" % ((current_interval*2)+3))
  
# Create the plot
fig, ax = plt.subplots()
ax.set_xlabel('$Frequency (Hz)$')
ax.set_ylabel('$Amplitude (V/V)$')
#ax.set_aspect('equal')
ln, = ax.plot([])

# Animate the plot
anim = animation.FuncAnimation(fig, animate, frames=ANIMATION_NUM_FRAMES, interval=100)
#writermp4 = animation.FFMpegWriter(fps=60) 
#anim.save('test1.mp4', writer=writermp4, dpi=300)
plt.show()
