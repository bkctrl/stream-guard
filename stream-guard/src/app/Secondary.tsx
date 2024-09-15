"use client"
import axios from 'axios';
import { useRef, useState, useEffect } from 'react';
import { Button } from '@mui/material';
import Webcam from 'react-webcam';
import AOS from 'aos';
const Secondary: React.FC = () => {
  const [transcription, setTranscription] = useState<string[]>([]);
  const transcriptionRef = useRef(transcription);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const webcamRef = useRef<Webcam>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const [recording, setRecording] = useState(false);
  const [timer, setTimer] = useState(0);
  const [censored, setcensored] = useState(0);
  const [intervalId, setIntervalId] = useState<NodeJS.Timeout | null>(null);
  const speakText = (text: string | undefined) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1;
      utterance.pitch = 1;
      window.speechSynthesis.speak(utterance);
    }
  };
  const fetchTranscription = async () => {
    try {
      const response = await axios.get('http://localhost:5000/transcription');
      const numCensoredResponse = await axios.get('http://localhost:5000/num-censored');
      const receivedNumCensored = numCensoredResponse.data.num_censored;
      const receivedTranscription: string[] = response.data.message;
      if (receivedTranscription.length > transcriptionRef.current.length) {
        const newTranscription = receivedTranscription.slice(transcriptionRef.current.length);
        setTranscription(receivedTranscription);
        setcensored(receivedNumCensored);
        transcriptionRef.current.length = receivedTranscription.length;
        speakText(newTranscription.join(' '));
      }
    } catch (error) {
      console.error('Error fetching transcription:', error);
    }
  };
  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };
  const startRecording = () => {
    const interval = setInterval(fetchTranscription, 1000);
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
    return () => clearInterval(interval);
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
  useEffect(() => {
    AOS.init();
    // const interval = setInterval(fetchTranscription, 1000);
    // return () => clearInterval(interval);
  }, []);
  return (
    <section
      id="demo-webcam"
      className="h-svh bg-slate-100 justify-center" style={{maxHeight: "91vh", width:"100%"}}
    >
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css" />
      <div>
        <h2 className="text-5xl mt-6 ml-12 font-semibold" style={{paddingTop: "3vh", textAlign: "center"}}>
          See It in Action
        </h2>
        <div data-aos="zoom-in" aos-duration="1500" style={{maxHeight: "93vh",
          paddingTop: "5vh", alignItems: "center", justifyContent: "center", display: "flex"}}>
          <div className="rounded-lg border bg-card p-4 shadow-sm transition-all duration-300 ease-in-out hover:scale-[1.02] hover:shadow-lg hover:shadow-[#8E5CCF]/50" style={{backgroundColor: "white", width: "80vw", height:"70vh"}}>
            <div style={{display: "flex", justifyContent: "space-between", alignItems: "center"}}>
              <Webcam audio={false} ref={webcamRef} className='rounded-md object-cover' style={{width: "40vw"}}/>
              <div className="w-1/3 p-4 h-auto m-4 ml-12 rounded-lg bg-white border-2 border-slate-500" style={{width: "35vw", height:"48vh"}}>
                <p>{transcription.join(' ')} </p>
              </div>
            </div>
            <div className="mt-4">
              <h3 className="text-lg font-semibold">Real-Time Video</h3>
              <p className="mt-2 text-muted-foreground">
              </p>
              <div className="mt-4 flex" style={{gap: "1rem"}}>
              <div className="flex flex-row border justify-center items-center rounded-lg"
                style={{alignItems: "center", justifyContent: "center", display: "flex", gap: "10rem",
                  height: "7rem", width: "90%"
                  }}>
                <div className="flex flex-col items-center">
                  <div id="time" className="text-6xl h-1/2">
                    {formatTime(timer)}
                  </div>
                  <p className="text-sm w-fit" style={{alignItems: "center"}}>
                    <em>Duration</em>
                  </p>
                </div>
                <div className="flex flex-col items-center">
                  <div id="count" className="text-6xl h-1/2">
                    {censored}
                  </div>
                  <div className="text-sm w-fit">
                    <em>Profanities filtered</em>
                  </div>
                </div>
              </div>
              {!recording ? (
                <Button className="rounded-2xl bg-green-500 text-white p-2 z-50 cursor-pointer" onClick={startRecording}  style={{display: "flex",
                  flexDirection: "column", alignItems: "center"}}>
                  <svg xmlns="http://www.w3.org/2000/svg" width="2.5em" height="2.5em" viewBox="0 0 12 12">
                    <path fill="currentColor" d="M4.496 1.994A1 1 0 0 0 3 2.862v6.277a1 1 0 0 0 1.496.868l5.492-3.139a1 1 0 0 0 0-1.736z" />
                  </svg>
                  <p style={{fontSize: "0.8rem", paddingTop: "0.2rem"}}>Start Record</p>
                </Button>
              ) : (
                <Button className="rounded-2xl bg-red-500 text-white p-2 z-50 cursor-pointer" onClick={stopRecording}  style={{display: "flex",
                  flexDirection: "column", alignItems: "center"}}>
                  <svg xmlns="http://www.w3.org/2000/svg" width="2.5em" height="2.5em" viewBox="0 0 12 12">
                    <path fill="currentColor" d="M3 2a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1zm5 0a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h1a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1z" />
                  </svg>
                  <p style={{fontSize: "0.8rem", paddingTop: "0.2rem"}}>Stop Record</p>
                </Button>
              )}
              </div>
            </div>
          </div>
          </div>
        </div>
    </section>
  )
}
export default Secondary;