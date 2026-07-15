import Link from "next/link";
import { splitByIndices } from "@/search";
import { formatDate } from "@/utils";

const SearchResult = props => {

  const { result, selected, id, onSelect, onHover } = props;

  const { entry, titleIndices } = result;

  const icons = {
    page: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
        <path d="M5 12h14M13 6l6 6-6 6" />
      </svg>
    ),
    article: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M16 13H8M16 17H8M10 9H8" />
      </svg>
    ),
    book: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 0 6.5 22H20V2H6.5A2.5 2.5 0 0 0 4 4.5z" />
      </svg>
    ),
    project: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
        <path d="M16 18l6-6-6-6M8 6l-6 6 6 6" />
      </svg>
    ),
    event: (
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 6v6l4 2" />
      </svg>
    ),
  };

  const imageClass = {
    article: "w-10 h-7 object-cover rounded-sm shadow-sm",
    book: "w-7 h-10 object-cover rounded-sm shadow-sm",
    project: "w-8 h-8 object-cover rounded-sm",
    event: "w-8 h-8 object-cover rounded-sm",
  }[entry.type];

  const segments = splitByIndices(entry.title, titleIndices);

  const meta = entry.type === "article" && entry.meta ? formatDate(entry.meta, true) : entry.meta;

  return (
    <Link
      href={entry.url}
      id={id}
      role="option"
      aria-selected={selected}
      onClick={onSelect}
      onMouseMove={onHover}
      className={`flex items-center gap-3 px-3 py-2 border-l-2 sm:px-4 ${selected ? "border-green-sidc bg-green-sidc/10" : "border-transparent"}`}
    >
      <div className="w-10 h-10 flex-shrink-0 flex items-center justify-center">
        {entry.image ? (
          <img
            src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${entry.image}`}
            alt=""
            className={imageClass}
          />
        ) : (
          <div className="w-8 h-8 rounded bg-green-sidc/10 text-green-sidc flex items-center justify-center">
            {icons[entry.type]}
          </div>
        )}
      </div>
      <div className="min-w-0 flex-grow">
        <div className="font-serif font-medium text-slate-800 truncate text-sm sm:text-base">
          {segments.map((segment, index) => segment.highlighted ? (
            <span key={index} className="text-green-sidc font-semibold">{segment.text}</span>
          ) : (
            <span key={index}>{segment.text}</span>
          ))}
        </div>
        {entry.subtitle && (
          <div className="text-xs text-slate-500 truncate sm:text-sm">{entry.subtitle}</div>
        )}
      </div>
      {meta && (
        <div className="ml-auto flex-shrink-0 text-2xs text-slate-400 sm:text-xs">{meta}</div>
      )}
    </Link>
  );
};

export default SearchResult;
