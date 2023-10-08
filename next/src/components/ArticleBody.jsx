import React from "react";
import PropTypes from "prop-types";
import Figure from "./Figure";

const ArticleBody = props => {

  const { blocks } = props;

  return (
    <div className="max-w-5xl mx-auto prose prose-a:text-green-sidc lg:prose-xl">
      {blocks.map((block, index) => {
        if (block.type === "text") {
          return <div key={index} dangerouslySetInnerHTML={{__html: block.value}}></div>
        }
        if (block.type === "code") {
          return <pre key={index}>{block.value.code}</pre>
        }
        if (block.type === "figure") {
          return <Figure key={index} figure={block.value} />
        }
      })}
    </div>
  );
};

ArticleBody.propTypes = {
  blocks: PropTypes.array.isRequired
};

export default ArticleBody;