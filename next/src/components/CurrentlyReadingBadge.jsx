const CurrentlyReadingBadge = props => {

  const { className = "" } = props;

  const badgeClass = "inline-flex whitespace-nowrap items-center gap-2 rounded-full bg-green-sidc/10 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-green-sidc sm:text-sm";

  return (
    <div className={`${badgeClass} ${className}`}>
      <span className="h-1.5 w-1.5 rounded-full bg-green-sidc animate-pulse" />
      Currently reading
    </div>
  );
};

export default CurrentlyReadingBadge;
