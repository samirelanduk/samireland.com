import Head from "next/head";

export default function About({title, text}) {
  return (
    <main>
      <Head>
        <title>{title} - Sam Ireland</title>
      </Head>
      <div dangerouslySetInnerHTML={{__html: text}} />
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
    }
  }
}