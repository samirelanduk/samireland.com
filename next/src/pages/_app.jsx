import Nav from "@/components/Nav"
import "@/styles/globals.css"
import { Bitter, Lora, Merriweather, Montserrat, Noto_Serif, Nunito, Open_Sans, Playfair_Display, Poppins, Raleway } from "next/font/google";

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
  return (
    <div className={`h-screen flex font-sans ${serif.variable} ${sans.variable}`}>
      <Nav />
      <div className="flex flex-col flex-grow py-8 px-4 sm:px-6 sm:py-12 md:px-10 md:py-16">
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
