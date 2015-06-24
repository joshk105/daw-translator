from xml.dom import minidom
from object_classes import *
from helpers import timeToSeconds


class HindenburgInt(object):

    def __init__(self, project_file, version="Hindenburg Journalist 1.26.1936", version_num="1.26.1936"):
        self.projectFile = project_file
        self.version = version
        self.version_num = version_num

    def get_session_name(self):
        for i in self.projectFile.split("/"):
            name = i

        name = name.split(".")
        return name[0]

    def read(self):
        projectXML = minidom.parse(self.projectFile)
        projectObj = Session(self.get_session_name())
        projectXML = projectXML.getElementsByTagName("Session")
        project = projectXML[0]
        projectObj.samplerate = project.getAttribute('Samplerate')
        fileSourceInfo = project.getElementsByTagName("AudioPool")[0]
        fileSourcePath = fileSourceInfo.getAttribute("Location") + "/" + fileSourceInfo.getAttribute("Path")
        projectObj.audio_folder = fileSourceInfo.getAttribute('Path')
        projectObj.folder_path = fileSourceInfo.getAttribute('Location')

        audioFiles = project.getElementsByTagName("File")
        for file in audioFiles:
            projectObj.addFile(fileSourcePath + "/" + file.getAttribute("Name"), int(file.getAttribute('Id')))

        markers = project.getElementsByTagName("Marker")
        for marker in markers:
            projectObj.addMarker(marker.getAttribute('Id'), marker.getAttribute('Name'), float(marker.getAttribute('Time')))

        tracks = project.getElementsByTagName("Track")
        for track in tracks:
            current_track = projectObj.addTrack(track.getAttribute('Name'))

            try:
                current_track.pan = self.interpretPan(track.getAttribute('Pan'))
            except:
                current_track.pan = 0

            try:
                current_track.volume = track.getAttribute('Volume')
            except:
                current_track.volume = 0

            try:
                if track.getAttribute('Solo') == "1":
                    current_track.solo = True
            except:
                current_track.solo = False

            try:
                if track.getAttribute('Mute') == "1":
                    current_track.mute = False
            except:
                current_track.mute = False

            try:
                if track.getAttribute('Rec') == "1":
                    current_track.rec = True
            except:
                current_track.rec = False


            trackItems = track.getElementsByTagName("Region")
            for item in trackItems:
                new_item = current_track.addItem(projectObj.getFileByID(int(item.getAttribute('Ref'))))
                try:
                    start = float(item.getAttribute('Start'))
                except:
                    start = 0
                new_item.startTime = start

                try:
                    startAt = float(item.getAttribute('Offset'))
                except:
                    startAt = 0
                new_item.startAt = startAt

                length = timeToSeconds(item.getAttribute('Length'))
                new_item.length = length

                try:
                    gain = float(item.getAttribute('Gain'))
                except:
                    gain = 0
                new_item.gain = gain

                new_item.name = item.getAttribute('Name')

                fades = item.getElementsByTagName('Fade')
                if fades:
                    autoEnv = current_track.getEnvelope('Volume')
                    if autoEnv == "Envelope Not Found":
                        autoEnv = current_track.addEnvelope('Volume')

                    firstFade = True

                    for fade in fades:
                        startTime = new_item.startTime + float(fade.getAttribute('Start'))
                        if firstFade:
                            startValue = new_item.gain
                        else:
                            startValue = autoEnv.points[-1].value
                            firstFade = False
                        endTime = startTime + float(fade.getAttribute('Length'))
                        try:
                            endValue = float(fade.getAttribute('Gain'))
                        except:
                            endValue = 0

                        autoEnv.addPoint(startTime, startValue)
                        autoEnv.addPoint(endTime, endValue)




            plugins = track.getElementsByTagName("Plugin")
            for plugin in plugins:
                if plugin.getAttribute('Name') == 'Compressor':
                    pluginType = "Native"
                else:
                    pluginType = "Plugin"
                new_plugin = current_track.addFX(plugin.getAttribute('Name'), pluginType, int(plugin.getAttribute('Id')))

                if pluginType == "Native":
                    if plugin.getAttribute('Name') == 'Compressor':
                        new_plugin.addProperty('UID', plugin.getAttribute('UID'))
                        new_plugin.addProperty('Comp', plugin.getAttribute('Comp'))

        return projectObj

    #Notes: Need to develop the section that reads the plugins...include support for external plugins, and the native EQ plugin

    def write(self, destinationFile):
        print('This function still needs to be written')


    def interpretPan(self, amount):
        num = -float(amount)
        num = num*90
        return num



