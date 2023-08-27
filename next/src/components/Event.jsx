import React from "react";
import PropTypes from "prop-types";

const Event = props => {

  const { event } = props;

  return (
    <div>
      <h2>{event.name}</h2>
      <time>{event.start} - {event.end}</time>
      <img src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${event.image}`} alt={event.name} />
      <div dangerouslySetInnerHTML={{ __html: event.description }} />
      {event.subevents && event.subevents.length > 0 && (
        <div>
          {event.subevents.map(subevent => <Event key={subevent.id} event={subevent} />)}
        </div>
      )}
    </div>
  );
};

Event.propTypes = {
  event: PropTypes.object.isRequired
};

export default Event;