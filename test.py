from tqdm import tqdm
import time

for _ in tqdm(range(10), desc="Processing"):
    time.sleep(0.5)  # Simulasi proses
