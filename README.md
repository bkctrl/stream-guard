<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/bkctrl/biquadris">
    <img src="https://github.com/user-attachments/assets/fb30e9e2-190f-4956-b198-ff73249fe4ad" alt="Logo" height="80">
  </a>

<h3 align="center">StreamGuard</h3>
  <p align="center">Because Every Word Counts<br/><br/>
    <a href="DEMO LINK, TO BE UPDATED AFTER WE'RE DONE"><strong>View Demo »</strong></a><br /><br />
    <a href="https://devpost.com/software/streamguard"><img src="https://img.shields.io/badge/Devpost-003E54?style=for-the-badge&logo=Devpost&logoColor=white"></a>
    <br />
    <br />
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Have you struggled with tounge slips?  
Done either by your favourite streamer or perhaps even yourself?  
Happens occasionally but when it does, it calls for disaster for the creator. One wrong word could mean losing portions of your audience, or worse, a long developed career.  
This is where StreamGuard come to save the day...  

StreamGuard is an innovative content moderation tool designed to enhance the live streaming experience by filtering out unwanted language in **real-time**. Whether you’re a Twitch streamer aiming to maintain a family-friendly channel or a broadcaster ensuring professional standards during live interviews, StreamGuard has you covered.

### Why StreamGuard?
In the fast-paced world of live streaming, maintaining a clean and professional broadcast can be challenging. StreamGuard provides a reliable solution to prevent unintended slip-ups from reaching your audience, protecting your brand and ensuring a positive viewing experience for all.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How we built it
We built StreamGuard's frontend using Next.js and Tailwind CSS for smooth transitions, creating a visually appealing user interface, all deployed on Vercel for easy updates. The backend, powered by Flask, handles HTTP requests, while PyDub and PyAudio manage audio processing. We leveraged PyTorch for machine learning alongside with OpenAI’s Whisper providing real-time speech recognition for accurate transcription and filtering. Real-time communication is facilitated by Socket, ensuring minimal latency. Finally, our final goal is for StreamGuard to be deployed on Google Cloud Platform, where it can thrive in larger clusters, taking advantage of the larger AI models via more resources. 

### How to Real-Time
As you might imagine, with one big difficult problem, you must first break it down into many manageable chunks. So that is exactly what we did! Our software breaks down the live feed into 1s to sub 1s segments which are processed individually then put together to create the final transcript you see. The system is intelligent and hence the chunk cuts happen when you finish the word you are speaking, i.e. the instant before you say the next word in your sentence. This opens many gateways and possibilities for us, concurrent-programming/parallel-computing, ability for APIs and faster response times are a few to mention. But for this project we are using concurrent programming at small scale to get the job done.
  
### Built With
<a href=""><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"></a>
<a href=""><img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white"></a>
<a href=""><img src="https://img.shields.io/badge/Next-black?style=for-the-badge&logo=next.js&logoColor=white"></a>
<a href=""><img src="https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white"></a>

## Contributors
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/bkctrl"><img src="https://avatars.githubusercontent.com/u/112859636?v=4?s=100" width="100px;" alt="BK Kang"/><br /><sub><b>BK Kang</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/ashsic"><img src="https://avatars.githubusercontent.com/u/99445200?v=4" width="100px;" alt="Name"/><br /><sub><b>Ashton Sicard</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/hmolavi"><img src="https://avatars.githubusercontent.com/u/75816912?v=4" width="100px;" alt="Name"/><br /><sub><b>
Hossein Molavi
</b></sub></a><br /></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/JackFrostDJ"><img src="https://avatars.githubusercontent.com/u/48857558?v=4" width="100px;" alt="Name"/><br /><sub><b>Joel Jishu
</b></sub></a><br /></td>
    </tr>
  </tbody>
</table>

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started


### Prerequisites


### Installation


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap
- [ ] Real-Time Audio Transcribing
  - [X] Real time processing
  - [X] Balance the model, adjusting speed to performance ratio
  - [ ] Compile all of the audio chunks back to singular output, making it user friendly
- [X] Detection of blacklisted words
  - [X] Detection of a single blacklisted word in live feed
  - [ ] Integerating a quick algorithm to check for words in a list. (Hashmap!)
- [ ] Customizable Alerts (beep, mute, etc.)
- [ ] Live Translation / Expand the blacklisted words feature to multiple languages
  - [ ] Ability to translate on the fly -> Need full sentences not small chunks
  - [ ] Bleep out words from the translated speech
- [ ] Dashboard: A web-based dashboard for configuration and monitoring
- [ ] Integration with Major Streaming Platforms (Twitch, YouTube, etc.)


<p align="right">(<a href="#readme-top">back to top</a>)</p>
