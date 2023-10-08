import ArticlePreview from "@/components/ArticlePreview";
import { fetchRemoteData } from "@/fetch";
import Head from "next/head";

export default function Writing({title, text, articles, meta}) {
  return (
    <main className="mx-auto max-w-sm sm:max-w-3xl xl:max-w-4xl 3xl:max-w-10xl">
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
      <h1 className="font-semibold text-3xl font-serif mb-3 sm:text-4xl sm:mb-4">{title}</h1>
      <div dangerouslySetInnerHTML={{__html: text}}  className="text-base pb-8 mb-10 border-b max-w-4xl sm:text-lg sm:pb-10 sm:mb-12"/>
      <div className="flex flex-wrap gap-16 sm:gap-12 md:gap-14 xl:gap-20">
        {articles.map(article => <ArticlePreview key={article.title} article={article} />)}
      </div>
    </main>
  )
}


export async function getStaticProps() {
  const data = await fetchRemoteData("writing", {
    title: "", text: "", articles: [], meta: {}
  });
  if (!data) return {notFound: true};
  return {
    props: {
      title: data.title,
      text: data.text,
      articles: data.articles,
      meta: data.meta
    }
  }
}
