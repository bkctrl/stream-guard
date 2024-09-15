"use client"
import {useEffect} from 'react';
import AOS from 'aos';
import ScrollDownButton from './ScrollDownButton';

export default function Banner() {
  useEffect(() => {
    AOS.init();
  })
  return (
    <div>
      <style>
        {`html {
            scroll-behavior: smooth;
          }`}
      </style>
      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 mb-4">
        <a href="#demo-webcam"><ScrollDownButton /></a>
      </div>
      <img src="htn-logo.png" alt="Decoration 1" 
        data-aos="fade-up-right" data-aos-duration="1500" data-aos-mirror="true"
        style={{
          position: "absolute", 
          top: "53rem", 
          left: "6rem", 
          width: '10rem', 
          height: '10rem', 
          zIndex: 100
        }} 
      />
      <img src="htn-logo.png" alt="Decoration 1" 
        data-aos="fade-up-right" data-aos-duration="1500" data-aos-mirror="true"
        style={{
          position: "absolute", 
          top: "49rem", 
          left: "14rem", 
          width: '5rem', 
          height: '5rem', 
          zIndex: 100
        }} 
      />
      <img src="stars.png" alt="Decoration 1" 
        data-aos="fade-down-left" data-aos-duration="1500" data-aos-mirror="true"
        style={{
          position: "absolute", 
          top: "4rem", 
          left: "82rem", 
          width: '22rem', 
          height: '20rem', 
          zIndex: 100
        }} 
      />
    <div className="relative w-full h-vh diagonal-split" style={{zIndex: 1, height: "100vh"}}>
      <a href="#" className="flex" style={{zIndex: 1000 }}>
        <div className="text-xl font-bold flex-shrink-0"
        style={{paddingLeft: "2.5rem", paddingTop: "0.5rem", fontSize: "1.5rem"}}>&nbsp; &nbsp; <img src="sg-logo.png" style={{width: "14rem", height: "2rem"}}
        data-aos="fade-right" data-aos-duration="1500" data-aos-mirror="true"/></div>
      </a>
      <div className="absolute z-10"></div>
      <div className="flex w-full h-96">
        
      <div className="h-full flex justify-center items-center w-2/3" style={{paddingTop: "20rem"}}>
        <span className="z-20 mx-10 mt-24 font-medium text-7xl max-w-xl" data-aos="fade-right" data-aos-duration="1500" data-aos-mirror="true">
          Remove explicit content from your audio — <br /> <strong>in real time.</strong>
          <br /><br />
        </span>
      </div>
      <div className="h-full flex justify-center w-1/3">
      <div style={{paddingTop: "35rem", paddingRight: "5rem", position: "relative"}} data-aos="fade-left" data-aos-duration="1500" data-aos-mirror="true">
        <iframe 
          width="560" 
          height="315" 
          src="https://www.youtube.com/embed/NxFkEj7KPC0" 
          title="YouTube video player" 
          frameBorder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          style={{backgroundColor: "#f0f0f0", boxShadow: "0px 10px 20px rgba(0, 0, 0, 0.4)", zIndex: 1, position: "relative"}}
          allowFullScreen
        ></iframe>
      </div>
      </div>
    </div> 
  </div>
  </div>
  );
}
