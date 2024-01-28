import React from "react";
import PropTypes from "prop-types";
import SocialShare from "./SocialShare";

const ArticleFooter = props => {

  const { tags, title } = props;

  return (
    <div className="flex -mx-4 flex-col items-center gap-y-3 sm:flex-row justify-between mt-3 sm:mt-6 md:mt-9">
      <div className="flex flex-wrap gap-3 font-semibold text-sm sm:text-base text-slate-900 md:text-lg">
        {tags.map(tag => (
          <div key={tag.name}>#{tag.name}</div>
        ))}
      </div>
      <SocialShare title={title} />
    </div>
  );
};

ArticleFooter.propTypes = {
  tags: PropTypes.array.isRequired,
  title: PropTypes.string.isRequired
};

export default ArticleFooter;