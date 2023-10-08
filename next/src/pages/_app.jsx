import Footer from "@/components/Footer";
import Nav from "@/components/Nav"
import "@/styles/globals.css"
import { Bitter, Lora, Merriweather, Montserrat, Noto_Serif, Nunito, Open_Sans, Playfair_Display, Poppins, Raleway, Sen } from "next/font/google";

const serif = Bitter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-serif",
  weight: ["400", "500", "700"]
})

const sans = Sen({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-sans",
  weight: ["400", "700"]
})

export default function App({ Component, pageProps }) {
  return (
    <div className={`flex font-sans ${serif.variable} ${sans.variable}`}>
      <Nav />
      <div className="flex flex-col flex-grow px-4 pt-20 sm:px-6 sm:pt-24 md:px-10 md:pt-28">
        <div className="flex-grow">
          <Component {...pageProps} />
        </div>
        <Footer />
      </div>
    </div>
  )
}
