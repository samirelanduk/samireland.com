const BookRating = props => {

  const { rating, large=false, className="" } = props;

  if (rating == null) return null;

  const circleClass = `rounded-full ${large ? "h-2 w-2" : "h-1.5 w-1.5"}`;
  const colorClass = rating <= 3 ? "bg-red-500" : rating <= 5 ? "bg-orange-500" : rating <= 7 ? "bg-yellow-500" : "bg-green-700";

  return (
    <div className={`flex flex-shrink-0 items-center ${large ? "gap-1" : "gap-0.5"} ${className}`} title={`${rating}/10`}>
      {Array.from({ length: 10 }).map((_, r) => (
        <span
          key={r}
          className={`${circleClass} ${r < rating ? colorClass : "bg-slate-300"}`}
        />
      ))}
    </div>
  )
}

export default BookRating;