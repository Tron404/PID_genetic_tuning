import collections
import matplotlib.pyplot as plt
import numpy as np
import signals

from matplotlib.widgets import Slider, Button, RadioButtons

## graph class to separate the visual part from the computation part
class PID_Graph:
    # constructor, func = function that creates a signal
    def __init__(self, func=signals.constant_sig, graph_size=100, widgets=False):
        self.graph_size = graph_size
        self.widgets = collections.defaultdict(list)
        self.func = func
        self.target_signal = func(graph_size)
        self.x_range = np.linspace(0, self.graph_size, num=self.graph_size)
        
        self.init_plot()
        if widgets:
            self.create_widgets()

    # generate the initial target and signal plots
    def init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.target_graph, = self.ax.plot(self.x_range, self.target_signal, linewidth=2) # target signal
        self.graph, = self.ax.plot(self.x_range, np.full((self.graph_size,), 0.0), linewidth=2) # initial signal
        self.ax.set_ylim((-6,6))

        # extra graph customisation
        self.ax.set_ylim((-6, 6))
        self.fig.set_dpi(175)
        plt.grid()
        plt.title("PID - Virtual simulation of a control signal")

    # create the interactive elements of the plot
    def create_widgets(self):
        plt.subplots_adjust(left=0.1, bottom=0.1, right=0.5, top=0.8)
        # ax positions
        p_ax = plt.axes([0.63, 0.55, 0.3, 0.03])
        i_ax = plt.axes([0.63, 0.49, 0.3, 0.03])
        d_ax = plt.axes([0.63, 0.43, 0.3, 0.03])
        sig_ax = plt.axes([0.63, 0.37, 0.3, 0.03])
        sig_type = plt.axes([0.63, 0.1, 0.3, 0.25])

        p_slider = Slider(p_ax, "K_p", 0.0, 10.0, 0.0, valstep=0.1)
        i_slider = Slider(i_ax, "K_i", 0.0, 100.0, 0.0, valstep=1.0)
        d_slider = Slider(d_ax, "K_d", -1.0, 1.0, 0.0,valstep=0.01)
        signal_slider = Slider(sig_ax, "Signal", 0.0, 3.0, 0.0)
        reset_button = Button(plt.axes([0.64, 0.6, 0.3, 0.3]), "Reset")
        sig_type_buttons = RadioButtons(sig_type, ("Constant Signal", "Cosine", "Custom Signal"))

        self.add_widget(p_slider, "slider")
        self.add_widget(i_slider, "slider")
        self.add_widget(d_slider, "slider")
        self.add_widget(signal_slider, "slider")
        self.add_widget(reset_button, "button")
        self.add_widget(sig_type_buttons, "radio_buttons")
    
    # event that will reset to the default state all sliders and consequently the graph
    def reset_graph(self, val):
        for w in self.widgets["slider"]:
            w.reset()

    # change the graph of the plant's signal
    def update_signal_plot(self, signal):
        self.graph.set_ydata(signal)
        plt.draw()

    # change the target graph based on a given signal function
    def update_target_graph(self, label):
        if label == "Constant Signal":
            self.func = signals.constant_sig
        elif label == "Cosine":
            self.func = signals.cosine_sig
        elif label == "Custom Signal":
            self.func = signals.custom_sig
        self.target_signal = self.func(self.graph_size)
        self.target_graph.set_ydata(self.target_signal)
        self.reset_graph(None)
        plt.draw()

    # add a widget of a certain type to the internal dictionary of widgets
    def add_widget(self, w, type):
        self.widgets[type].append(w)

    # add event listeners to the widgets, with a certain function given
    def add_event_listeners(self, function):
        for key in self.widgets:
            for w in self.widgets[key]:
                if key == "slider":
                    w.on_changed(function)
                elif key == "button":
                    w.on_clicked(self.reset_graph)
                elif key == "radio_buttons":
                    w.on_clicked(self.update_target_graph)    

    # display the plot to the screen
    def display_plot(self):
        plt.show()

    def get_graph_size(self):
        return self.graph_size

    def get_target_signal(self):
        return self.target_signal

    def get_slider_values(self):
        values = []
        for s in self.widgets["slider"]:
            values.append(s.val)
        return values