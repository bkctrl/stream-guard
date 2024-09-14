import Link from 'next/link';

export default function HeaderBar() {
  return (
    <header className=" h-16 w-full flex justify-between px-8 border-2 border-slate-800">
      <div className="flex justify-center items-center">
        <h2>
          Real Time Content Moderator
        </h2>

      </div>

      <div className="flex justify-center items-center">
        <Link
          href="/login"
          className="bg-amber-200 hover:bg-amber-100 active:bg-amber-300 px-4 py-1.5 border-2 border-slate-400 rounded-3xl"
        >
          Sign In
        </Link>
      </div>



    </header>
  );
}