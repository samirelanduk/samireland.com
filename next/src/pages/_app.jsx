import "@/styles/globals.css"
import Link from "next/link"

export default function App({ Component, pageProps }) {
  return (
    <div className="bg-[#f0f5f0] h-screen flex">
      <nav className="flex flex-col">
        <Link href="/">samireland.com</Link>
        <Link href="/projects/">Projects</Link>
        <Link href="/about/">About</Link>
        <Link href="/writing/">Writing</Link>
      </nav>
      <div className="flex flex-col flex-grow">
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
