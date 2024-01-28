import PropTypes from "prop-types";
import GithubIcon from "@/images/github.svg?react"
import WebIcon from "@/images/web.svg?react"

const Project = props => {

  const { project } = props;

  const isFeatured = Boolean(project.featured_overview);

  const linkClass = `fill-green-sidc-faint transition duration-500 hover:fill-green-sidc ${isFeatured ? "w-6 h-6 xl:w-7 xl:h-7" : "w-5 h-5"}`;

  return (
    <div className={`flex flex-col justify-center items-center gap-2 px-4 max-w-sm mx-auto sm:max-w-none sm:mx-0 ${isFeatured ? "gap-4 border rounded py-6 items-start relative border-green-sidc-faint sm:px-6 md:justify-start md:flex-row md:gap-4 lg:gap-8 lg:py-8 lg:px-7 xl:py-10 xl:gap-10 md:items-start xl:px-8" : "sm:items-start"} ${props.className || ""}`}>
      {isFeatured && (
        <div className="absolute text-xs bg-green-sidc font-bold text-white -top-2.5 left-6 px-1.5 py-0.5 rounded lg:left-7 xl:left-8">FEATURED</div> 
      )}

      <img
        src={`${process.env.NEXT_PUBLIC_MEDIA_URL}/${project.image}`}
        className={`object-contain max-w-full rounded-lg ${isFeatured ? "w-44 h-44 md:w-56 md:h-56 lg:w-64 lg:h-64 xl:w-72 xl:h-72" : "w-40 h-40"}`}
        alt={project.name}
      />

      <div className="flex-grow max-w-5xl">

        <h2 className={`font-serif flex flex-wrap justify-center whitespace-nowrap items-center gap-3 font-semibold mb-2 text-center ${isFeatured ? "text-3xl md:justify-start xl:text-4xl" : "text-2xl sm:justify-start"}`}>
          {project.name}
          <div className={`flex justify-center sm:justify-start ${isFeatured ? "gap-2.5" : "gap-2"}`}>
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
        </h2>

        {isFeatured && (
          <div
            dangerouslySetInnerHTML={{__html: project.featured_overview}}
            className="prose text-center mx-auto prose-p:my-1.5 sm:text-left sm:mx-0 lg:prose-lg lg:max-w-none xl:prose-xl xl:max-w-none"
          /> 
        )}

        <div
          dangerouslySetInnerHTML={{__html: project.description}}
          className="prose-sm w-full text-center mb-4 mx-auto prose-p:my-1.5 sm:text-left sm:mx-0 xl:prose xl:max-w-none"
        />

        <div className={`flex flex-wrap gap-x-2 gap-y-0.5 justify-center font-semibold sm:justify-start text-slate-600  ${isFeatured ? "text-sm sm:text-base md:text-lg" : "text-xs sm:text-sm md:text-base"}`}>
          {project.tags.map(tag => (
            <div key={tag.name}>#{tag.name}</div>
          ))}
        </div>
      </div>
    </div>
  );
};

Project.propTypes = {
  project: PropTypes.object.isRequired,
};

export default Project;