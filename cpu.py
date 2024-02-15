import psutil
import time


def measure_cpu_utilization():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    print(f"CPU utilization: {cpu_percent}%")


if __name__ == "__main__":
    measure_cpu_utilization()
