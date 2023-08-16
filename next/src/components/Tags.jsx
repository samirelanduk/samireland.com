import React from "react";
import PropTypes from "prop-types";

const Tags = props => {

  const { projects, selectedTags, setSelectedTags } = props;

  const tags = {};
  for (let project of projects) {
    for (let tag of project.tags) {
      if (tag in tags) {
        tags[tag] += 1;
      } else {
        tags[tag] = 0;
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
    <div>
      {tagsList.map(tag => (
        <span
          key={tag}
          onClick={() => handleTagClick(tag)}
          className={`tag ${(selectedTags.includes(tag) || selectedTags.length === 0) ? "opacity-100" : "opacity-50"}`}
        >
          {tag}
        </span>
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