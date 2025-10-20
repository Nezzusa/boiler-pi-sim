import math

def waterLevelChangeOverTime():
    surfaceArea = 2.5
    outflowConstant = 0.035
    inflowIntensity = 0.05
    testPeriod = 0.1
    simulationTime = 1800
    level = [0.0]
    timestamp = [0.0]
    minLevel = 0.0
    maxLevel = 5.0

    for i in range(int(simulationTime/testPeriod)):
        timestamp.append(timestamp[-1] + testPeriod)
        x = (inflowIntensity - outflowConstant * (math.sqrt(level[-1]))) * testPeriod / surfaceArea + level[-1]
        level.append(min(maxLevel, max(minLevel,x)))

    return timestamp, level

timestamp, level = waterLevelChangeOverTime()
print(level)