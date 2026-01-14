import React from "react";
import PropTypes from "prop-types";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/cjs/styles/prism";

const CodeBlock = props => {

  const { code, language } = props;

  return (
    <div className="max-w-full overflow-x-auto text-2xs sm:text-sm md:text-base">
      <SyntaxHighlighter
        language={language}
        style={vscDarkPlus}
        customStyle={{paddingLeft: "2rem", paddingRight: "2rem", fontSize: "inherit"}}
        codeTagProps={{style: {fontSize: "inherit"}}}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
};

CodeBlock.propTypes = {
  code: PropTypes.string.isRequired,
  language: PropTypes.string.isRequired
};

export default CodeBlock;