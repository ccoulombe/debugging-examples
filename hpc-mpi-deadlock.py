import faulthandler
import signal
from mpi4py import MPI

# Registers SIGUSR1 in each MPI rank (process) to print its traceback
faulthandler.register(signal.SIGUSR1, all_threads=True)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    print("Rank 0 is waiting for rank 1...")
    # Bug: Rank 0 waits for a message that will never be sent
    data = comm.recv(source=1, tag=11)  # Rank 0 process blocks here
else:
    print(f"Rank {rank} is busy...")
    import time
    while True:
        time.sleep(1)  # Other rank process loops here
