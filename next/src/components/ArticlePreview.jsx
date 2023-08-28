import React from "react";
import PropTypes from "prop-types";
import Link from "next/link";

const ArticlePreview = props => {

  const { article } = props;

  return (
    <Link href={`/writing/${article.slug}`}>
      <img src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${article.image}`} alt={article.title} />
      <h2>{article.title}</h2>
      <time>{article.date}</time>
      <div>{article.intro}</div>
      <div>
        {article.tags.map(tag => (
          <span key={tag.name}>{tag.name}</span>
        ))}
      </div>
    </Link>
  );
};

ArticlePreview.propTypes = {
  article: PropTypes.object.isRequired,
};

export default ArticlePreview;