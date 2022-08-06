import numpy as np
from PID_Graph import PID_Graph

pid_plot = PID_Graph(widgets=True)

class PID:
    def __init__(self, kp=0.0, ki=0.0, kd=0.0, dt=0.1):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.bound = 5.0

        self.dt = dt
        self.last_signal = 0.0
        self.sum_error = 0.0

    # limit the signal between an arbitrary interval
    def _limit_signal(self, signal):
        return np.sign(signal)*self.bound if (signal > self.bound or signal < -self.bound) else signal 
    
    # compute the signal value required to achieve a given target
    def compute_pid(self, sig, target):
        error = target - sig
        delta_signal = sig - self.last_signal # use derivative on signal measurement, *not* derivative on error

        self.sum_error += error  * self.dt
        self.sum_error = self._limit_signal(self.sum_error)

        signal = self.kp*error + self.ki*self.sum_error + self.kd*(delta_signal/self.dt)
        signal = self._limit_signal(signal)

        self.last_signal = sig

        return signal

# compute a signal response over a period of discrete time
def pid_loop_update(val):
    kp, ki, kd, signal = pid_plot.get_slider_values()
    pid = PID(kp, ki, kd)
    target_signal = pid_plot.get_target_signal()
    
    signal_list = [signal] # needed to create the plot
    for time in range(pid_plot.get_graph_size()-1):
        signal = pid.compute_pid(signal, target_signal[time])
        signal_list.append(signal)
        
    pid_plot.update_signal_plot(signal_list)

pid_plot.add_event_listeners(pid_loop_update)
pid_plot.display_plot()

kp, ki, kd, _, = pid_plot.get_slider_values()
print(f"The last parameters were: P: {kp} - I: {ki} - D: {kd}")