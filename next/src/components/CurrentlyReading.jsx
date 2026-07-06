import Link from "next/link";
import BookPreview from "@/components/BookPreview";
import CurrentlyReadingBadge from "@/components/CurrentlyReadingBadge";

const CurrentlyReading = props => {

  const { queues, className="" } = props;

  const books = queues.flatMap(queue =>
    queue.books
      .filter(book => !book.finished)
      .map(book => ({ book, queue }))
  );

  if (books.length === 0) return null;

  const bookHeight = 75;
  const queueLinkClass = "subtle-link text-sm whitespace-nowrap font-semibold text-slate-500 sm:text-base";

  return (
    <div className={`${className} flex flex-shrink-0 flex-col gap-4 items-start xl:items-end`}>
      <CurrentlyReadingBadge />
      <div className="flex flex-col gap-x-8 gap-y-6 sm:flex-row sm:flex-wrap lg:gap-x-16 xl:gap-x-8 2xl:gap-x-12">
        {books.map(({ book, queue }) => (
          <div
            key={`${queue.slug}-${book.slug}`}
            className="flex flex-col gap-2"
          >
            <Link href={`/reading/${queue.slug}`} className={queueLinkClass}>
              {queue.title}
            </Link>
            <BookPreview
              book={book}
              queue={queue}
              compress={true}
              bookHeight={bookHeight * 2/3}
              className="group md:hidden xl:flex 2xl:hidden"
            />
            <BookPreview
              book={book}
              queue={queue}
              compress={false}
              bookHeight={bookHeight}
              className="group hidden md:flex xl:hidden 2xl:flex"
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default CurrentlyReading;
