import multiprocessing
import random
from multiprocessing.shared_memory import SharedMemory

def worker(num):
    shared_mem = SharedMemory(name='Mem', create=False)
    count = 0
    for i in range(500000):
        if random.randint(1, 1000000) == 1:
            print(f"Stoping in {num}")
            shared_mem.buf[0] = num
            return

        if random.randint(1, 10000) <= 100:
            print(f"{count} in {num}")
            count += 1
        if shared_mem.buf[0] != 0:
            print("Another thread stopped.")
            return


if __name__ == "__main__":
    shared_mem = SharedMemory(name='Mem', size=8, create=True)
    shared_mem.buf[0] = 0
    procs = []
    for i in range(1, 6):
        p = multiprocessing.Process(target=worker, args=(i,))
        procs.append(p)
        p.start()
    print("launched")
    for p in procs:
        p.join()
    print("Done")
