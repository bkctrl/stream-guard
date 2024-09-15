"use client"

import axios from 'axios';
import {useState, useEffect, useRef} from 'react';
import AOS from 'aos';

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
    AOS.init();
    const interval = setInterval(fetchTranscription, 1000); 
    return () => clearInterval(interval); 
  }, []);  


  return (
    <div className="relative w-full h-svh diagonal-split flex flex-col">
      <div className="flex w-full h-96">
        <div className="h-full flex items-center w-2/3">
          <span className="z-20 mx-24 mt-32 font-medium text-7xl max-w-4xl" data-aos="fade-right" data-aos-duration="1500" data-aos-mirror="true">
            Remove unwanted content from your audio <br /> <strong>in real time.</strong>
            {/* <br /><br />{transcription.join(' ')}  */}
          </span>

        </div>

        <div className="h-full flex justify-center w-1/3">
        </div>
      </div>
      <div
        className='flex items-center h-96'
      >
        <div
          className=''
        >

        </div>
        <span 
          data-aos="fade-right" data-aos-duration="1500" data-aos-delay="750" data-aos-mirror="true"
            className="mt-8 ml-40 w-1/3 text-xl"
          >
            <strong>Streamers</strong> - We protect your income stream by staying up to date on TOS violations, so you don't have to. <br /> <br />
            <strong>Everyone else</strong> - Enjoy your favourite streaming content without worrying about unwanted content. 
          </span>
      </div>
    </div>
  );
}