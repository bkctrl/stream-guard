import { LinkInterface } from "../../types";
import Link from "next/link";

export default function Footer() {

  const links: LinkInterface[] = [
    {
      route: "documentation",
      title: "Documentation"
    },
    {
      route: "login",
      title: "Sign In"
    },
    {
      route: "signup",
      title: "Create an account"
    }
  ]

  return (
    <footer className="w-full h-96 flex footer-bg">
      


      <div 
        className="w-full h-full flex flex-col pt-8"
      >
        <h1 className="pl-16 text-lg font-semibold hover:animate-pulse">
          <Link href={"/"}>
            Real Time Content Moderator 
          </Link>
        </h1>

        <ul className="pl-24 mt-4">
          {
            links.map((link) => {
              return (
                <li key={link.route}>
                  <Link
                    className="hover:font-semibold" 
                    href={link.route}
                  >
                    {link.title}
                  </Link>
                </li>
              );
            })
          }
        </ul>
      </div>

    </footer>
  );
}