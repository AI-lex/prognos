
import pandas as pd

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d

import tensorflow as tf
from tensorflow import keras


path = os.path.abspath(".")
filepath = "/data/AAPL.csv"

data = pd.read_csv(path + filepath, parse_dates=["Date"])




#data.plot(x="Date", y="Open")

data_past_2010 = data[data["Date"] > "2010"].copy()
data_before_2010 = data[data["Date"] <= "2010"].copy()



#data_past_2010.plot(x="Date", y="Open")
#data_before_2010.plot(x="Date", y="Open")


#sns.lineplot(x=data_past_2010["Date"].to_numpy(), y="Open", data=data_past_2010)


#d_month_mean = data_past_2010.set_index("Date").resample("M").mean()
#d_month_median = data_past_2010.set_index("Date").resample("M").median()

#sns.lineplot(x=d_month_mean.index, y="Open", data=d_month_mean)
#sns.lineplot(x=d_month_median.index, y="Open", data=d_month_median)




#X=data_past_2010.index.to_numpy()
#Y=data_past_2010["Open"].to_numpy()
#f1 = interp1d(X, Y)
#f2 = interp1d(X, Y, kind='cubic')

#plt.plot(X, Y, 'o', X, f1(X), '-', X, f2(X), '--')
#plt.legend(['data', 'linear', 'cubic'], loc='best')
#plt.show()


# prepare data
### test train split
close_values = pd.DataFrame()
close_values["close"] = data_past_2010.set_index("Date")["Close"].copy()

print(close_values["close"].shape)
close_values.plot()
#plt.show()


train_size = int(len(close_values) * 0.9)

train = close_values.iloc[:train_size]
test = close_values.iloc[train_size:]

print(train.shape, test.shape)
### scale data

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
print(train[["close"]])
scaler = scaler.fit(train[["close"]])

train["close"] = scaler.transform(train[["close"]])
test["close"] = scaler.transform(test[["close"]])

print(test.head())

def create_sequences(X, Y, TIME_STEPS):
    X_sequences, Y_sequences = [], []

    for i in range(len(X) - TIME_STEPS):
        seq_x = X.iloc[i: (i + TIME_STEPS)].to_numpy()
        seq_y = Y.iloc[i: (i + TIME_STEPS)]

        X_sequences.append(seq_x)
        Y_sequences.append(seq_y)

    return np.array(X_sequences), np.array(X_sequences)


TIME_STEPS = 30

x_train, y_train = create_sequences(train[["close"]], train["close"], TIME_STEPS)
x_test, y_test = create_sequences(test[["close"]], test["close"], TIME_STEPS)

print(x_train.shape, y_test.shape)

#### LSTM AUTOENCODER

model = keras.Sequential()
model.add(keras.layers.LSTM(
    units=64,
    input_shape=(x_train.shape[1], x_train.shape[2])
))

model.add(keras.layers.Dropout(rate=0.2))

model.add(keras.layers.RepeatVector(n=x_train.shape[1]))

model.add(keras.layers.LSTM(
    units=64,
    return_sequences=True
))

model.add(keras.layers.Dropout(rate=0.2))

model.add(keras.layers.TimeDistributed(keras.layers.Dense(
    units=x_train.shape[2]
)))

model.compile(loss="mae", optimizer="adam")

## train model

history = model.fit(
    x_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.1,
    shuffle=False
)

#plt.plot(history.history["loss"], label="train")
#plt.plot(history.history["val_loss"], label="test")
#plt.legend()
#plt.show()
print(history.history["loss"])

