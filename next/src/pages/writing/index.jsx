import ArticlePreview from "@/components/ArticlePreview";
import Head from "next/head";

export default function Writing({title, text, articles}) {
  return (
    <main>
      <Head>
        <title>{title} - Sam Ireland</title>
      </Head>
      <div dangerouslySetInnerHTML={{__html: text}} />
      <div>
        {articles.map(article => <ArticlePreview key={article.title} article={article} />)}
      </div>
    </main>
  )
}


export async function getStaticProps() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/writing`)
  const data = await res.json()

  return {
    props: {
      title: data.title,
      text: data.text,
      articles: data.articles,
    }
  }
}
