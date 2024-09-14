import Webcam from "react-webcam";

const Secondary: React.FC = () => {

  return (
    <div 
      className="w-full h-svh bg-slate-100 flex justify-center"
    >
      <div
        className="w-3/4 shadow-2xl h95 bg-slate-300 flex flex-col pb-12 rounded-xl"
      >
        <div 
          className="w-full h-24 bg-slate-300 rounded-xl"
        >
          <div>
            <h2
              className="text-6xl mt-6 ml-12"
            >
              Try the demo!
            </h2>
          </div>
        </div>

        <div className="w-full h-full flex">
          <div className="w-2/3 h-full">
            <div className="mt-4 ml-4 pt-0.5 h-full w-full gbg1">
              <div className="mt-4 ml-4 h-full w-full">
                <div className="h-3/4 border border-slate-400 bg-cyan-50">
                  {/* <Webcam /> */}
                </div>
                <div className="flex h-1/4 border border-slate-400 bg-white">
                  <div 
                    className="w-full h-1/3 border-b-2 flex"
                  >
                    <div className="w-1/3 h-full">
                    
                    </div>
                    <div className="w-1/3 h-full flex justify-center items-center">
                      <button
                        className="size-12 rounded-3xl bg-white border border-black"
                      >
                        mic
                      </button>
                    </div>
                    <div className="w-1/3 h-full">
                    
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
