import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ClassSync | Smart Assignment Management",
  description: "Modern academic workflow for higher education.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&family=Syne:wght@400..800&family=JetBrains+Mono:ital,wght@0,100..800;1,100..800&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen selection:bg-[#00D4AA33] selection:text-[#00D4AA]">
        <nav className="sticky top-0 z-50 bg-[#0D1117]/80 backdrop-blur-md border-b border-[#2D3A4A] p-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center px-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-[#00D4AA] rounded-lg rotate-12 flex items-center justify-center">
                <span className="text-black font-black text-lg -rotate-12">C</span>
              </div>
              <h1 className="text-xl font-extrabold tracking-tight text-[#E6EDF3]">ClassSync</h1>
            </div>
            <div className="flex items-center space-x-6">
              <a href="/faculty" className="text-sm font-semibold text-[#8B949E] hover:text-[#00D4AA] transition-colors">Faculty Portal</a>
              <a href="/student" className="text-sm font-semibold text-[#8B949E] hover:text-[#00D4AA] transition-colors">Student Portal</a>
              <div className="w-8 h-8 rounded-full bg-[#1C2333] border border-[#2D3A4A] flex items-center justify-center">
                <span className="text-xs font-bold text-[#8B949E]">JD</span>
              </div>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto p-6 md:p-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
          {children}
        </main>
      </body>
    </html>
  );
}
