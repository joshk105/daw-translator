import math

# this function will take the time in hh:min:sec:frame(or something) and convert it to seconds
def timeToSeconds(time):
    split_time = time.split(":")
    minutes = 0
    hours = 0
    seconds = float(split_time[-1])
    if len(split_time) > 1:
        minutes = int(split_time[-2])
    if len(split_time) > 2:
        hours = int(split_time[-3])

    minutes = minutes + (hours*60)
    seconds = seconds + (minutes*60)
    return seconds

#this function helps you view an object at any time
def displayObject(obj, indent=''):
    for (key, value) in obj.__dict__.items():
        if type(value) is str:
            print(indent + key + ":\t" + value)
        elif type(value) is int or type(value) is float:
            print(indent + key + ":\t" + str(value))
        elif type(value) is bool:
            print(indent + key + ":\t" + str(value))
        elif type(value) is list or type(value) is dict:
            print(indent + key + ":")
            for item in value:
                displayObject(item, indent + "\t")
        else:
            print(indent + key +":")
            displayObject(value, indent + "\t")

#These functions help to convert DB measurements

def powerToDb(num):
    return math.log10(num)*10

def dbToPower(num):
    temp = math.pow(10, num)
    return math.pow(temp, .1)

def powerToAmplitude(num):
    return math.sqrt(num)

def amplitudeToPower(num):
    return num*num

def dbToAmplitude(num):
    return powerToAmplitude(dbToPower(num))

def amplitudeToDb(num):
    return powerToDb(amplitudeToPower(num))
