class Session(object):

    def __init__(self, name):
        self.name = name
        self.tracks = []
        self.files = []
        self.markers = []
        self.samplerate = 0
        self.audio_folder = ''
        self.folder_path = ''


    def addTrack(self, name, number=-1):
        if number == -1:
            number = self.getTrackNum()
        new_track = Track(name, number)
        self.tracks.append(new_track)
        return self.tracks[-1]

    def getTrack(self, track_number):
        for track in self.tracks:
            if track.track_num == track_number:
                return track
        return "Track Not Found"

    def getTrackNum(self):
        track_num = 1
        for track in self.tracks:
            if track_num <= track.track_num:
                track_num = track.track_num + 1
        return track_num

    def addFile(self, fpath, itemID=-1):
        if itemID == -1:
            itemID = self.getFileID()
        new_file = AudioFile(fpath, itemID)
        self.files.append(new_file)
        return self.getFile(fpath)

    def getFile(self, fpath):
        for file in self.files:
            if file.fpath == fpath:
                return file
        return "File Not Found"

    def getFileByID(self, itemID):
        for file in self.files:
            if file.itemID == itemID:
                return file
        return "File Not Found"

    def getFileID(self):
        itemID = 0
        for file in self.files:
            if itemID <= file.itemID:
                itemID = file.itemID + 1
        return itemID

    def addMarker(self, num, name, time):
        new_marker = Marker(num, name, time)
        self.markers.append(new_marker)
        return self.getMarker(num)

    def getMarker(self, num):
        for marker in self.markers:
            if marker.num == num:
                return marker
        return "Marker Not Found"


class Track(object):

    def __init__(self, name, number):
        self.name = name
        self.track_num = number
        self.items = []
        self.effects = []
        self.envelopes = []
        self.solo = False
        self.mute = False
        self.rec = False
        self.pan = 0
        self.volume = 0

    def addItem(self, audio_file):
        itemID = self.createItemID()
        new_item = TrackItem(audio_file, itemID)
        self.items.append(new_item)
        return self.getItem(itemID)

    def getItem(self, itemID):
        for item in self.items:
            if item.itemID == itemID:
                return item
        return "Track Item Not Found"

    def createItemID(self):
        itemID = 0
        for item in self.items:
            if itemID < item.itemID:
                itemID = item.itemID + 1
        return itemID

    def addFX(self, name, type, itemID):
        new_fx = FX(name, type, itemID)
        self.effects.append(new_fx)
        return self.effects[-1]

    def addEnvelope(self, envType):
        new_envelope = AutomationEnvelope(envType)
        self.envelopes.append(new_envelope)
        return self.envelopes[-1]

    def getEnvelope(self, envType):
        for envelope in self.envelopes:
            if envelope.type == envType:
                return envelope
        return "Envelope Not Found"


class TrackItem(object):

    def __init__(self, source_file, itemID):
        self.source_file = source_file
        self.effects = []
        self.itemID = itemID
        self.gain = 0
        self.startTime = 0
        self.startAt = 0
        self.length = 0
        if source_file == "TEMP":
            self.name = "TEMP"
        else:
            self.name = self.source_file.fpath.split("/")[-1]

    def applyFX(self, name, type, itemID):
        new_fx = FX(name, type)
        self.effects.append(new_fx)
        return self.effects[-1]


class AudioFile(object):

    def __init__(self, fpath, itemID):
        self.fpath = fpath
        self.itemID = itemID



    def fileType(self):
        for i in self.fpath.split("."):
            ext = i
        if ext == "mp3":
            return "MP3"
        elif ext == "wav":
            return "WAV"
        elif ext == "ogg":
            return "OGG"
        else:
            return "UNDEFINED"


class FX(object):

    def __init__(self, name, type, itemID):
        self.name = name
        self.type = type
        self.itemID = itemID
        self.values = []


    def addProperty(self, name, value):
        new_prop = FXprop(name, value)
        self.values.append(new_prop)
        return self.values[-1]


class Marker(object):

    def __init__(self, num, name, time):
        self.num = num
        self.name = name
        self.time = time


class FXprop(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value


class AutomationEnvelope(object):

    def __init__(self, envType):
        self.type = envType
        self.points = []

    def addPoint(self, time, value):
        new_point = AutomationPoint(time, value)
        self.points.append(new_point)
        return self.points[-1]


class AutomationPoint(object):

    def __init__(self, time, value):
        self.time = time
        self.value = value