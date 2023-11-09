import PropTypes from "prop-types";
import GithubIcon from "@/images/github.svg?react"
import WebIcon from "@/images/web.svg?react"

const Project = props => {

  const { project } = props;

  const linkClass = "w-6 h-6 fill-green-sidc";

  return (
    <div className="w-full sm:max-w-xl">
      <img
        src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${project.image}`}
        className="w-44 rounded-lg"
        alt={project.name}
      />
      <h2 className="font-serif font-semibold text-2xl mb-2">{project.name}</h2>
      <div className="flex gap-2 mb-2">
        {project.code_url && (
          <a href={project.code_url} target="_blank" rel="noopener noreferrer">
            <GithubIcon className={linkClass} />
          </a>
        )}
        {project.about_url && (
          <a href={project.about_url} target="_blank" rel="noopener noreferrer">
            <WebIcon className={linkClass} />
          </a>
        )}
      </div>
      <div dangerouslySetInnerHTML={{__html: project.description}} className="prose-sm" />
      <div className="flex flex-wrap gap-2 font-semibold text-xs sm:text-sm text-slate-900 md:text-base">
        {project.tags.map(tag => (
          <div key={tag.name}>#{tag.name}</div>
        ))}
      </div>
    </div>
  );
};

Project.propTypes = {
  project: PropTypes.object.isRequired,
};

export default Project;