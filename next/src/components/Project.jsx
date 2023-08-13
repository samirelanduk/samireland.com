import React from "react";
import PropTypes from "prop-types";

const Project = props => {

  const { project } = props;

  return (
    <div>
      <h2>{project.name}</h2>
      <div dangerouslySetInnerHTML={{__html: project.description}} />
      {project.code_url && (
        <a href={project.code_url} target="_blank" rel="noopener noreferrer">
          {project.code_url}
        </a>
      )}
      {project.about_url && (
        <a href={project.about_url} target="_blank" rel="noopener noreferrer">
          {project.about_url}
        </a>
      )}
      <img src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${project.image}`} alt={project.name} />
    </div>
  );
};

Project.propTypes = {
  project: PropTypes.object.isRequired,
};

export default Project;