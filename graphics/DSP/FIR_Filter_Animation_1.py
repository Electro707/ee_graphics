#!/usr/bin/python3
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
import argparse


class MainAnimation:
    def __init__(self, **kwargs):
        self.lp_f = 800     # The low pass filter's cutoff frequency
        self.sr = 8E3       # The sampling rate
        self.numb_frames_per_tap = 10     # The number of frames per tap increment

        self.export_video = False
        self.export_video_name = None

        self.do_linear_interpolation = not kwargs['linear_interpolation']
        if 'export_video_name' in kwargs:
            self.export_video = True
            self.export_video_name = kwargs['export_video_name']

        self.max_taps = 120 - 2     # The number of taps to up to. Offset that amount by 2 to account for the startup of 3 taps

        # Internal variable stuff
        self.num_anim_frames = self.max_taps * self.numb_frames_per_tap
        self.omega_c = 2*numpy.pi*self.lp_f/self.sr

        # Data for animation
        self.next_frame_data = None
        self.current_frame_data = None
        self.current_frame_num = None

        # Create the plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('$Frequency (Hz)$')
        self.ax.set_ylabel('$Amplitude (V/V)$')
        self.ln, = self.ax.plot([])

        # Animate the plot
        self.animFunc = animation.FuncAnimation(self.fig, self._animate_callback, frames=self.num_anim_frames, interval=1)

    @staticmethod
    def get_mag_angle(eq):
        """
            Function that takes a number and returns the magnitude and phase
        """
        return numpy.abs(eq), numpy.degrees(numpy.angle(eq))

    @staticmethod
    def hz_e(b_coef, o):
        """
            Function to calculate the response of the filter for a given b coefficients
            and a normalized frequency (between 0 and pi)
        """
        sum = 0
        for key in b_coef:
            sum += b_coef[key]*numpy.exp(-o*1j*key)
        return sum


    @staticmethod
    def get_numb_taps(interval: int) -> int:
        """
            Helper function to get the number of taps given the current interval number
        """
        return 3 + interval

    def calculate_response(self, tap_numb: int):
        """
            Function to calculate the response of the filter with a given number of
            taps
        """
        m = (tap_numb-1)//2
        h = {0: self.omega_c/numpy.pi}
        for i in range(1, m+1):
            h[i] = numpy.sin(self.omega_c*i)/(i*numpy.pi)
            h[-i] = h[i]

        b = {}
        for i in range(0, len(h)):
            b[i] = h[i-m]

        data = {}
        for i in numpy.linspace(0, float(numpy.pi), 300):
            data[i*self.sr/(2*numpy.pi)] = self.get_mag_angle(self.hz_e(b, i))[0]
        return data

    def _animate_callback(self, frame_number):
        """
            Animation function MatPlotLib uses to do the plotting
        """
        current_interval = frame_number // self.numb_frames_per_tap
        numb_taps = self.get_numb_taps(current_interval)
        print("Frame %d out of %d. Tap %d" % (frame_number, self.num_anim_frames, numb_taps))
        if self.current_frame_num is None or self.current_frame_num != current_interval or frame_number == 0:
            self.current_frame_num = current_interval
            if self.next_frame_data is not None:
                self.current_frame_data = self.next_frame_data.copy()
            else:
                self.current_frame_data = self.calculate_response(numb_taps).copy()
            self.next_frame_data = self.calculate_response(numb_taps).copy()
            data = self.current_frame_data
        else:
            if self.do_linear_interpolation:
                data = {}
                for d_k in self.current_frame_data:
                    data[d_k] = self.current_frame_data[d_k] + (frame_number-(current_interval*self.numb_frames_per_tap)) * (self.next_frame_data[d_k] - self.current_frame_data[d_k]) / self.numb_frames_per_tap
            else:
                data = self.current_frame_data

        x, y = zip(*sorted(data.items()))
        self.ln.set_data(x, y)
        self.ax.relim()
        self.ax.autoscale_view()
        plt.title("Low Pass Filter for Tap#%d" % (current_interval+3))

    def animate(self):
        if self.export_video:
            writermp4 = animation.FFMpegWriter(fps=60)
            self.animFunc.save(self.export_video_name, writer=writermp4, dpi=300)
            print("Done with exporting video")
        else:
            plt.show()
  

def setup_parser():
    return_kargs = {}
    parser = argparse.ArgumentParser(description='FIR Animation #1')
    parser.add_argument('--export_file', metavar='File', type=str, default=None, help='The mp4 file name to export the animation to')
    parser.add_argument('--no_linear_interpolation', action='store_false', help='Whether to add linear interpolation in the annimation or not.')
    parser.add_argument('--numb_taps', type=int, help='The number of taps for this animation')

    args = parser.parse_args()

    if args.export_file is not None:
        export_video_name = args.export_file
        if export_video_name.endswith('.mp4') is False:
            return_kargs['export_video_name'] = export_video_name + '.mp4'
    return_kargs['linear_interpolation'] = not args.no_linear_interpolation

    return return_kargs


if __name__ == '__main__':
    p = setup_parser()
    m = MainAnimation(**p)
    m.animate()
