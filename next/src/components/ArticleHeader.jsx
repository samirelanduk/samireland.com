import React from "react";
import PropTypes from "prop-types";
import { formatDate } from "@/utils";

const ArticleHeader = props => {

  const { title, date, body } = props;

  const largeTitle = title.length > 75;

  const fontSize = largeTitle ? (
    "text-3xl leading-snug sm:text-4xl sm:leading-snug md:text-5xl md:leading-tight"
  ) : (
    "text-4xl leading-snug sm:text-5xl sm:leading-snug md:text-7xl md:leading-tight"
  );

  const text = body.filter(b => b.type === "text").map(b => b.value).join(" ");
  const wpm = 225;
  const words = text.trim().split(/\s+/).length;
  const minutes = Math.ceil(words / wpm);

  return (
    <div className="mb-16">
      <h1 className={`${fontSize} text-center font-serif font-semibold text-slate-800 mb-3 sm:mb-4 md:mb-6`}>{title}</h1>
      <div className="flex flex-col items-center text-slate-500 justify-center gap-1 sm:text-lg sm:flex-row sm:gap-0">
        <time >{formatDate(date)}</time>
        <span className="hidden w-1 h-1 bg-slate-500 rounded-full mx-3 sm:inline-block" />
        <span>{minutes} minute{minutes === 1 ? "" : "s"}</span>
      </div>
    </div>
  );
};

ArticleHeader.propTypes = {
  title: PropTypes.string.isRequired,
  date: PropTypes.string.isRequired,
  body: PropTypes.array.isRequired
};

export default ArticleHeader;