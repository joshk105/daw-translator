from object_classes import *
from hindenburg import HindenburgInt
from helpers import displayObject
from reaper import ReaperInt
hindyFile = '/Users/jklos/Desktop/Session Transfer/Hindenburg.nhsx'
reaperFile = '/Users/jklos/Desktop/Session Transfer/Reaper/Reaper.RPP'

#The following code is creating a fake session file for test purposes...
def create_session_test():

    session = Session("Test Session")

    session.addTrack("First Track", 1)
    session.addTrack("Second Track", 2)
    file = session.addFile("/Users/jklos/Desktop/file.mp3")
    print(file.fileType())

    track_test = session.getTrack(1)
    print(track_test.name)
    track_item = track_test.addItem(file)
    print(track_item.source_file.fpath)
    track_test = session.getTrack(2)
    print(track_test.name)
    print(session.name)

    return session

#test_session = create_session_test()

#printProperties(test_session)

#interpreter = HindenburgInt(hindyFile)
#session = interpreter.read()

#displayObject(session)

interpreter = ReaperInt(reaperFile)
session = interpreter.read()

displayObject(session)
