from pyaudio import paInt16, PyAudio
from threading import Event, Thread
from uuid import uuid1
import wave


CHUNK = 1024
FORMAT = paInt16
CHANNELS = 2
RATE = 44100


class Recorder(Thread):
    '''
    A thread which records audio as its activity.

    self.p: pyaudio.PyAudio :: a PyAudio instance
    self.frames: A list of audio frames

    self._stop: threading.Event :: when set the thread will stop recording
    self._stream :: a PyAudio stream which to record from
    '''
    def __init__(self, flag):
        Thread.__init__(self)
        '''
        flag: a flag when set will stop the recording
        '''
        self._stopFlag = flag
        self.frames = []

        self.p = PyAudio()
        self._stream = self.p.open(format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    frames_per_buffer=CHUNK)

    def run(self):
        print("* recording")
        while not self._stopFlag.is_set():
            data = self._stream.read(CHUNK)
            self.frames.append(data)
        self._stream.stop_stream()
        self._stream.close()
        self.p.terminate()
        print("* done recording")


if __name__ == '__main__':
    stopFlag = Event()
    while True:
        try:
            stopFlag.clear()
            input("Press enter to start recording")

            recorder = Recorder(stopFlag)
            recorder.start()

            input("Press enter to stop recording")
            stopFlag.set()
            recorder.join()

            print("Saving...")
            filename = f'{uuid1()}.wav'
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(recorder.p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(recorder.frames))
            wf.close()
            print("Saved")
        except KeyboardInterrupt:
            print("Exitting...")
            break


