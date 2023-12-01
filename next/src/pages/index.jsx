import Head from "next/head";
import { fetchRemoteData } from "@/fetch";
import Link from "next/link";

export default function Home({title, about, meta}) {
  return (
    <main className="flex flex-grow w-full max-w-[100rem] mx-auto flex-col p-4 sm:p-6 md:p-10 xl:p-14">
      <Head>
        <title>{meta.title}</title>
        <meta name="description" content={meta.description} />
        <meta content="summary_large_image" name="twitter:card"/>
        <meta content="@samirelanduk" name="twitter:site"/>
        <meta content={meta.title} name="twitter:title"/>
        <meta content={meta.description} name="twitter:description"/>
        <meta content="https://samireland.com/images/social-card.png" name="twitter:image"/>
        <meta content="https://samireland.com/images/social-card.png" property="og:image"/>
        <meta property="og:title" content={meta.title} />
        <meta property="og:description" content={meta.description} />
      </Head>
      <div className="lg:flex lg:justify-between">
        <div>
          <h1 className="font-serif text-slate-700 text-3xl w-fit border-b-4 border-l-4 border-green-sidc font-semibold mb-6 py-px pl-1 sm:text-4xl sm:mb-8 sm:py-0.5 sm:pl-1.5 md:text-5xl md:mb-10 md:py-1 md:pl-2 md:border-b-8 md:border-l-8 lg:text-6xl lg:mb-12 lg:py-1.5 lg:pl-2.5 xl:text-7xl xl:mb-14 xl:py-2 xl:pl-3">
            {title}
          </h1>
          <div className="text-sm mb-8 sm:text-base md:text-lg lg:text-xl xl:text-2xl">
            {about}
          </div>
        </div>
        <div className="w-fit flex flex-col text-slate-600 justify-center text-base gap-4 sm:text-lg sm:gap-6 md:text-xl md:gap-8 lg:text-2xl lg:gap-10 xl:test-3xl xl:gap-12">
          <Link href="/projects/" className="subtle-link">
            PROJECTS
          </Link>
          <Link href="/about/" className="subtle-link">
            ABOUT ME
          </Link>
          <Link href="/writing/" className="subtle-link">
            WRITING
          </Link>
        </div>
      </div>
    </main>
  )
}

export async function getStaticProps() {
  const data = await fetchRemoteData("", {
    title: "", about: "", meta: {}
  });
  if (!data) return {notFound: true};
  return {
    props: {
      title: data.title,
      about: data.about,
      meta: data.meta
    }
  }
}
