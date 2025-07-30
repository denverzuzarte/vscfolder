def measure_flops():
    import time
    x = 1.0
    count = 0
    end_time = time.perf_counter() + 20  # one second from now
    while time.time() < end_time:
        x += 1.0
        count += 1.0
    return count/2

print(measure_flops())