"use client"

import axios from 'axios';
import {useState, useEffect, useRef} from 'react';

export default function Banner() {
  const [transcription, setTranscription] = useState<string[]>([]);
  const transcriptionRef = useRef(transcription);

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
      const response = await axios.get('http://127.0.0.1:5001/transcription');
      const receivedTranscription: string[] = response.data.transcription;
      if (receivedTranscription.length > transcriptionRef.current.length) {
        const newTranscription = receivedTranscription.slice(transcriptionRef.current.length);
        setTranscription(receivedTranscription); 
        transcriptionRef.current.length = receivedTranscription.length;
        speakText(newTranscription.join(' '));
      }
    } catch (error) {
      console.error('Error fetching transcription:', error);
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchTranscription, 1000); 
    return () => clearInterval(interval); 
  }, []);  


  return (
    <div className="relative w-full h-svh diagonal-split">
      <div className="absolute z-10"></div>
      <div className="flex w-full h-96">
      <div className="h-full flex justify-center items-center w-2/3">
        <span className="z-20 mx-10 mt-24 font-medium text-7xl max-w-xl">
          Remove unwanted content from your audio <br /> <strong>in real time.</strong>
          <br /><br />{transcription.join(' ')} 
        </span>
      </div>
      <div className="h-full flex justify-center w-1/3">
      </div>
    </div>
  </div>
  );
}