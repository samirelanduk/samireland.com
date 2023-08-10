import "@/styles/globals.css"

export default function App({ Component, pageProps }) {
  return (
    <div>
      <nav>samireland.com</nav>
      <Component {...pageProps} />
    </div>
  )
}
