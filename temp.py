import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import datetime

from decimal import Decimal, ROUND_DOWN

fig = pyplot.figure()
ax1 = fig.add_subplot(111)

def refreshGraphData(i):
	print("Refreshing data...")
	graphData = open("BNBUSDT-price.csv", "r").read()
	lines = graphData.split("\n")
	yValues = []
	xValues = []
	for line in lines:
		if len(line) > 1:
			x, y = line.split(",")
			print(x)
			xValues.append(str(datetime.datetime.fromtimestamp(Decimal(x)/1000)))
			yValues.append(float(y))

	print(yValues)
	ax1.clear()
	ax1.plot(yValues)

ani = animation.FuncAnimation(fig, refreshGraphData, interval=1000)
pyplot.show()