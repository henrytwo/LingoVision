from playsound import playsound

def startSound():
    playsound("StartSound.mp3")

def errorSound():
    playsound("ErrorSound.mp3")

if __name__ == '__main__':
    startSound()

    print(7)
    errorSound()
