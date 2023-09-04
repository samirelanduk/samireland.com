import React, { useEffect, useState } from "react";
import PropTypes from "prop-types";
import {
  FacebookShareButton,
  LinkedinShareButton,
  TwitterShareButton,
  TwitterIcon,
  FacebookIcon,
  LinkedinIcon
} from "react-share";

const SocialShare = props => {

  const { title } = props;

  const [url, setUrl] = useState("");

  useEffect(() => {
    setUrl(window.location.href);
  }, []);

  return (
    <div>
      <div>Share on:</div>
      <TwitterShareButton url={url} title={title}>
        <TwitterIcon size={24} round={true} />
      </TwitterShareButton>
      <FacebookShareButton url={url} quote={title}>
        <FacebookIcon size={24} round={true} />
      </FacebookShareButton>
      <LinkedinShareButton url={url} title={title}>
        <LinkedinIcon size={24} round={true} />
      </LinkedinShareButton>
    </div>
  );
};

SocialShare.propTypes = {
  title: PropTypes.string.isRequired,
};

export default SocialShare;