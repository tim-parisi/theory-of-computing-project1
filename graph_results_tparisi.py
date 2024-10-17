#!/usr/bin/python3
import sys
import os
import matplotlib.pyplot as plt

def graph(Xt, Yt, Xf, Yf):
    fig, ax = plt.subplots()
    
    # Data
    ax.scatter(Xt,Yt, c='#00ff00')
    ax.scatter(Xf,Yf, c='#ff0000')
    xMax, yMax = find_max_line(Xt, Yt, Xf, Yf)
    ax.plot(xMax, yMax, c='#000000')
    
    # Formatting
    plt.title("Time of k-Partite Matchings")
    plt.ylabel("Time (seconds)")
    plt.xlabel("Number of nodes")    
    plt.show()
    
    
def find_max_line(Xt, Yt, Xf, Yf):
    X_both = Xt + Xf
    Y_both = Yt + Yf
    times = {}
    for it in range(len(X_both)):
        if times.get(X_both[it], 0) < Y_both[it]:
            times[X_both[it]] = Y_both[it]
    time_keys_sorted = sorted(times, key=lambda x: x)
    max_X = []
    max_Y = []
    for ix in range(len(time_keys_sorted)):
        key = time_keys_sorted[ix]
        if time_keys_sorted[ix] < 2:
            continue
        max_X.append(key)
        max_Y.append(times[key])
        
    return max_X, max_Y

def remove_outliers(Xt, Yt, Xf, Yf):
    for ix in range(len(Yt)):
        if Yt[ix] > 30:
            Xt.pop(ix)
            Yt.pop(ix)
    for jx in range(len(Yf)):
        if Yf[ix] > 30:
            Xf.pop(ix)
            Yf.pop(ix)