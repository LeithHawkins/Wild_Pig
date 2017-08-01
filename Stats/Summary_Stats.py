import numpy as np
import pandas as pd

df = pd.read_csv("N:\\Wild_Pig_Project\\GI_Combined_Test.csv")
list(df['Device_ID'].groupby(df['Device_ID']))

