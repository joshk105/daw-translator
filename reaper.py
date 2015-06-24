from object_classes import *
from helpers import *


class ReaperInt(object):

    def __init__(self, project_file, version="4.76/OSX64", version_num="4.76"):
        self.projectFile = project_file
        self.version = version
        self.versionNum = version_num

    def get_session_name(self):
        for i in self.projectFile.split("/"):
            name = i

        name = name.split(".")
        return name[0]

    def read(self):
        projectFile = open(self.projectFile, 'r')
        tags = []
        session = Session(self.get_session_name)
        for line in projectFile:
            current = self.readLine(line)
            if current[0] == "tag_open":
                tags.append(current[1])
                if current[1] == 'REAPER_PROJECT':
                    last = "tag_open"
                elif current[1] == "TRACK":
                    session.addTrack("TEMP")
                elif current[1] == "ITEM":
                    session.tracks[-1].addItem("TEMP")
                elif current[1] == "SOURCE":
                    session.addFile("TEMP")
                elif current[1] == "VOLENV2":
                    session.tracks[-1].addEnvelope('Volume')
                elif current[1] == "PANENV2":
                    session.tracks[-1].addEnvelope('Pan')
                else:
                    pass
                    #print ("Tag " + current[1] + " does not currently correspond to a property that exists")
            elif current[0] == "tag_close":
                tags.pop()
            elif current[0] == "attribute":
                if tags[-1] == 'REAPER_PROJECT':
                    if current[1] == "SAMPLERATE":
                        session.samplerate = int(current[2][0])
                if tags[-1] == "TRACK":
                    current_track = session.tracks[-1]
                    if current[1] == "NAME":
                        current_track.name = self.joinAndStrip(current[2])
                    if current[1] == "MUTESOLO":
                        if current[2][0] != "0":
                            current_track.mute = True
                        if current[2][1] != "0":
                            current_track.solo = True
                    if current[1] == "REC":
                        if current[2][0] != "0":
                            current_track.rec = True
                    if current[1] == "VOLPAN":
                        current_track.pan = float(current[2][1]) * 90
                        current_track.volume = amplitudeToDb(float(current[2][0]))
                if tags[-1] == "ITEM":
                    last_item = session.tracks[-1].items[-1]
                    if current[1] == "POSITION":
                        last_item.startTime = float(current[2][0])
                    if current[1] == "SOFFS":
                        last_item.startAt = float(current[2][0])
                    if current[1] == "NAME":
                        last_item.name = self.joinAndStrip(current[2])
                if tags[-1] == 'VOLENV2':
                    envelope = session.tracks[-1].envelopes[-1]
                    if current[1] == 'PT':
                        time = current[2][0]
                        value = amplitudeToDb(float(current[2][1]))
                        envelope.addPoint(time, value)
                if tags[-1] == 'PANENV2':
                    envelope = session.tracks[-1].envelopes[-1]
                    if current[1] == 'PT':
                        time = current[2][0]
                        value = float(current[2][1])*90
                        envelope.addPoint(time, value)
                if tags[-1] == "SOURCE":
                    current_file = session.files[-1]
                    if current[1] == "FILE":
                        current_file.fpath = self.joinAndStrip(current[2])
                        current_item = session.tracks[-1].items[-1]
                        current_item.source_file = current_file


            else:
                print("Unable to process " + current)


        return session



    def joinAndStrip(self, array):
        new_string = " ".join(array)
        if new_string[0] == '"':
            new_string = new_string[1:]
        if new_string[-1] == '"':
            new_string = new_string[:-1]
        if new_string[-3] == '"':
            new_string = new_string[:-3]
        return new_string

    def readLine(self, line):
        # returns what type it is (open tag, close tag, or attribute), what the text_value is, an array of values
        content = line.lstrip()
        content = content.rstrip()
        if content == ">":
            return ["tag_close", None, []]
        content = content.split(" ")
        if content[0][0] == "<":
            return ["tag_open", content[0][1:], content[1:]]
        else:
            return ["attribute", content[0], content[1:]]

    def write(self, destinationFile):
        pass