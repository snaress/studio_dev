import math


def getDistance(p1, p2):
    """
    Get distance between two 3d points

    :param p1: First point coord
    :type p1: tuple
    :param p2: Second point coord
    :type p2: tuple
    :return: Distance between p1 and p2
    :rtype: float
    """
    dist = math.sqrt(math.pow((p1[0]-p2[0]), 2) +
                     math.pow((p1[1]-p2[1]), 2) +
                     math.pow((p1[2]-p2[2]), 2))
    return dist

def coordOp(p1, p2, operation):
    """
    Coord operations

    :param p1: First point coord
    :type p1: tuple
    :param p2: Second point coord
    :type p2: tuple
    :param operation: 'plus', 'minus', 'mult', 'divide' or 'average'
    :type operation: str
    :return: New coords
    :rtype: tuple
    """
    #--- Check Operator ---#
    operations = ('plus', 'minus', 'mult', 'divide', 'average')
    if not operation in operations:
        raise NotImplementedError("The operation must be in %s" % ", ".join(operations))
    #--- Calculate New Coord ---#
    newCoord = []
    if operation == 'plus':
        for x, y in zip(p1, p2):
            newCoord.append(x + y)
    elif operation == 'minus':
        for x, y in zip(p1, p2):
            newCoord.append(x - y)
    elif operation == 'mult':
        for x, y in zip(p1, p2):
            newCoord.append(x * y)
    elif operation == 'divide':
        for x, y in zip(p1, p2):
            newCoord.append(x / y)
    elif operation == 'average':
        for x, y in zip(p1, p2):
            newCoord.append((x + y) / 2)
    #--- Result ---#
    result = (newCoord[0], newCoord[1], newCoord[2])
    return result

def linear(minVal, maxVal, newMin, newMax, value):
    """
    Linear step from range (minVal, maxVal) to new range (newMin, newMax)

    :param minVal: Range min value
    :type minVal: float
    :param maxVal: Range max value
    :type maxVal: float
    :param newMin: New range min value
    :type newMin: float
    :param newMax: New range max value
    :type newMax: float
    :param value: Range value to convert
    :type value: float
    :return: Linear value
    :rtype: float
    """
    coef = ((float(value) - float(minVal)) * 100) / (float(maxVal) - float(minVal))
    newVal = float(newMin) + ((coef * (float(newMax) - float(newMin))) / 100)
    return newVal
