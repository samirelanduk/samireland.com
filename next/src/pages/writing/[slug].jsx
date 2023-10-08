import ArticleBody from "@/components/ArticleBody";
import SocialShare from "@/components/SocialShare";
import Head from "next/head";
import { fetchRemoteData } from "@/fetch";
import { formatDate } from "@/utils";

export default function Article({title, image, date, body, tags, meta}) {

  const largeTitle = title.length > 75;

  const fontSize = largeTitle ? "text-3xl leading-snug sm:text-4xl sm:leading-snug md:text-5xl md:leading-tight" : "text-4xl leading-snug sm:text-5xl sm:leading-snug md:text-7xl md:leading-tight";

  const text = body.filter(b => b.type === "text").map(b => b.value).join(" ");
  const wpm = 225;
  const words = text.trim().split(/\s+/).length;
  const minutes = Math.ceil(words / wpm);

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
      <article className="px-4 max-w-5xl mx-auto">
        <h1 className={`${fontSize} text-center font-serif font-semibold text-slate-800 mb-6`}>{title}</h1>

        <div className="font-serif flex items-center text-slate-500 mb-16 justify-center sm:text-lg">
          <time >
            {formatDate(date)}
          </time>
          <span className="inline-block mx-2 w-1 h-1 bg-slate-500 rounded-full sm:mx-3" />
          <span>{minutes} minute{minutes === 1 ? "" : "s"}</span>
        </div>
        <ArticleBody blocks={body} />
        <div>
          {tags.map(tag => (
            <span key={tag.name}>{tag.name}</span>
          ))}
        </div>
        <SocialShare title={title} />
      </article>
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