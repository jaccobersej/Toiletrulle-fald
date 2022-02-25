import math
import numpy
import matplotlib.pyplot as plt
#import pandas

inputA = input("input t værdi i sekunder: ")
inputB = input("input timestep længde i sekunder: ")
inputC = input("input start radius værdi i cm: ")
inputD = input("input tykkelsen af papiret i mm: ")
inputE = input("input pap cylinderens radius i cm: ")
inputF = input("input toiletrullens start masse her i kg: ")
timeValue = float(inputA)
stepLength = float(inputB)
startRadius = float(inputC) * 0.01  #unit conversion til m fra cm
paperThickness = float(inputD) * 0.001  #unit conversion til m fra mm
papRadius = float(inputE) * 0.01 #unit conversion til m fra cm
StartMass = float(inputF)
PreviousRadiusAtPreviousStep = startRadius
currentIndex = 1.00
a = True

piRatio = 2*math.pi
precisionCorrection = 0.01*stepLength

xRadiusPlot = []
yRadiusPlot = []
vinkelHastighed = []
xRotationsPlot = []
yRotationsPlot = []
vinkelTotal = 0


def RadiusRotation(timeValue, stepLength, PreviousRadiusAtPreviousStep, paperThickness, currentIndex, vinkelTotal):
    for currentIndex in numpy.arange(currentIndex, (timeValue/stepLength)+1.00, 1.00):
        tidspunkt = currentIndex*stepLength
        linærAcc = (2*9.82*(PreviousRadiusAtPreviousStep**2))/(papRadius**2+3*(PreviousRadiusAtPreviousStep**2)) #m/s^2 (acceleration)
        rotationelAcc = linærAcc/PreviousRadiusAtPreviousStep # 1/s^2 (hz eller vinkelhastigheds standard enheder)
        tension = (rotationelAcc*0.5*StartMass*(PreviousRadiusAtPreviousStep**2+papRadius**2))/(PreviousRadiusAtPreviousStep) # (kg * m)/s^2 (Newton)
        tensionAccel = tension/StartMass #m/s^2
        vinkel = (((tensionAccel*tidspunkt)/PreviousRadiusAtPreviousStep)*stepLength)
        ratio = vinkel/piRatio
        PreviousRadiusAtPreviousStep -= (ratio*paperThickness)
        #vinkelHastighed.append(vinkel)
        if currentIndex % 50 == 0:
            #linærAcc = (2*9.82*(PreviousRadiusAtPreviousStep**2))/(papRadius**2+3*(PreviousRadiusAtPreviousStep**2)) #m/s^2 (acceleration)
            #rotationelAcc = linærAcc/PreviousRadiusAtPreviousStep # 1/s^2 (hz eller vinkelhastigheds standard enheder)
            #tension = StartMass * 9.82 - StartMass * linærAcc # (kg * m)/s^2 (Newton)
            #tensionAccel = tension/StartMass #m/s^2
            tyngdekraftY = (0.5*(-9.82+(tensionAccel))*(tidspunkt**2)) #m
            xRadiusPlot.append(tidspunkt)
            yRadiusPlot.append(PreviousRadiusAtPreviousStep)
            xRotationsPlot.append(PreviousRadiusAtPreviousStep*math.cos(((tensionAccel*tidspunkt)/PreviousRadiusAtPreviousStep)*tidspunkt)) #opdateret efter vi fandt vinkel acceleration ud fra torque og tension.
            yRotationsPlot.append(PreviousRadiusAtPreviousStep*math.sin(((tensionAccel*tidspunkt)/PreviousRadiusAtPreviousStep)*tidspunkt)+tyngdekraftY) #opdateret efter vi fandt vinkel acceleration ud fra torque og tension.
        if PreviousRadiusAtPreviousStep <= papRadius:
            result(PreviousRadiusAtPreviousStep, tidspunkt, vinkelTotal)
            break
        if tidspunkt+precisionCorrection >= timeValue:
            result(PreviousRadiusAtPreviousStep, tidspunkt, vinkelTotal)
            break

#def radiusPlot():
    #plt.scatter(xRadiusPlot, yRadiusPlot, label="radius", color="blue", marker=".", s=30)
    #plt.xlabel("x - akse i sekunder")
    #plt.ylabel("y - akse i m")
    #plt.title("graf over radius")
    #plt.legend()
    #plt.show()

def positionPlot():
    plt.plot(xRotationsPlot, yRotationsPlot, label="position", color="blue",marker=",", linewidth=1, scalex=7, scaley= 4)
    plt.xlabel("x position i meter")
    plt.ylabel("y position i meter")
    plt.title("position i 2-dimensioner i meter")
    plt.axis('equal')
    plt.legend()
    plt.show()

#def coordsPlotToTime():
#    fig, (xCoords, yCoords) = plt.subplots(2, 1)
#    fig.suptitle('x pos og y pos i forhold til tid')
#    xCoords.plot(xRadiusPlot, xRotationsPlot, label="x position pr. tid", color="red", marker=",", linewidth=0.5)
#    yCoords.plot(xRadiusPlot, yRotationsPlot, label="y position pr. tid", color="blue", marker=",", linewidth=0.5)
#    plt.legend()
#    plt.show()

def result(PreviousRadiusAtPreviousStep, tidspunkt, vinkelTotal):
    print("____________________________________________________________________________________")   
    print("resultat = "+ str(PreviousRadiusAtPreviousStep) + " m, hvilket er tilsvarende til: " + str(PreviousRadiusAtPreviousStep*100) + " cm")  
    print("tiden er = "+ str(tidspunkt) +" s")
    print("Længden toiletrullen er faldet er = " + str(yRotationsPlot[len(yRotationsPlot)-1]) + " meter")
    print("Punktets x-position er = " + str(xRotationsPlot[len(xRotationsPlot)-1]) + " meter")
    #for x in range(0, len(vinkelHastighed)):
    #    vinkelTotal += vinkelHastighed[x]
    #print("Den samlede vinkel toiletrullen har roteret er = " + str(vinkelTotal) + " og det er tilsvarende til: " + str(vinkelTotal/piRatio) + " rotationer")
    #dataForExcel = {'tidspunkt i sekund': xRadiusPlot, 'vinkel hastighed (radianer)': vinkelHastighed}
    #dataFrameForExcel = pandas.DataFrame(data=dataForExcel)
    #dataFrameForExcel.to_excel(r'C:\Users\Jacob\Documents\2. Programmering\Python\Toiletrulle radius calc\Data.xlsx', index = False)
    positionPlot()
    #print(dataFrameForExcel)
    #radiusPlot()
    #coordsPlotToTime()
    
if a == True:
    a = False
    RadiusRotation(timeValue, stepLength, PreviousRadiusAtPreviousStep, paperThickness, currentIndex, vinkelTotal)