import React from "react";
import PropTypes from "prop-types";
import SocialShare from "./SocialShare";

const ArticleFooter = props => {

  const { tags, title } = props;

  return (
    <div className="flex flex-col items-center gap-y-6 sm:flex-row justify-between mt-8">
      <div>
        {tags.map(tag => (
          <span
            key={tag.name}
            className="text-white rounded-full text-sm px-3 py-1"
            style={{background: tag.color}
          }>
            {tag.name}
          </span>
        ))}
      </div>
      <SocialShare title={title} />
    </div>
  );
};

ArticleFooter.propTypes = {
  tags: PropTypes.array.isRequired
};

export default ArticleFooter;