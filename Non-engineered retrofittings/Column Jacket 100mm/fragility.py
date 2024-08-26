import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os
import pandas as pd
os.chdir(r"E:\4th year project\opensees\Pushover all typology\Non engineered buildings\column jacketing\Column Jacket 100mm")
# Read earthquake data from "maxx_values.txt"
with open("maxx_values.txt", "r") as file:
    data = file.read()

# Initialize arrays to store data
pga = []
earthquake = []
drift = []

# Extract data using regular expressions
pattern = re.compile(r'drift_(\d+\.\d+)g_([\w_]+)\.out:\s+([\d\.]+)')
matches = pattern.findall(data)

# Populate arrays
for match in matches:
    pga.append(float(match[0]))
    earthquake.append(match[1])
    drift.append(float(match[2]))

# Plotting
plt.figure(figsize=(10,6))
for eq in set(earthquake):
    index = []
    for i, x in enumerate(earthquake):
        if x == eq:
            index.append(i)
    plt.plot([pga[i] for i in index], [drift[i] for i in index], 'o-',label=eq)

plt.xlabel('PGA')
plt.ylabel('Drift')
plt.legend()
plt.title('IDA Curve')
plt.grid(True,linestyle='--',alpha=0.7)
plt.show()


######### Plotting ln(IDA)


lnPGA = np.log(pga)
lnDRIFT = np.log(drift)

# Linear regression
a = np.polyfit(lnPGA, lnDRIFT, 1)   # 1 for first order polinomial fitting ie a straight line 
fit = np.polyval(a, lnPGA) 

# Calculate R-squared
SSres = np.sum((lnDRIFT - fit)**2)
SStot = np.sum((lnDRIFT - np.mean(lnDRIFT))**2)
R2 = 1 - SSres / SStot


# Plotting regression line
plt.figure()
plt.scatter(lnPGA, lnDRIFT, label='Data', color='blue', alpha=0.7)
plt.plot(lnPGA, fit, '-', label=f'Regression line: {a[1]:.4f} + {a[0]:.4f} ln(PGA)')
plt.text(-2, -1, f'R^2 = {R2:.4f}', color='k', fontsize=10)
plt.xlabel('ln(PGA)', fontsize=12)
plt.ylabel('ln(Drift)', fontsize=12)
plt.legend()
plt.grid()
plt.show()

# Calculate fragility curves
LAMBDA = a[1] + a[0] * lnPGA #linear fit y values
EXP1 = (lnDRIFT - LAMBDA)**2 #squared residuals or squared errors
n = lnPGA.size
BETA = (np.sum(EXP1) / (n - 2))**0.5 #standard deviation of the residuals

PGA_FRAG = np.arange(0.01, 1.01 , 0.01) #PGA_FRAG = range of fragility curve ranging from 0.01 to 2.0 with a step size of 0.01. 
LAMBDA_FRAG = a[1] + a[0] * np.log(PGA_FRAG) # calculates the expected values for the fragility curve

# Define limit states and calculate probabilities
LS_IO = 1 ;  LS_LS = 2 ;  LS_CP = 4
P_IO = 1 - norm.cdf(np.log(LS_IO), LAMBDA_FRAG, BETA) #calculated using (CDF) of the normal distribution 
P_LS = 1 - norm.cdf(np.log(LS_LS), LAMBDA_FRAG, BETA) #probability of exceeding a specified limit state (LS_X) based on a fragility curve.
P_CP = 1 - norm.cdf(np.log(LS_CP), LAMBDA_FRAG, BETA)

fig=plt.figure(figsize=(10, 6))
plt.plot(PGA_FRAG, P_IO, '-', markersize=5, label='Operational', color='blue')
plt.plot(PGA_FRAG, P_LS, '-', markersize=5, label='Life Safety', color='green')
plt.plot(PGA_FRAG, P_CP, '-', markersize=5, label='Collapse Prevention', color='red')
plt.xlabel('PGA (g)', fontsize=14)
plt.ylabel('Probability of exceeding limit state', fontsize=14)
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.title('Fragility Curve of Engineered Building', fontsize=16)
plt.show()

data= {
    'PGA'     : PGA_FRAG,
    f'LS_{LS_IO}%' : P_IO,
    f'LS_{LS_LS}%' : P_LS,
    f'LS_{LS_CP}%' : P_CP   
}

df = pd.DataFrame(data)
# Define the output Excel file path
output_excel_file = 'fragilitydata.xlsx'
# Export the DataFrame to Excel
df.to_excel(output_excel_file, index=False)

# filename='fragility.png'
# fig.savefig(filename,dpi=300)
