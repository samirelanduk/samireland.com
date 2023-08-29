import Head from "next/head";

export default function Home({title, about, meta}) {
  return (
    <main>
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
