import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/router";
import SearchResult from "@/components/SearchResult";
import { searchEntries } from "@/search";

let cachedIndex = null;

const groupLabels = {
  page: "Pages",
  event: "About",
  article: "Writing",
  book: "Reading",
  project: "Projects",
};

const makeSuggestions = entries => {
  const suggestions = [
    { label: "Pages", items: entries.filter(entry => entry.type === "page").slice(0, 4) },
    { label: "Recent writing", items: entries.filter(entry => entry.type === "article").slice(0, 4) },
    { label: "Currently reading", items: entries.filter(entry => entry.type === "book" && entry.current).slice(0, 3) },
  ];
  return suggestions.filter(group => group.items.length).map(group => ({
    label: group.label,
    items: group.items.map(entry => ({ entry, titleIndices: [] })),
  }));
}

const SearchPalette = props => {

  const { open, onClose } = props;

  const [query, setQuery] = useState("");
  const [entries, setEntries] = useState(cachedIndex);
  const [failed, setFailed] = useState(false);
  const [selected, setSelected] = useState(0);
  const inputRef = useRef();
  const router = useRouter();

  useEffect(() => {
    if (!open) return;
    setQuery("");
    setSelected(0);
    document.body.style.overflow = "hidden";
    const timeout = setTimeout(() => inputRef.current?.focus(), 0);
    return () => {
      document.body.style.overflow = "";
      clearTimeout(timeout);
    };
  }, [open]);

  useEffect(() => {
    if (!open || cachedIndex) return;
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/search-index`)
      .then(resp => resp.ok ? resp.json() : Promise.reject())
      .then(data => {
        cachedIndex = data.entries;
        setEntries(data.entries);
      })
      .catch(() => setFailed(true));
  }, [open]);

  const groups = useMemo(() => {
    if (!entries) return [];
    if (!query.trim()) return makeSuggestions(entries);
    const results = searchEntries(query, entries);
    const grouped = [];
    for (const result of results) {
      const label = groupLabels[result.entry.type];
      let group = grouped.find(g => g.label === label);
      if (!group) {
        group = { label, items: [] };
        grouped.push(group);
      }
      group.items.push(result);
    }
    return grouped;
  }, [entries, query]);

  const flatItems = groups.flatMap(group => group.items);

  useEffect(() => setSelected(0), [query]);

  useEffect(() => {
    const element = document.getElementById(`search-result-${selected}`);
    element?.scrollIntoView({ block: "nearest" });
  }, [selected]);

  if (!open) return null;

  const handleKeyDown = event => {
    if (event.key === "Escape") {
      event.preventDefault();
      onClose();
    } else if (event.key === "ArrowDown") {
      event.preventDefault();
      setSelected(current => Math.min(current + 1, flatItems.length - 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setSelected(current => Math.max(current - 1, 0));
    } else if (event.key === "Enter") {
      const item = flatItems[selected];
      if (item) {
        router.push(item.entry.url);
        onClose();
      }
    }
  };

  const handleOverlayMouseDown = event => {
    if (event.target === event.currentTarget) onClose();
  };

  const handleQueryChange = event => setQuery(event.target.value);

  const handleHover = index => () => setSelected(index);

  const message = failed ? "Search is unavailable right now." : (
    !entries ? "Loading…" : (
      flatItems.length === 0 ? `No results for “${query}”` : null
    )
  );

  let itemIndex = -1;

  return (
    <div
      className="fixed inset-0 z-[100] bg-slate-900/30 backdrop-blur-[2px] p-4 pt-[12vh] sm:pt-[15vh]"
      onMouseDown={handleOverlayMouseDown}
      onKeyDown={handleKeyDown}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Site search"
        className="palette-in mx-auto flex max-h-[65vh] w-full max-w-xl flex-col overflow-hidden rounded-xl border border-slate-200 bg-background-2 shadow-2xl"
      >
        <div className="flex items-center gap-3 border-b border-slate-200 px-4 py-3">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-5 w-5 flex-shrink-0 text-green-sidc">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={handleQueryChange}
            placeholder="Search writing, books, projects..."
            aria-label="Search the site"
            autoComplete="off"
            autoCorrect="off"
            spellCheck="false"
            className="flex-grow bg-transparent text-base text-slate-800 placeholder-slate-400 outline-none sm:text-lg"
          />
          <kbd className="hidden flex-shrink-0 rounded border border-slate-300 px-1.5 py-0.5 font-sans text-2xs text-slate-400 sm:block">
            esc
          </kbd>
        </div>
        <div role="listbox" className="flex-grow overflow-y-auto overscroll-contain py-2">
          {message ? (
            <div className="px-4 py-8 text-center text-sm text-slate-400">{message}</div>
          ) : groups.map(group => (
            <div key={group.label}>
              <div className="px-4 pb-1 pt-3 text-2xs font-bold uppercase tracking-widest text-slate-400">
                {group.label}
              </div>
              {group.items.map(result => {
                itemIndex++;
                const index = itemIndex;
                return (
                  <SearchResult
                    key={result.entry.url + result.entry.title}
                    id={`search-result-${index}`}
                    result={result}
                    selected={index === selected}
                    onSelect={onClose}
                    onHover={handleHover(index)}
                  />
                );
              })}
            </div>
          ))}
        </div>
        <div className="flex items-center justify-center gap-4 border-t border-slate-200 px-4 py-2 text-2xs text-slate-400">
          <span><kbd className="font-sans">↑↓</kbd> navigate</span>
          <span><kbd className="font-sans">↵</kbd> open</span>
          <span><kbd className="font-sans">esc</kbd> close</span>
        </div>
      </div>
    </div>
  );
};

export default SearchPalette;
