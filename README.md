# NuRS_Data_Processing

Tools for processing data received during the NuRS research project. 
Current focus is on measuring the data quality via automated methods. 

## API functions

To identify patterns of missing data - there is an exposed python function, `mine_missing`:

```python
import pandas as pd
from nurs_data_processing import mine_missing

data = pd.read_csv('file_path')
mine_missing(data) 
```

## Theory 

For guidance on the theory of missingness and reasoning behind the models applied see Documents/...
