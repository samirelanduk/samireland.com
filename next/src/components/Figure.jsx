import React from "react";
import PropTypes from "prop-types";

const Figure = props => {

  const { figure } = props;

  return (
    <figure className="w-full max-w-3xl mx-auto">
      <img src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${figure.image}`} className="w-full" />
      {figure.caption && (
        <figcaption
          dangerouslySetInnerHTML={{__html: figure.caption}}
          className="text-center text-slate-600 text-sm sm:text-base md:text-lg"
        />
      )}
    </figure>
  );
};

Figure.propTypes = {
  figure: PropTypes.object.isRequired
};

export default Figure;