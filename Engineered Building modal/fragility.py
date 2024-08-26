import numpy as np
import openseespy.opensees as ops
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import os
pga = []
drift = []
os.chdir(r"E:\4th year project\opensees\Pushover all typology\Engineered Building modal")
# Read data from maxx_values.txt
with open("maxx_values.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    # Split the line into filename and value
    value = line.strip().split()  
    # Extract the 7th, 8th, and 9th characters from each line
    pga_digits = line[6:9]
    pga.append(float(pga_digits))
    drift.append(float(value[1]))

# Load data

PGA = pga  #extracted from max_values
DRIFT = drift  #''
lnPGA = np.log(PGA)
lnDRIFT = np.log(DRIFT)

# Linear regression
a = np.polyfit(lnPGA, lnDRIFT, 1)   # 1 for first order polinomial fitting
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
LAMBDA = a[1] + a[0] * lnPGA
EXP1 = (lnDRIFT - LAMBDA)**2
n = lnPGA.size
BETA = (np.sum(EXP1) / (n - 2))**0.5

PGA_FRAG = np.arange(0.01, 2.01, 0.01) #PGA_FRAG = range of fragility curve
LAMBDA_FRAG = a[1] + a[0] * np.log(PGA_FRAG)

# Define limit states and calculate probabilities
LS_IO = 1 ;  LS_LS = 2;  LS_CP = 4
P_IO = 1 - norm.cdf(np.log(LS_IO), LAMBDA_FRAG, BETA) #calculated using (CDF) of the normal distribution 
P_LS = 1 - norm.cdf(np.log(LS_LS), LAMBDA_FRAG, BETA) #probability of exceeding a specified limit state (LS_X) based on a fragility curve.
P_CP = 1 - norm.cdf(np.log(LS_CP), LAMBDA_FRAG, BETA)

plt.figure(figsize=(10, 6))
plt.plot(PGA_FRAG, P_IO, '-', markersize=5, label='Operational', color='blue')
plt.plot(PGA_FRAG, P_LS, '-', markersize=5, label='Life Safety', color='green')
plt.plot(PGA_FRAG, P_CP, '-', markersize=5, label='Collapse Prevention', color='red')
plt.xlabel('PGA (g)', fontsize=14)
plt.ylabel('Probability of exceeding limit state', fontsize=14)
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.title('Fragility Curve of Engineered Building', fontsize=16)
plt.show()

#record all data in excel file
data= {
    'PGA'     : PGA_FRAG,
    'LS_1%' : P_IO,
    'LS_2%' : P_LS,
    'LS4_%' : P_CP   
}

df = pd.DataFrame(data)
# Define the output Excel file path
output_excel_file = 'fragilitydata.xlsx'
# Export the DataFrame to Excel
df.to_excel(output_excel_file, index=False)

# filename=f'fragility_curve0.5g.png'
# fig.savefig(filename,dpi=300)
