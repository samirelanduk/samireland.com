import Link from "next/link";
import { formatDate } from "@/utils";
import BookRating from "@/components/BookRating";
import BookCategory from "@/components/BookCategory";

const BookPreview = props => {

  const { book, queue, bookHeight, reversed=false, compress=false, style, className="" } = props;

  return (
    <Link href={`/reading/${queue.slug}/${book.slug}`} style={style} className={`flex gap-2 ${reversed ? "flex-row-reverse" : "flex-row"} ${className}`}>
      <img
        alt={book.title}
        className="w-auto flex-shrink-0 rounded object-cover shadow-md shadow-slate-900/10 ring-1 ring-slate-900/10 transition-transform duration-300 group-hover:scale-105"
        style={{ height: bookHeight }}
        src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${book.image}`}
      />
      <div className={reversed ? "text-right" : "text-left"}>
        <h3 className={`font-serif font-semibold text-slate-800 leading-snug truncate transition-colors duration-300 group-hover:text-green-sidc ${compress ? "text-base" : "text-xl"}`}>
          {book.title}
        </h3>
        <div className={`mb-1 flex ${compress ? "text-xs flex-col gap-1.5" : "text-sm items-center gap-2"} ${reversed ? (compress ? "items-end" : "flex-row-reverse") : "flex-row"}`}>
          <div className={`flex  items-center text-slate-500 ${compress ? "gap-x-1.5" : "gap-x-2"}`}>
            <div className="whitespace-nowrap">{book.author}</div>
            <BookCategory category={book.category} />
          </div>
          <BookRating rating={book.rating} />
        </div>
        <div className={`text-slate-400 whitespace-nowrap ${compress ? "text-2xs" : "text-xs"}`}>
          {formatDate(book.started, compress)}
          {book.finished && ` – ${formatDate(book.finished, compress)}`}
          {!book.finished && <span className="text-green-sidc font-semibold"> · reading</span>}
        </div>
      </div>
    </Link>
  )
};

export default BookPreview;
