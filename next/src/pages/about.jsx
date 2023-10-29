import Head from "next/head";
import Event from "../components/Event";
import { fetchRemoteData } from "@/fetch";

export default function About({title, text, events, meta}) {
  return (
    <main className="mx-auto max-w-md px-2 sm:max-w-4xl xl:max-w-4xl">
      <Head>
        <title>{`${meta.title} - Sam Ireland`}</title>
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
      <h1 className="title">{title}</h1>
      <div dangerouslySetInnerHTML={{__html: text}} className="intro" />
      <div className="flex flex-col gap-16 max-w-4xl mx-auto relative sm:gap-24">
        <div className="hidden absolute w-2 h-full bg-green-sidc-faint z-0 left-10 ml-1 sm:block md:left-16" />
        {events.map((event, index) => <Event key={index} event={event} />)}
      </div>
    </main>
  )
}


export async function getStaticProps() {
  const data = await fetchRemoteData("about", {
    title: "", text: "", events: [], meta: {}
  });
  if (!data) return {notFound: true};
  return {
    props: {
      title: data.title,
      text: data.text,
      events: data.events,
      meta: data.meta
    }
  }
}