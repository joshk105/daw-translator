from object_classes import *
from hindenburg import HindenburgInt
from helpers import displayObject
from reaper import ReaperInt

interpreter = ReaperInt(reaperFile)
session = interpreter.read()

displayObject(session)
