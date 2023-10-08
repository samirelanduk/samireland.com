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
      <div className="flex flex-col flex-grow px-4 pt-20 pb-8 sm:px-6 sm:pb-12 sm:pt-24 md:px-10 md:pb-16 md:pt-28">
        <div className="flex-grow">
          <Component {...pageProps} />
        </div>
        <footer className="flex h-12 flex-shrink justify-end w-full">
          <a href="https://twitter.com/samirelanduk">
            <img src="/images/twitter.svg" alt="Twitter" className="h-full" />
          </a>
          <a href="https://instagram.com/samirelanduk">
            <img src="/images/instagram.svg" alt="Instagram" className="h-full" />
          </a>
          <a href="https://www.linkedin.com/in/samirelanduk/">
            <img src="/images/linkedin.svg" alt="LinkedIn" className="h-full" />
          </a>
          <a href="/rss" title="Subscribe to RSS feed">
            RSS
          </a>
        </footer>
      </div>
    </div>
  )
}
