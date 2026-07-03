import { bookCategoryColor } from "@/utils";

const BookCategory = props => {

  const { category, large = false } = props;

  if (!category) return null;

  const tagBase = "inline-flex flex-shrink-0 items-center rounded-full bg-opacity-10 font-semibold bg- uppercase tracking-wide";
  const tagClass = `${tagBase} ${bookCategoryColor(category).textColor} ${bookCategoryColor(category).blockColor} ${large ? "px-3 py-1 text-xs sm:text-sm" : "px-1.5 py-0 text-2xs"}`;

  return (
    <span className={tagClass}>{category.name}</span>
  );
};

export default BookCategory;
