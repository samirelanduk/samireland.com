const SearchButton = props => {

  const { onClick, className } = props;

  return (
    <button
      onClick={onClick}
      aria-label="Search the site"
      className={`subtle-link items-center text-slate-600 cursor-pointer ${className || ""}`}
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="w-4 h-4 md:w-[1.1rem] md:h-[1.1rem] xl:w-5 xl:h-5">
        <circle cx="11" cy="11" r="8" />
        <path d="m21 21-4.35-4.35" />
      </svg>
    </button>
  );
};

export default SearchButton;
