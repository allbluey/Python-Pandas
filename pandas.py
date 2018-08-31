import pandas as pd
import numpy as np
import plolty
import plotly.plotly
import plotly.graph_objs as go
import plotly.tools as tls
import cufflinks as cf
import matplotlib.pyplot as  plt



chuva = pd.read_csv("http://www.ime.unicamp.br/~gvludwig/2018s2-me315/INMET-14JAN2018-14AUG2018-SOROCABA.csv")

#structure
chuva.info()
# replace '///' for NA values
chuva['precipitacao']  = chuva['precipitacao'].replace('////', np.NaN)
# Transform 'precitação' column in float
chuva['precipitacao'] = chuva['precipitacao'].astype(float)

# Exclude the first and last row
chuva  = chuva.drop(chuva.index[[-0,-4975]])

# chuva['precipitacao'].value_counts()
# sum of 'precipitação' per day
chuvadia = chuva.groupby('data')['precipitacao'].sum().reset_index()

# Accumulation of total rain in period of 10 days. There are 212 days

chuvacumula = pd.Index(range(chuvadia['precipitacao'].shape[0])) // 10
chuvacumula = chuvadia.groupby(chuvacumula, axis = 0).sum() # table  with the sum by every 10 days


# exclude the  NaN values for construct a time series graph

chuvadia = chuvadia.dropna()

# plotly graph
graph = [go.Scatter( x = chuvadia['data'], y = chuvadia['precipitacao'])]
plotly.offline.plot(graph)  # abre o gráfico em formato html

# function for exponential smoothing


def alis_exp(alpha, x):
    if (alpha <= 0.0) | (alpha >= 1.0):
        raise ValueError("alpha must be a number between 0 and 1.")
    else:
        y = np.empty(len(x)-1 , float)
        y[0] = x[0]
        for i in range(1, len(x)-1):
            y[i] = x[i]*alpha + y[i-1]*(1-alpha)
        return y
# exponential smoothing for alpha = 0.2 and alpha = 0.8
e1 = alis_exp(0.2,chuvacumula['precipitacao'])
e2 = alis_exp(0.8,chuvacumula['precipitacao'])

# Graph for exponential smoothing of e1 and e2
Ge1 = go.Scatter(
    y = e1,
    mode = 'lines',
    name = '0.2'
)

Ge2 = go.Scatter(
    y = e2,
    mode = 'lines',
    name = '0.8'
)
layout = go.Layout(
    title='Alisamento exponencial para alfa 0.2 e 0.8')

expGraph = [Ge1,Ge2]

Expfig = go.Figure(data=expGraph, layout=layout)
plotly.offline.plot(Expfig)

# baby names dataframe

baby = pd.read_csv("http://www.ime.unicamp.br/~gvludwig/2018s2-me315/baby-names.csv")

# separete the tables
baby_girl = baby.query('sex == "girl"')
baby_boy = baby.query('sex == "boy"')

# building a new column just with the last letter of name

baby_boy['last'] = baby_boy['name'].astype(str).str[-1]
baby_girl['last'] = baby_girl['name'].astype(str).str[-1]

#  a list with the total number of last letter occurrences per decade

lastletter_boy = baby_boy.groupby((baby_boy.year // 10) * 10)['last'].value_counts()
lastletter_girl = baby_girl.groupby((baby_girl.year // 10) * 10)['last'].value_counts()

# How to sort the columns and some missing data we use:

# for boys
temp_boy = lastletter_boy.to_frame()
temp_boy = temp_boy.rename(columns={'year':'year','last':'last','last':'count'}).reset_index()
freq_boys = temp_boy.pivot_table(index = 'year', columns = 'last', values = 'count').reset_index()

# for girls

temp_girl = lastletter_girl.to_frame()
temp_girl= temp_girl.rename(columns={'year':'year','last':'last','last':'count'}).reset_index()
freq_girls = temp_girl.pivot_table(index = 'year', columns = 'last', values = 'count').reset.index()



# graph to observe the evolution of the number of letters in male names in recent decades
# use import cufflinks as cf

# for boys
plotly.offline.plot([{
    'x': freq_boys['year'],
    'y': freq_boys[col],
    'name': col
}  for col in freq_boys.columns[1:26]])


# for girls
plotly.offline.plot([{
    'x': freq_girls['year'],
    'y': freq_girls[col],
    'name': col
}  for col in freq_girls.columns[1:26]])

