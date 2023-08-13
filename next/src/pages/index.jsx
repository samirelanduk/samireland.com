import Head from "next/head";

export default function Home({title, about}) {
  return (
    <main>
      <Head>
        <title>{title}</title>
      </Head>
      <h1>Sam Ireland</h1>
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
    }
  }
}
