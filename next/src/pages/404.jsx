import Head from "next/head";

export default function PageNotFound() {
  return (
    <main>
      <Head>
        <title>Page Not Found - Sam Ireland</title>
      </Head>
      <div className="font-semibold text-center max-w-lg mx-auto text-slate-500 text-xl leading-relaxed py-24 xs:text-2xl xs:leading-relaxed xs:py-20 md:text-3xl md:leading-relaxed md:py-10 xl:text-4xl xl:leading-relaxed xl:py-5 xl:max-w-2xl">
        Regrettably, this URL does not match any page on this website.
        You are encouraged to look elsewhere.
      </div>
    </main>
  )
}
