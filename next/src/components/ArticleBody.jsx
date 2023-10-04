import React from "react";
import PropTypes from "prop-types";

const ArticleBody = props => {

  const { blocks } = props;

  return (
    <div className="max-w-5xl mx-auto prose">
      {blocks.map((block, index) => {
        if (block.type === "text") {
          return <div key={index} dangerouslySetInnerHTML={{__html: block.value}}></div>
        }
        if (block.type === "code") {
          return <pre key={index}>{block.value.code}</pre>
        }
        if (block.type === "figure") {
          return (
            <figure key={index}>
              <img src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${block.value.image}`} alt={block.alt} />
              {block.value.caption && <figcaption dangerouslySetInnerHTML={{__html: block.value.caption}} />}
            </figure>
          )
        }
      })}
    </div>
  );
};

ArticleBody.propTypes = {
  blocks: PropTypes.array.isRequired
};

export default ArticleBody;