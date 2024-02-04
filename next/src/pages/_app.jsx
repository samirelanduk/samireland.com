import { useEffect } from "react";
import Footer from "@/components/Footer";
import Nav from "@/components/Nav"
import "@/styles/globals.css"
import { Bitter, Nunito } from "next/font/google";
import Head from "next/head";
import { usePathname } from "next/navigation";

const serif = Bitter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-serif",
  weight: ["400", "500", "700"]
})

const sans = Nunito({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-sans",
  weight: ["400", "700"]
})


export default function App({ Component, pageProps }) {

  const isHome = usePathname() === "/";

  useEffect(() => {
    const hostnames = ["samireland.com", "www.samireland.com"];
    const currentDomain = window.location.hostname;
    if (hostnames.includes(currentDomain)) {
      const script = document.createElement("script");
      script.defer = true;
      script.dataset.domain = "samireland.com";
      script.src = "https://plausible.io/js/script.js";
      document.body.appendChild(script);
    }
  }, []);

  return (
    <div className={`font-sans ${serif.variable} ${sans.variable}`}>
      <Head>
        <link href="/images/favicon.svg" rel="icon" type="image/svg" />
      </Head>
      <div className="flex flex-col">
        {!isHome && <Nav />}
        <div className={`flex-grow h-full flex flex-col ${isHome ? "" : "px-6 pt-20 sm:px-10 sm:pt-24 md:px-12 md:pt-28 lg:px-20 xl:pt-32 3xl:pt-36"}`}>
          <Component {...pageProps} />
        </div>
        <Footer isHome={isHome} />
      </div>
    </div>
  )
}
