import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "StreamGuard",
  description: "StreamGuard - Safely filter your stream contents",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
