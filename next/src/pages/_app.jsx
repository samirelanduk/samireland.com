import Nav from "@/components/Nav"
import "@/styles/globals.css"

export default function App({ Component, pageProps }) {
  return (
    <div className="h-screen flex">
      <Nav />
      <div className="flex flex-col flex-grow py-10">
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
