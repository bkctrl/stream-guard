"use client"
import { useRef, useState, useEffect } from 'react';
import Webcam from 'react-webcam';

const Secondary: React.FC = () => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const webcamRef = useRef<Webcam>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const [recording, setRecording] = useState(false);
  const [timer, setTimer] = useState(0); // Timer in seconds
  const [intervalId, setIntervalId] = useState<NodeJS.Timeout | null>(null);

  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };


  const startRecording = () => {
    setRecording(true);
    const stream = webcamRef.current?.video?.srcObject as MediaStream;
    mediaRecorderRef.current = new MediaRecorder(stream, {
      mimeType: 'video/webm',
    });

    const chunks: Blob[] = [];
    mediaRecorderRef.current.ondataavailable = (event) => {
      chunks.push(event.data);
    };

    mediaRecorderRef.current.onstop = () => {
      const blob = new Blob(chunks, { type: 'video/mp4' });
      const videoURL = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = videoURL;
      a.download = 'recorded-video.mp4';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(videoURL);

      setTimer(0);
      if (intervalId) {
        clearInterval(intervalId);
        setIntervalId(null);
      }
    };

    mediaRecorderRef.current.start();

    const id = setInterval(() => {
      setTimer((prevTimer) => prevTimer + 1);
    }, 1000);
    setIntervalId(id);
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setRecording(false);
    setTimer(0);
    if (intervalId) {
      clearInterval(intervalId);
      setIntervalId(null);
    }
  };

  return (
    <div 
      className="w-full h-svh bg-slate-100 flex justify-center"
    >
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" />
      <div className="w-3/4 shadow-2xl h95 bg-slate-300 flex flex-col pb-12 rounded-xl">
        <div className="w-full h-24 bg-slate-300 rounded-xl">
          <div>
            <h2 className="text-6xl mt-6 ml-12" >
              Try the demo!
            </h2>
          </div>
        </div>

        <div className="w-full h-full flex">
          <div className="w-2/3 h-full">
            <div className="mt-4 ml-4 pt-0.5 h-full w-full gbg1">
              <div className="mt-4 ml-4 h-full w-full">
                <div className="h-3/4 border border-slate-400 bg-cyan-50" 
                  >
                  <Webcam audio={true} ref={webcamRef} />
                </div>
                <div className="flex flex-col h-1/4 border  bg-white">
                  <div 
                    className="w-full h-1/3 border-b-2 flex"
                  >
                    <div className="w-1/3 h-full">
                    
                    </div>
                    <div className="w-1/3 h-full flex justify-center items-center">
                      <button
                        className="size-12 rounded-3xl bg-white border border-black"
                        id="start"
                      >
                        mic
                      </button>
                    </div>
                    <div className="w-1/3 h-full">
                    </div>
                  </div>

                  <div className="flex flex-col h-1/4 border border-slate-400 bg-white">
                  <div className="w-full h-1/3 border-b-2 flex justify-center items-center">
                    {!recording ? (
                      <button className="rounded-3xl bg-green-500 text-white p-2 z-50 cursor-pointer" onClick={startRecording}>
                        Start Record
                      </button>
                    ) : (
                      <button className="rounded-3xl bg-red-500 text-white p-2 z-50 cursor-pointer" onClick={stopRecording}>
                        Stop Record
                      </button>
                    )}
                  </div>
                  </div>
                    
                  <div className="flex w-full h-full">
                    <div className="flex flex-col w-2/3 border justify-center items-center">
                      <span 
                          id="time"
                          className="text-6xl h-1/2" 
                          // ref={timerRef}
                        >
                          {formatTime(timer)}
                        </span>
                        <span className="text-sm w-fit">
                          <em>Duration</em>
                        </span>
                    </div>
                    <div className="flex w-1/3 flex-col justify-center items-center">
                      <span 
                        id="count"
                        className="text-6xl h-1/2" 
                      >
                        0
                      </span>
                      <span className="text-sm w-fit">
                        <em>Profanities filtered</em>
                      </span>
                    </div>

                  </div>

                </div>
              </div>
            </div>
          </div>

          <div className="w-1/3 p-4 h-auto m-4 ml-12 rounded-lg bg-white border-2 border-slate-500">
            <p>transcript goes here</p>
          </div>



        </div>


      </div>
    </div>
  );
}

export default Secondary;
