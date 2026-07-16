import BookPreview from "@/components/BookPreview";
import BookCategory from "@/components/BookCategory";
import BookRating from "@/components/BookRating";
import ReadingTimeline from "@/components/ReadingTimeline";
import Toggle from "@/components/Toggle";
import { fetchRemoteData } from "@/fetch";
import { formatDate } from "@/utils";
import Head from "next/head";
import Link from "next/link";
import { useState } from "react";

export default function Queue(props) {

  const { title, description, books, meta, slug, now } = props;

  const [timelineView, setTimelineView] = useState(true);

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
      <h1 className="title">{title}</h1>
      <p className="intro">{description}</p>
      <Toggle
        value={timelineView}
        setValue={setTimelineView}
        trueLabel="Timeline"
        falseLabel="List"
        className="hidden mb-8 ml-auto w-fit -mt-4 sm:flex"
      />
      <div className={`flex flex-col gap-12 ${timelineView ? "sm:hidden" : "sm:max-w-3xl"}`}>
        {[...books].reverse().map(book => (
          <Link
            href={`/reading/${slug}/${book.slug}`}
            className="flex gap-4 group"
            key={book.slug}
          >
            <img src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${book.image}`} alt={book.title} className="w-20 h-auto flex-shrink-0 rounded object-cover shadow-md shadow-slate-900/10 ring-1 ring-slate-900/10 transition-transform duration-300 group-hover:scale-105 xs:w-24" />
            <div>
              <h2 className="font-serif font-semibold text-slate-800 whitespace-normal text-xl leading-snug truncate transition-colors duration-300 group-hover:text-green-sidc xs:text-2xl">{book.title}</h2>
              <div className="flex flex-wrap items-center justify-start w-fit gap-x-2 gap-y-1 xs:flex-nowrap">
                <div className="text-slate-500 text-sm leading-snug w-full whitespace-normal xs:text-base">{book.author}</div>
                <BookCategory category={book.category} />
              </div>
              <BookRating rating={book.rating} large={true} className="my-2 xs:mt-2.5 xs:mb-3" />
              {!book.finished && <div className="text-green-sidc text-sm mt-0.r5 font-semibold mb-1 xs:text-base">reading</div>}
              <time className="text-slate-400 whitespace-nowrap text-xs xs:text-sm">
                {formatDate(book.started, true)}
                {book.finished && ` – ${formatDate(book.finished, true)}`}
                
              </time>
            </div>
          </Link>
        ))}
      </div>
      {timelineView && <ReadingTimeline className="hidden sm:block" queues={[{slug: slug, books: books}]} now={now} />}
    </main>
  );
}


export async function getStaticProps({ params }) {
  const data = await fetchRemoteData(`reading/${params.slug}`);
  if (!data) return { notFound: true };
  return {
    props: {
      title: data.title,
      description: data.description,
      books: data.books,
      meta: data.meta,
      slug: params.slug,
      now: new Date().toISOString(),
    },
    revalidate: 3600,
  };
}

export async function getStaticPaths() {
  const data = await fetchRemoteData("reading", { queues: [] });
  return {
    paths: data.queues.map(queue => ({ params: { slug: queue.slug } })),
    fallback: "blocking",
  };
}
