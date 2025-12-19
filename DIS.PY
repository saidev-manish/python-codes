import threading
import time

def print_even():
    for i in range(0, 11, 2):
        print("Even:", i)
        time.sleep(0.5)

def print_odd():
    for i in range(1, 11, 2):
        print("Odd :", i)
        time.sleep(0.5)

# Creating threads
t1 = threading.Thread(target=print_even)
t2 = threading.Thread(target=print_odd)

# Starting threads
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()
t2.join()

print("Done!")
