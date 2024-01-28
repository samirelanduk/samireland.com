import React from "react";
import PropTypes from "prop-types";

const Tags = props => {

  const { projects, selectedTags, setSelectedTags } = props;

  const tags = {};
  const tagColors = {};
  for (let project of projects) {
    for (let tag of project.tags) {
      tagColors[tag.name] = tag.color;
      if (tag.name in tags) {
        tags[tag.name] += 1;
      } else {
        tags[tag.name] = 0;
      }
    }
  }

  const tagsList = Object.entries(tags).sort((a, b) => b[1] - a[1]).map(tag => tag[0]);

  const handleTagClick = tag => {
    if (selectedTags.includes(tag)) {
      setSelectedTags(selectedTags.filter(t => t !== tag));
    } else {
      setSelectedTags([...selectedTags, tag]);
    }
  }

  return (
    <div className={`flex flex-wrap gap-2 bg-green-sidc-faint bg-opacity-50 py-3 px-4 w-fit mx-auto text-slate-900 rounded-3xl justify-center font-semibold sm:gap-x-4 sm:gap-y-2 sm:py-4 sm:px-6 md:text-lg xl:gap-x-5 3xl:gap-x-6 ${props.className || ""}`}>
      {tagsList.map(tag => (
        <div
          key={tag}
          onClick={() => handleTagClick(tag)}
          className={`cursor-pointer transition-opacity duration-200 ${(selectedTags.includes(tag) || selectedTags.length === 0) ? "opacity-100" : "opacity-50"}`}
        >
          #{tag}
        </div>
      ))}
    </div>
  );
};

Tags.propTypes = {
  projects: PropTypes.array.isRequired,
  selectedTags: PropTypes.array.isRequired,
  setSelectedTags: PropTypes.func.isRequired
};

export default Tags;