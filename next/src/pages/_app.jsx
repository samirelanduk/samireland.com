import "@/styles/globals.css"
import Link from "next/link"

export default function App({ Component, pageProps }) {
  return (
    <div>
      <nav>
        <Link href="/">samireland.com</Link>
        <Link href="/projects/">Projects</Link>
        <Link href="/articles/">Articles</Link>
      </nav>
      <Component {...pageProps} />
    </div>
  )
}
