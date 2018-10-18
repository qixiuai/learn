import pandas as pd
from fbprophet import Prophet

df = pd.read_csv('../data/example_wp_log_peyton_manning.csv')
df.head()
