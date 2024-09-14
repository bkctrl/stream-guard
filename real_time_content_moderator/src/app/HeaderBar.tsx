export default function HeaderBar() {
  return (
    <div className="h-16 w-full flex justify-between px-8 border-2 border-slate-800">
      <div className="flex justify-center items-center">
        <h2>
          Real Time Content Moderator
        </h2>

      </div>

      <div className="flex justify-center items-center">
        <button
          className="bg-amber-400 hover:bg-amber-300 focus:bg-amber-500 px-4 py-1.5 border-2 border-slate-400 rounded-3xl"
        >
          Sign In
          <i></i>
        </button>
      </div>



    </div>
  );
}