import "@/styles/globals.css"
import Link from "next/link"

export default function App({ Component, pageProps }) {
  return (
    <div>
      <nav>
        <Link href="/">samireland.com</Link>
        <Link href="/projects/">Projects</Link>
        <Link href="/about/">About</Link>
        <Link href="/writing/">Writing</Link>
      </nav>
      <Component {...pageProps} />
      <footer className="w-12">
        <a href="https://twitter.com/samirelanduk">
          <img src="/images/twitter.svg" alt="Twitter" />
        </a>
        <a href="https://instagram.com/samirelanduk">
          <img src="/images/instagram.svg" alt="Instagram" />
        </a>
        <a href="https://www.linkedin.com/in/samirelanduk/">
          <img src="/images/linkedin.svg" alt="LinkedIn" />
        </a>
        <a href="/rss" title="Subscribe to RSS feed">
          RSS
        </a>
      </footer>
    </div>
  )
}
