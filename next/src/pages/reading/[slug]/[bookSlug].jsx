import { fetchRemoteData } from "@/fetch";
import { formatDate } from "@/utils";
import Head from "next/head";
import Link from "next/link";
import BookRating from "@/components/BookRating";
import BookCategory from "@/components/BookCategory";
import CurrentlyReadingBadge from "@/components/CurrentlyReadingBadge";

export default function Book(props) {

  const {
    title,
    subtitle,
    author,
    year,
    image,
    rating,
    category,
    started,
    finished,
    notes,
    meta,
    queueSlug,
    queueTitle,
    previousBook,
    nextBook,
  } = props;

  const metaText = "text-base sm:text-lg xl:text-xl";

  return (
    <main className="mx-auto max-w-sm sm:max-w-3xl xl:max-w-4xl 3xl:max-w-10xl">
      <Head>
        <title>{`${meta.title} - Sam Ireland`}</title>
        <meta name="description" content={meta.description} />
        <meta content="summary_large_image" name="twitter:card"/>
        <meta content="@samirelanduk" name="twitter:site"/>
        <meta content={meta.title} name="twitter:title"/>
        <meta content={meta.description} name="twitter:description"/>
        {image ? (
          <>
            <meta content={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${image}`} property="twitter:image"/>
            <meta content={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${image}`} property="og:image"/>
          </>
        ) : (
          <>
            <meta content="https://samireland.com/images/social-card.png" name="twitter:image"/>
            <meta content="https://samireland.com/images/social-card.png" property="og:image"/>
          </>
        )}
        <meta property="og:title" content={meta.title} />
        <meta property="og:description" content={meta.description} />
      </Head>
      <Link href={`/reading/${queueSlug}`} className="subtle-link group inline-flex items-center gap-1.5 text-sm font-semibold text-slate-500 mb-8 sm:text-base sm:mb-10">
        <span className="transition-transform duration-300 group-hover:-translate-x-1">←</span>
        {queueTitle}
      </Link>

      <article>
        <header className="flex flex-col items-center text-center gap-7 sm:flex-row sm:items-start sm:text-left sm:gap-8 xl:gap-12">
          {image && (
            <img
              alt={title}
              className="w-40 flex-shrink-0 rounded-md object-cover shadow-xl shadow-slate-900/15 ring-1 ring-slate-900/10 sm:w-44 xl:w-52 3xl:w-60"
              src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${image}`}
            />
          )}

          <div className="flex flex-col items-center sm:items-start">
            {!finished && <CurrentlyReadingBadge className="mb-3" />}

            <h1 className="font-serif font-semibold text-slate-800 text-3xl mb-2 sm:text-4xl xl:text-5xl 3xl:text-6xl">
              {title}
            </h1>

            {subtitle && (
              <p className="text-slate-600 text-lg mb-3 sm:text-xl xl:text-2xl">{subtitle}</p>
            )}

            <div className={`flex flex-wrap items-center justify-center gap-2 mb-3 sm:justify-start ${metaText}`}>
              <p className="text-slate-500">{author}, {year}</p>
              <BookCategory category={category} large={true} />
            </div>

            <p className={`flex flex-wrap items-center justify-center gap-x-2 gap-y-1 text-slate-700 mb-5 sm:justify-start ${metaText}`}>
              <span>{formatDate(started)}</span>
              {finished && (
                <>
                  <span className="text-slate-400">–</span>
                  <span>{formatDate(finished)}</span>
                </>
              )}
            </p>

            {rating != null && (
              <div className="flex items-center gap-3">
                <BookRating rating={rating} large={true} />
                <span className="font-semibold text-slate-900 text-sm sm:text-base">{rating}<span className="text-slate-400">/10</span></span>
              </div>
            )}
          </div>
        </header>

        {notes && (
          <div className="mt-10 pt-10 border-t border-slate-300 sm:mt-12 sm:pt-12">
            <div
              className="prose prose-slate prose-a:text-green-sidc prose-a:no-underline hover:prose-a:underline lg:prose-xl max-w-none"
              dangerouslySetInnerHTML={{ __html: notes }}
            />
          </div>
        )}
      </article>

      {(previousBook || nextBook) && (
        <nav className="flex flex-col gap-8 mt-10 pt-10 border-t border-slate-300 sm:flex-row sm:justify-between sm:gap-10 sm:mt-12 sm:pt-12">
          {previousBook && (
            <Link
              href={`/reading/${queueSlug}/${previousBook.slug}`}
              className="group flex items-center gap-4 sm:max-w-[45%]"
            >
              {previousBook.image && (
                <img
                  alt={previousBook.title}
                  src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${previousBook.image}`}
                  className="w-14 flex-shrink-0 rounded object-cover shadow-md shadow-slate-900/10 ring-1 ring-slate-900/10 transition-transform duration-300 group-hover:scale-105 sm:w-16"
                />
              )}
              <div>
                <div className="flex items-center gap-1.5 text-xs uppercase tracking-wide text-slate-400 font-semibold mb-1">
                  <span className="transition-transform duration-300 group-hover:-translate-x-1">←</span>
                  Previous
                </div>
                <div className="font-serif font-semibold text-slate-800 text-lg leading-snug transition-colors duration-300 group-hover:text-green-sidc sm:text-xl">
                  {previousBook.title}
                </div>
                <div className="text-sm text-slate-500 sm:text-base">{previousBook.author}</div>
              </div>
            </Link>
          )}
          {nextBook && (
            <Link
              href={`/reading/${queueSlug}/${nextBook.slug}`}
              className="group flex flex-row-reverse items-center gap-4 text-right sm:max-w-[45%] sm:ml-auto"
            >
              {nextBook.image && (
                <img
                  alt={nextBook.title}
                  src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${nextBook.image}`}
                  className="w-14 flex-shrink-0 rounded object-cover shadow-md shadow-slate-900/10 ring-1 ring-slate-900/10 transition-transform duration-300 group-hover:scale-105 sm:w-16"
                />
              )}
              <div>
                <div className="flex items-center justify-end gap-1.5 text-xs uppercase tracking-wide text-slate-400 font-semibold mb-1">
                  Next
                  <span className="transition-transform duration-300 group-hover:translate-x-1">→</span>
                </div>
                <div className="font-serif font-semibold text-slate-800 text-lg leading-snug transition-colors duration-300 group-hover:text-green-sidc sm:text-xl">
                  {nextBook.title}
                </div>
                <div className="text-sm text-slate-500 sm:text-base">{nextBook.author}</div>
              </div>
            </Link>
          )}
        </nav>
      )}
    </main>
  );
}


export async function getStaticProps({ params }) {
  const [data, queueData] = await Promise.all([
    fetchRemoteData(`reading/${params.slug}/${params.bookSlug}`),
    fetchRemoteData(`reading/${params.slug}`),
  ]);
  if (!data || !queueData) return { notFound: true };
  return {
    props: {
      title: data.title,
      subtitle: data.subtitle,
      author: data.author,
      year: data.year,
      image: data.image,
      rating: data.rating,
      category: data.category,
      started: data.started,
      finished: data.finished,
      notes: data.notes,
      meta: data.meta,
      queueSlug: params.slug,
      queueTitle: queueData.title,
      previousBook: data.previous_book ?? null,
      nextBook: data.next_book ?? null,
    }
  };
}

export async function getStaticPaths() {
  const data = await fetchRemoteData("reading", { queue: [] });
  const paths = data.queues.flatMap(queue =>
    queue.books.map(book => ({
      params: { slug: queue.slug, bookSlug: book.slug },
    }))
  );
  return {
    paths,
    fallback: "blocking",
  };
}
