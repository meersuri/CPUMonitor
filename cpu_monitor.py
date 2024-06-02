import collections
import psutil
import time
import sys
import threading

import matplotlib.pyplot as plt
import matplotlib.animation as anim

class ProcessCPUMonitor:
    def __init__(self, pid, buffer_size=200, sample_interval=0.2, plot_interval=200):
        self._pid = pid
        self._cpu_percent_readings = collections.deque(maxlen=buffer_size)
        self._times = collections.deque(maxlen=buffer_size)
        self._sample_interval = sample_interval
        self._fig, self._ax = plt.subplots()
        self._ax.set_title("CPU monitor")
        self._ax.set_xlabel("Time")
        self._ax.set_ylabel("CPU usage")
        self._ax.set_yticks(list(range(0, 100, 10)))
        self._ax.set_xticks([])
        self._ax.set_ylim(0, 100)
        self._line, = self._ax.plot([], [])
        self._frames = []
        self._plot_interval = plot_interval
        self._thread = threading.Thread(target=self._measure, daemon=True)

    def run(self):
        self._thread.start()
        self._plot()

    def _measure(self):
        process = psutil.Process(self._pid)
        t = 0
        try:
            while True:
                usage = process.cpu_percent(interval=self._sample_interval)
                self._cpu_percent_readings.append(usage/24)
                self._times.append(t)
                t += self._sample_interval
                self._frames.append((t, usage))
        except KeyboardInterrupt:
            return

    def _animation_func(self, i):
        self._line.set_data(list(self._times), list(self._cpu_percent_readings))
        self._ax.relim()
        self._ax.autoscale_view()
        return self._line,

    def _plot(self):
        animtion = anim.FuncAnimation(self._fig, self._animation_func, interval=self._plot_interval, blit=True, cache_frame_data=False)
        plt.show()


if __name__ == '__main__':
    mon = ProcessCPUMonitor(int(sys.argv[1]))
    mon.run()

