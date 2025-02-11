import pandas as pd
import fireducks.pandas as fpd
import numpy as np
import time

num_rows = 100000000 # 100 MILLION
df_pandas = pd.DataFrame({
    'A': np.random.randint(1, 100, num_rows),
    'B': np.random.rand(num_rows),
})

df_fireducks = fpd.DataFrame(df_pandas)

start_time = time.time()
result_pandas = df_pandas.groupby('A')['B'].sum()
pandas_time = time.time() - start_time
print(f"Pandas execution time: {pandas_time:.4f} seconds")

start_time = time.time()
result_fireducks = df_fireducks.groupby('A')['B'].sum()
fireducks_time = time.time() - start_time
print(f"FireDucks execution time: {fireducks_time:.4f} seconds")

speed_up = pandas_time / fireducks_time
print(f"FireDucks is approximately {speed_up:.2f} times faster than pandas.")