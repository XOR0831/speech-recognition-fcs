# import dependencies
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import speech_recognition as sr
import datetime

# use the audio file as the audio source for recognition                                       
r = sr.Recognizer()

# file path to original data
path = "./Data/"
# file path to transcribed data
path_split = "./Data_Clean/"
# if directory for transcribed data does not exists
if not os.path.exists(path_split):
    # create directory
    os.makedirs(path_split) 

# for every volume folder in the original data    
for volume in os.listdir(path):
    # if volume directory for transcribed data does not exists
    if not os.path.exists(path_split + volume):
        # create directory
        os.makedirs(path_split + volume)
    # for every folder in volume directory of original data
    for folder in os.listdir(path + volume):
        # initialize/reset unknown count to 0 
        unknown = 0
        # if folder in volume directory of transcribed data does not exists
        if not os.path.exists(path_split + volume + "/" + folder):
            # create directory
            os.makedirs(path_split + volume + "/" + folder)
        # for every file in folder under volume directory of original data
        for file in os.listdir(path + volume + "/" + folder):
            # initialize/reset transcripts container to empty/null
            transcripts = []
            # if folder for the transcribe audio under folder under volume directory does not exists
            if not os.path.exists(path_split + volume + "/" + folder + "/" + file[:-4]):
                #create directory
                os.makedirs(path_split + volume + "/" + folder + "/" + file[:-4])
            # load audio file    
            sound_file = AudioSegment.from_wav(path + volume + "/" + folder + "/" + file)
            print("LOADED: " + str(path + volume + "/" + folder + "/" + file))
            # segments/splits audio on silence and assign segmented/splitted audio to audio chunks
            # some segmented/splitted audio are per word but some are in sentences due to fast speech of speaker 
            print("SEGMENTING")
            audio_chunks = split_on_silence(sound_file, 
                # must be silent for at least a half second to consider it a word
                min_silence_len=25,

                # consider it silent if quieter than -16 dBFS 
                silence_thresh=-35
            )
            print("SEGMENTED")
            # write all segmented audio into new file
            print("WRITING")
            for i, chunk in enumerate(audio_chunks):
                # save every segmented audio to created directory for transcribed data
                out_file = path_split + volume + "/" + folder + "/" + file[:-4] + "/" + "chunk{0}.wav".format(i)    
                print("WRITE:", out_file)
                chunk.export(out_file, format="wav")
                # status for transcript checking
                status = ""
                # open saved audio and send to Google Speech Recognition (Speech to Text) to recognize and label the audio
                with sr.AudioFile(out_file) as source:
                    audio = r.record(source)  # read the entire audio file
                    
                    is_not_transcribe = True
                    while is_not_transcribe:
                        try:
                            # send audio to GSR for recognition 
                            transcribe = r.recognize_google(audio,language="fil-PH") # set language code to Filipino
                            print("(GSR)Transcription: " + transcribe)
                            status = "GSR"
                            is_not_transcribe = False
                        except sr.UnknownValueError:
                            # if GSR cant recognize audio set audio name to UNKNOWN 
                            print("Unknown")
                            unknown += 1
                            status = "UNKNOWN"
                            is_not_transcribe = False
                        except:
                            is_not_transcribe = True
                # renaming audio with the GSR transcript
                print("LABELING")
                writed = True
                # if GSR recognize
                if status == "GSR":
                    # if GSR transcribe exist in transcripts
                    if transcribe in transcripts:
                        # add timestamp
                        transcribe = transcribe + " " + str(datetime.datetime.now().second) + "" + str(datetime.datetime.now().minute) + "" + str(datetime.datetime.now().hour)
                        while writed:
                            print("-"*100)
                            # try to rename audio with GSR transcript if not set to UNKNOWN
                            try:
                                # rename audio with GSR transcribe
                                os.rename(out_file, path_split + volume + "/" + folder + "/" + file[:-4] + "/" + "{0}.wav".format(transcribe))
                                writed = False
                                # add GSR transcribe to transcripts
                                transcripts.append(transcribe)
                            except:
                                # rename audio with UNKNOWN
                                unknown += 1
                                os.rename(out_file, path_split + volume + "/" + folder + "/" + file[:-4] + "/" + "UNKNOWN{0}.wav".format(unknown))
                                writed = False
                    # if not
                    else:
                        while writed:
                            print("+"*100)
                            # try to rename audio with GSR timestamp
                            try:
                                # rename audio with GSR transcribe
                                os.rename(out_file, path_split + volume + "/" + folder + "/" + file[:-4] + "/" + "{0}.wav".format(transcribe))
                                writed = False
                                # add GSR transcribe to transcripts
                                transcripts.append(transcribe)
                            except:
                                # rename audio with UNKNOWN
                                unknown += 1
                                os.rename(out_file, path_split + volume + "/" + folder + "/" + file[:-4] + "/" + "UNKNOWN{0}.wav".format(unknown))
                                writed = False
                # if not recognized
                else:
                    while writed:
                        print("="*100)
                        # try to rename audio until renamed
                        try:
                            # rename audio with UNKNOWN
                            os.rename(out_file, path_split + volume + "/" + folder + "/" + file[:-4] + "/" + "UNKNOWN{0}.wav".format(unknown))
                            writed = False
                        except:
                            writed = True
                print("LABELED")
