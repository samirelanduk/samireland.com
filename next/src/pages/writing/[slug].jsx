import ArticleBody from "@/components/ArticleBody";
import Head from "next/head";

export default function Article({title, image, date, body, tags, meta}) {
  return (
    <main>
      <Head>
        <title>{`${meta.title} - Sam Ireland`}</title>
        <meta name="description" content={meta.description} />
        <meta content="summary_large_image" name="twitter:card"/>
        <meta content="@samirelanduk" name="twitter:site"/>
        <meta content={meta.title} name="twitter:title"/>
        <meta content={meta.description} name="twitter:description"/>
        <meta content={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${image}`} property="twitter:image"/>
        <meta content={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${image}`} property="og:image"/>
        <meta property="og:title" content={meta.title} />
        <meta property="og:description" content={meta.description} />
      </Head>
      <h1>{title}</h1>
      <time>{date}</time>
      <ArticleBody blocks={body} />
      <div>
        {tags.map(tag => (
          <span key={tag.name}>{tag.name}</span>
        ))}
      </div>
    </main>
  )
}


export async function getServerSideProps({ params }) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/writing/${params.slug}`)
  const data = await res.json()

  return {
    props: {
      title: data.title,
      image: data.image,
      date: data.date,
      body: data.body,
      tags: data.tags,
      meta: data.meta
    }
  }
}