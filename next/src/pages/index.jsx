import Head from "next/head";

export default function Home({title, about, meta}) {
  return (
    <main>
      <Head>
        <title>{meta.title}</title>
        <meta name="description" content={meta.description} />
      </Head>
      <h1>{title}</h1>
      <div>
        {about}
      </div>
    </main>
  )
}

export async function getStaticProps() {
  const res = await fetch(process.env.NEXT_PUBLIC_API_URL)
  const data = await res.json()

  return {
    props: {
      title: data.title,
      about: data.about,
      meta: data.meta
    }
  }
}
