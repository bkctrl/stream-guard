"use client"
import React, { useRef, useEffect } from 'react';

const WebcamComponent: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const getWebcamStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing the webcam: ", err);
      }
    };

    getWebcamStream();
  }, []);

  return (
    <div>
      <h1>Webcam Without Certificates</h1>
      <video ref={videoRef} autoPlay playsInline style={{ width: '100%', height: 'auto' }} />
    </div>
  );
};

export default WebcamComponent;