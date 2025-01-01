import React from "react";
import PropTypes from "prop-types";
import Figure from "./Figure";
import CodeBlock from "./CodeBlock";

const ArticleBody = props => {

  const { blocks } = props;

  return (
    <div className="max-w-5xl -mx-4 prose prose-a:text-green-sidc lg:prose-xl">
      {blocks.map((block, index) => {
        if (block.type === "text") {
          return <div key={index} dangerouslySetInnerHTML={{__html: block.value}}></div>
        }
        if (block.type === "code") {
          return <CodeBlock key={index} code={block.value.code} language={block.value.language} />
        }
        if (block.type === "figure") {
          return <Figure key={index} figure={block.value} />
        }
        if (block.type === "section") {
          return (
            <section key={index} className="my-12 sm:my-16 md:my-20">
              <h2 className="text-2xl font-bold">{block.value.title}</h2>
              {block.value.subtitle && <p className="italic -mt-6 lg:-mt-7">{block.value.subtitle}</p>}
              {block.value.body.map((sectionBlock, sectionIndex) => {
                if (sectionBlock.type === "text") {
                  return <div key={sectionIndex} dangerouslySetInnerHTML={{__html: sectionBlock.value}}></div>
                }
                if (sectionBlock.type === "code") {
                  return <CodeBlock key={sectionIndex} code={sectionBlock.value.code} language={sectionBlock.value.language} />
                }
                if (sectionBlock.type === "figure") {
                  return <Figure key={sectionIndex} figure={sectionBlock.value} />
                }
              })}
            </section>
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