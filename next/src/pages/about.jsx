import Head from "next/head";
import Event from "../components/Event";

export default function About({title, text, events, meta}) {
  return (
    <main>
      <Head>
        <title>{`${meta.title} - Sam Ireland`}</title>
        <meta name="description" content={meta.description} />
      </Head>
      <h1>{title}</h1>
      <div dangerouslySetInnerHTML={{__html: text}} />
      <div>
        {events.map((event, index) => <Event key={index} event={event} />)}
      </div>
    </main>
  )
}


export async function getStaticProps() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/about`)
  const data = await res.json()

  return {
    props: {
      title: data.title,
      text: data.text,
      events: data.events,
      meta: data.meta
    }
  }
}