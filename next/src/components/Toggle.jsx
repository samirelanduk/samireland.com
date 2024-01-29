import React from "react";
import PropTypes from "prop-types";

const Toggle = props => {

  const { value, setValue, trueLabel, falseLabel } = props;

  const activeLabelClass = "text-green-sidc";
  const inactiveLabelClass = "text-green-sidc-faint transition-color duration-200 cursor-pointer hover:text-green-sidc hover:opacity-70";

  return (
    <div className={`flex text-xs items-center gap-2 font-semibold md:text-sm xl:text-base xl:gap-2.5 ${props.className || ""}`}>
      <div
        className={value ? activeLabelClass : inactiveLabelClass}
        onClick={() => setValue(true)}
      >
        {trueLabel}
      </div>
      <div
        className={"w-8 h-2 rounded relative bg-green-sidc-faint cursor-pointer group md:w-9 xl:w-10 xl:h-2.5"}
        onClick={() => setValue(!value)}
        >
        <div className={`w-4 h-4 bg-green-sidc rounded-full absolute transition-all group-hover:w-4.5 group-hover:scale-[105%] -top-1 xl:w-5 xl:h-5 xl:-top-1.5  xl:mt-px ${value ? "left-0" : "left-4 md:left-5 xl:left-6"}`} />
      </div>
      <div
        className={!value ? activeLabelClass : inactiveLabelClass}
        onClick={() => setValue(false)}
      >
        {falseLabel}
      </div>
    </div>
  );
};

Toggle.propTypes = {
  value: PropTypes.bool.isRequired,
  setValue: PropTypes.func.isRequired,
  trueLabel: PropTypes.string.isRequired,
  falseLabel: PropTypes.string.isRequired,
};

export default Toggle;