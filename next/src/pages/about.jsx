import Head from "next/head";
import Event from "../components/Event";

export default function About({title, text, events}) {
  return (
    <main>
      <Head>
        <title>{title} - Sam Ireland</title>
      </Head>
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
      events: data.events
    }
  }
}