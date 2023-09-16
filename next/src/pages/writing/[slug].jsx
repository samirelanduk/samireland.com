import ArticleBody from "@/components/ArticleBody";
import SocialShare from "@/components/SocialShare";
import Head from "next/head";
import { fetchRemoteData } from "@/fetch";

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
      <SocialShare title={title} />
    </main>
  )
}


export async function getStaticProps({ params }) {
  const data = await fetchRemoteData(`writing/${params.slug}`);
  if (!data) return {notFound: true};
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

export async function getStaticPaths() {
  const data = await fetchRemoteData("writing/", {articles: []});
  const staticPaths = {
    paths: data.articles.map(article => ({params: { slug: article.slug }})),
    fallback: "blocking"
  }
  return staticPaths;
}