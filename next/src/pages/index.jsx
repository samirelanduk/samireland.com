import Head from "next/head";
import { fetchRemoteData } from "@/fetch";
import Link from "next/link";

export default function Home({title, about, meta}) {
  return (
    <main className="flex flex-grow w-full max-w-[100rem] mx-auto flex-col p-4 xs:p-6 md:p-10 xl:p-14">
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
      <div className="w-full md:flex md:justify-between md:gap-16 md:items-start max-w-[100rem] mx-auto">

        <div className="pr-4 xs:pr-6 md:pr-10 xl:pr-14">
          <h1 className="font-serif text-slate-700 text-4xl w-fit border-b-4 border-l-4 border-green-sidc font-semibold mb-8 py-px pl-1 xs:text-5xl xs:py-1 xs:pl-2 xs:border-b-8 xs:border-l-8 xs:mb-9 sm:text-6xl sm:py-1.5 sm:pl-2.5 sm:mb-12 md:text-7xl md:py-2 md:pl-3 md:mb-12 lg:text-8xl lg:border-l-12 lg:border-b-12 lg:py-3 lg:pl-4">
            {title}
          </h1>
          <div className="w-fit mb-8 text-base max-w-2xl text-slate-700 leading-relaxed xs:text-lg xs:leading-relaxed sm:text-xl sm:leading-relaxed md:text-2xl md:leading-relaxed xl:max-w-5xl">
            {about}
          </div>
        </div>

        <img
          src="/images/sam.png" 
          alt="Sam Ireland" 
          className="fixed bottom-0 left-0 opacity-40 grayscale w-0 xs:w-64 sm:w-96 md:w-108 2xl:w-full 2xl:max-w-2xl 3xl:max-w-4xl" 
        />

        <div className="w-fit flex-shrink-0 flex flex-col ml-auto text-right fixed right-4 bottom-24 text-slate-600 justify-center text-base gap-6 xs:right-6 sm:text-lg md:static md:text-xl md:gap-8 lg:justify-start lg:text-2xl lg:gap-10 xl:text-3xl xl:gap-12">
          <Link href="/about/" className="subtle-link">
            ABOUT ME
          </Link>
          <Link href="/projects/" className="subtle-link">
            PROJECTS
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
