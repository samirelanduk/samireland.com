import React from "react";
import Base from "./Base";
import LandingSection from "../components/LandingSection";

const HomePage = () => {
  return (
    <Base className="home-page">
      <LandingSection />
    </Base>
  );
};

HomePage.propTypes = {
  
};

export default HomePage;