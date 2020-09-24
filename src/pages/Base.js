import React from "react";

const Base = props => {
  return (
    <div className="base">
      {props.children}
    </div>
  );
};

Base.propTypes = {
  
};

export default Base;