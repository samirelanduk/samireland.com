import Footer from "@/components/Footer";
import Nav from "@/components/Nav"
import "@/styles/globals.css"
import { Bitter, Lora, Abel, Merriweather, Montserrat, Noto_Serif, Noto_Sans, Nunito, Dosis, Open_Sans, Playfair_Display, Poppins, Raleway, Sen, Albert_Sans, Arsenal  } from "next/font/google";

import Head from "next/head";
import { usePathname } from "next/navigation";
import Div100vh from "react-div-100vh";

const serif = Bitter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-serif",
  weight: ["400", "500", "700"]
})

// Nunito, Open_Sans, Poppins, Raleway, Noto_Sans, Albert_Sans
const sans = Nunito({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-sans",
  weight: ["400", "700"]
})


export default function App({ Component, pageProps }) {

  const isHome = usePathname() === "/";

  return (
    <div className={`font-sans ${serif.variable} ${sans.variable}`}>
      <Head>
        <link href="/images/favicon.svg" rel="icon" type="image/svg" />
      </Head>
      <div className="flex flex-col">
        {!isHome && <Nav />}
        <div className={`flex-grow h-full flex flex-col ${isHome ? "" : "px-4 pt-20 sm:px-6 sm:pt-24 md:px-10 md:pt-28 xl:px-14 xl:pt-32 3xl:pt-36 3xl:px-18 "}`}>
          <Component {...pageProps} />
        </div>
        <Footer isHome={isHome} />
      </div>
    </div>
  )
}
