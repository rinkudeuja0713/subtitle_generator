import os
from datetime import timedelta
import whisper
import pyaudio
import pysrt



def audio_transcribe(path,output_filetype ="srt", whisper_model="base"):
    # takes the filename only from the path without extension
    filename = os.path.splitext(os.path.basename(path))[0]
    output_filename = os.path.join("SrtFiles",f"{filename}.{output_filetype}")
    # to check if the output file already exixts or not. if it exists , appends a number to make the filename unique
    if os.path.exists(output_filename):
        i=1
        while os.path.exists(output_filename):
            output_filename= os.path.join("SrtFiles",f"{filename}({i}).{output_filetype}")
            i+=1
    if output_filetype=="srt":
        with open(output_filename, "w" , encoding="utf-8") as SrtFile:
            SrtFile.write("")
        model= whisper.load_model(whisper_model)
        print("Whisper model loaded")
        transcribe= model.transcribe(audio=path)
        segments=transcribe["segments"]

        for segment in segments:
            startTime= str(0)+str(timedelta(seconds=int(segment["start"])))+",000"
            endTime= str(0)+str(timedelta(seconds=int(segment["end"])))+",000"
            text= segment["text"]
            segmentId= segment["id"] +1
            segment= f"{segmentId}\n {startTime} --> {endTime} \n {text[1:] if text[0]=='' else text} \n \n"
            with open(output_filename, "a", encoding="utf-8") as SrtFile:
                SrtFile.write(segment)
        return SrtFile
    
    elif output_filetype =="json":
        with open(output_filename, "w", encoding="utf-8") as jsonFile:
            jsonFile.write('{\n "captions": [\n')
        model = whisper.load_model(whisper_model)
        print("whisper model loaded")
        transcribe= model.transcribe(audio=path)
        segments= transcribe["segments"]

        for segment in segments:
            startTime = timedelta(seconds=int(segment["start"]))
            endTime = timedelta(seconds= int(segment["end"]))
            duration = endTime-startTime
            startTime_str = str(0) + str(startTime) + ",000"
            endTime_str = str(0) + str(endTime) + ",000"
            duration_str = str(0) + str(duration) + ",000"
            text = segment["text"]
            segmentId = segment["id"]+1
            segment = f"{{\t\n\"id\": {segmentId},\n\"start\": \"{startTime_str}\",\n\"end\": \"{endTime_str}\",\n\"duration\": \"{duration_str}\",\n\"text\": \"{text[1:] if text[0] == ' ' else text}\"\n}},\n"
            with open(output_filename, "a", encoding="utf-8") as jsonFile:
                jsonFile.write(segment)
        with open(output_filename, "rb+") as jsonFile:
            jsonFile.seek(-2, os.SEEK_END)
            jsonFile.truncate()
        with open(output_filename, "a", encoding="utf-8") as jsonFile:
            jsonFile.write("\n]\n}")
        return jsonFile
    
    elif output_filetype == "txt":
        with open(output_filename, "w", encoding= "utf-8") as txtFile:
            txtFile.write("")
        model= whisper.load_model(whisper_model)
        print("whisper model loaded")
        transcribe= model.transcribe(audio=path)
        segments = transcribe["segments"]

        for segment in segments:
            timeStart= str(0) + str(timedelta(seconds=int(segment["start"]))) + ",000"
            timeEnd= str(0) + str(timedelta(seconds=int(segment["end"]))) + ",000"
            text= segment["text"]
            segmentId= segment["id"]+1
            segment= f"{segmentId}\n {timeStart} --> {timeEnd} \n {text[1:] if text[0]=='' else text} \n \n "
            with open(output_filename, "a", encoding="utf-8") as txtFile:
                txtFile.write(segment)
        return txtFile
    
output_dir = "SrtFiles"
if not os.path.exists(output_dir):
    os.mkdir("SrtFiles")
path = input("enter the path of the file")
output_filetype = int (input("enter the type of output file (srt is selected by default): \n 1.SRT \n 2.JSON \n 3.TXT \n"))

if output_filetype==1:
    output_filetype="srt"
if output_filetype==2:
    output_filetype="json"
if output_filetype==3:
    output_filetype="txt"

whisper_model = int(input(" select the type of whisper model you want to use (base is selected by default): \n 1.Tiny \n 2.Base \n 3.Small \n 4.Medium \n 5.Large \n"))
if whisper_model ==1:
    whisper_model="tiny"
if whisper_model ==2:
    whisper_model="base"
if whisper_model ==3:
    whisper_model="small"
if whisper_model ==4:
    whisper_model="medium"
if whisper_model ==5:
    whisper_model="large"

srtFilename= audio_transcribe(path, output_filetype, whisper_model)
srtFilename= os.path.basename(srtFilename.name)
print(f"your subtitles are ready. you can find them at {srtFilename}")






    

       
    



        

