import React from "react";
import PropTypes from "prop-types";
import { formatDate } from "@/utils";

const ArticleHeader = props => {

  const { title, date, body } = props;

  const largeTitle = title.length > 75;

  const fontSize = largeTitle ? (
    "text-2xl leading-snug sm:text-4xl sm:leading-snug lg:text-5xl lg:leading-tight"
  ) : (
    "text-3xl leading-snug sm:text-5xl sm:leading-snug md:text-6xl md:leading-tight lg:text-7xl lg:leading-tight"
  );

  const text = body.filter(b => b.type === "text").map(b => b.value).join(" ");
  const wpm = 225;
  const words = text.trim().split(/\s+/).length;
  const minutes = Math.ceil(words / wpm);

  return (
    <div className="mb-6 sm:mb-8 md:mb-12">
      <h1 className={`${fontSize} text-center font-serif font-semibold text-slate-800 mb-3 sm:mb-4 md:mb-6`}>{title}</h1>
      <div className="flex flex-col text-sm items-center text-slate-500 justify-center gap-1 sm:text-lg sm:flex-row sm:gap-0 lg:text-xl">
        <time>{formatDate(date)}</time>
        <span className="hidden w-1 h-1 bg-slate-500 rounded-full mx-3 sm:inline-block" />
        <span className="text-xs sm:text-lg lg:text-xl">{minutes} minute{minutes === 1 ? "" : "s"}</span>
      </div>
      <div className="w-48 max-w-xs mx-auto h-px bg-slate-300 mt-6 sm:w-full sm:mt-8 md:mt-12 md:max-w-sm" />
    </div>
  );
};

ArticleHeader.propTypes = {
  title: PropTypes.string.isRequired,
  date: PropTypes.string.isRequired,
  body: PropTypes.array.isRequired
};

export default ArticleHeader;