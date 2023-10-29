import React from "react";
import PropTypes from "prop-types";

const Event = props => {

  const { event, isSub } = props;

  const formatMonth = dateString => {
    if (!dateString) return "";
    const date = new Date(dateString);
    const month = date.toLocaleString("default", { month: "long" });
    return `${month} ${date.getFullYear()}`;
  }

  return (
    <div className="z-10 relative">
      {isSub && (
        <div className={`border-green-sidc-faint rounded-bl-3xl absolute border-l-8 border-b-8 w-20 h-16 -top-1 -left-12 ml-3 sm:-left-20 sm:-top-7 md:-left-24 md:ml-1 md:-top-1 md:w-32`} />
      )}
      <div className="flex gap-3 flex-col sm:flex-row sm:gap-6">
        <img
          alt={event.name}
          className={`object-contain rounded-lg flex-shrink-0 z-20  ${isSub ? "w-28 h-28 sm:w-16 sm:h-16 md:w-28 md:h-28" : "w-36 h-36 sm:w-24 sm:h-24 md:w-36 md:h-36"}`}
          src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${event.image}`}
        />
        <div className="">
          <h2 className="font-semibold text-2xl font-serif md:text-3xl">{event.name}</h2>
          <time className="text-slate-500 block mb-2 text-bse md:text-lg">{formatMonth(event.start)} - {formatMonth(event.end)}</time>
          <div
            dangerouslySetInnerHTML={{ __html: event.description }}
            className={`prose prose-p:my-2 max-w-none text-slate-800 ${isSub ? "text-sm" : "text-base"}`}
          />
        </div>
      </div>
      {event.subevents && event.subevents.length > 0 && (
        <div className="ml-12 flex flex-col gap-16 pt-16 relative sm:ml-28 md:ml-40">
          <div className="absolute w-2 h-full bg-green-sidc-faint z-0 top-0 -left-12 ml-3 sm:hidden md:left-16" />
          {event.subevents.map(subevent => <Event key={subevent.id} event={subevent} isSub={true} />)}
        </div>
      )}
    </div>
  );
};

Event.propTypes = {
  event: PropTypes.object.isRequired,
  isSub: PropTypes.bool
};

export default Event;