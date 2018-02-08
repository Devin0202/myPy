from scipy.optimize import curve_fit  
import matplotlib.pyplot as plt  
import numpy as np

# inputForXY[0, :] represents x axis
# inputForXY[1, :] represents y axis

inputForXY = np.array([[-5,  -3,  56, -66, -10, 119, 114,-131,-122,  -2, 180, -10,-187,-226, 231, 228,-242,-294,   1, 294, -14,-337,-310, 326, 325], \
						[13, -45,  17,  13,  71,-101, 135, 129,-101,-158,  18, 191,  12,-205,-209, 249, 235,   8,-267,  17, 304, 324,-289,-299, 345]])
fitGoalX = np.array([-5,  -6,  56, -66,  -6, 116, 116,-124,-125,  -4, 176,  -4,-187,-244, 236, 235,-244,-304,  -5, 295,  -5,-364,-365, 355, 355])
fitGoalY = np.array([13, -47,  13,  13,  73,-107, 133, 133,-106,-168,  12, 192,  12,-227,-226, 253, 253,  12,-286,  13, 313, 359,-347,-346, 358])
'''
inputForXY = np.array([[-5, -67, 57, -2, -7, -230, 235, 288, -242, 0, 447, -11, -429], \
						[16, 12, 14, -103, 134, -155, -156, 190, 235, -215, 18, 303, 8]])
fitGoalX = np.array([-5, -60, 51, -5, -5, -225, 216, 271, -224, -4, 435, -4, -444])
fitGoalY = np.array([16, 15, 16, -95, 125, -149, -149, 181, 235, -204, 16, 292, 16])
'''
def fitY(x, a, b, c, d, e, f, g, h, i, j, k, l):
	#print(a * x[1] * x[1] + b * x[1] + c)
	#print(d * x[1] * x[1] + e * x[1] + f)
	#print(g * x[1] * x[1] + h * x[1] + i)
	#print(j * x[1] * x[1] + k * x[1] + l)
	#print
	return (a * x[1] * x[1] + b * x[1] + c) * x[0] * x[0] + (d * x[1] * x[1] + e * x[1] + f) * x[0] + (g * x[1] * x[1] + h * x[1] + i) + (j * x[1] * x[1] + k * x[1] + l) * x[1]

def fitX(x, a, b, c, d, e, f, g, h, i, j, k, l):
    return (a * x[0] * x[0] + b * x[0] + c) * x[1] * x[1] + (d * x[0] * x[0] + e * x[0] + f) * x[1] + (g * x[0] * x[0] + h * x[0] + i) + (j * x[0] * x[0] + k * x[0] + l) * x[0]

#print(inputForXY)
popt, pcov = curve_fit(fitY, inputForXY, fitGoalY)
print(popt)
for i in range(fitGoalY.size):
    print(inputForXY[:, i])
    print("Y COMPARE")
    print(fitY(inputForXY[:, i], popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11]))
    print(fitGoalY[i])

test = np.array([55, 30])
print("TEST")
print(fitY(test, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11]))

#inputForXY[[0, 1], :] = inputForXY[[1, 0], :]
#print(inputForXY)
popt, pcov = curve_fit(fitX, inputForXY, fitGoalX)
print(popt)
for i in range(fitGoalX.size):
    print(inputForXY[:, i])
    print("X COMPARE")
    print(fitX(inputForXY[:, i], popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11]))
    print(fitGoalX[i])

test = np.array([55, 30])
print("TEST")
print(fitX(test, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8], popt[9], popt[10], popt[11]))