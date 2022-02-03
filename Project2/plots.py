import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join


files_tmp = [f for f in listdir("Data") if isfile(join("Data", f))]
files = []
for file in files_tmp:
    file = 'Data/' + file
    files.append(file)
print(files)
    

afraid_large = files[0:10]
afraid_walls = files[11:20]
confused_large = files[21:30]
confused_walls = files[31:40]
scared_large = files[41:50]
scared_walls = files[51:60]


df_afraid =[] # Afraid without walls
for file in afraid_large:
    df = pd.read_csv(file, sep = ";", header=None)
    df_afraid.append(df)

df_afraid_large = pd.concat(df_afraid, axis=1)
uncert_afraid = np.median(df_afraid_large.iloc[-1:, ::2])
qual_afraid = np.median(df_afraid_large.iloc[-1:, 1::2])

df_afraid2 =[] # Afraid  walls
for file in afraid_walls:
    df = pd.read_csv(file, sep = ";", header=None)
    df_afraid2.append(df)

df_afraid_walls = pd.concat(df_afraid2, axis=1)
uncert_afraid_walls = np.median(df_afraid_walls.iloc[-1:, ::2])
qual_afraid_walls = np.median(df_afraid_walls.iloc[-1:, 1::2])

df_confused =[] # Confused without walls
for file in confused_large:
    df = pd.read_csv(file, sep = ";", header=None)
    df_confused.append(df)

df_confused_large = pd.concat(df_confused, axis=1)
uncert_confused = np.median(df_confused_large.iloc[-1:, ::2])
qual_confused = np.median(df_confused_large.iloc[-1:, 1::2])

df_confused2 =[] # Confused  walls
for file in confused_walls:
    df = pd.read_csv(file, sep = ";", header=None)
    df_confused2.append(df)

df_confused_walls = pd.concat(df_confused2, axis=1)
uncert_confused_walls = np.median(df_confused_walls.iloc[-1:, ::2])
qual_confused_walls = np.median(df_confused_walls.iloc[-1:, 1::2])

df_scared =[] # Scared without walls
for file in scared_large:
    df = pd.read_csv(file, sep = ";", header=None)
    df_scared.append(df)

df_scared_large = pd.concat(df_scared, axis=1)
uncert_scared = np.median(df_scared_large.iloc[-1:, ::2])
qual_scared = np.median(df_scared_large.iloc[-1:, 1::2])

df_scared2 =[] # Scared walls
for file in scared_walls:
    df = pd.read_csv(file, sep = ";", header=None)
    df_scared2.append(df)

df_scared_walls = pd.concat(df_scared2, axis=1)
uncert_scared_walls = np.median(df_scared_walls.iloc[-1:, ::2])
qual_scared_walls = np.median(df_scared_walls.iloc[-1:, 1::2])




plt.errorbar(1, uncert_scared, yerr = [[0.05], [0.95]],fmt='.k', capsize = 4, capthick = 1, color = "turquoise", label = "Scared large filter")
plt.errorbar(2, uncert_scared_walls, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color = "mediumseagreen", label = "Scared large filter with walls")
plt.errorbar(3, uncert_afraid, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color = "cornflowerblue", label = "Afraid large filter")
plt.errorbar(4, uncert_afraid_walls, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color = "mediumblue", label = "Afraid large filter with walls")
plt.errorbar(5, uncert_confused, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color= "purple",  label = "Confused large filter")
plt.errorbar(6, uncert_confused_walls, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color = "indigo", label = "Confused large filter with walls")
plt.legend(loc ='upper left')
plt.show()

plt.errorbar(1, qual_scared, yerr = [[0.05], [0.95]],fmt='.k', capsize = 4, capthick = 1, color = "turquoise", label = "Scared large filter")
plt.errorbar(2, qual_scared_walls, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color = "mediumseagreen", label = "Scared large filter with walls")
plt.errorbar(3, qual_afraid, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color = "cornflowerblue", label = "Afraid large filter")
plt.errorbar(4, qual_afraid_walls, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color = "mediumblue", label = "Afraid large filter with walls")
plt.errorbar(5, qual_confused, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color= "purple",  label = "Confused large filter")
plt.errorbar(6, qual_confused_walls, yerr = [[0.05], [0.95]], fmt='.k', capsize = 4, capthick = 1, color = "indigo", label = "Confused large filter with walls")
plt.legend(loc ='upper left')
plt.show()