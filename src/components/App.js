import React from "react";
import { Switch, Route } from "react-router";
import { BrowserRouter } from "react-router-dom";
import { ApolloProvider } from "@apollo/react-hooks";
import { makeClient } from "../api";
import HomePage from "../pages/HomePage";
import AboutPage from "../pages/AboutPage";
import ProjectsPage from "../pages/ProjectsPage";

export default () => {  

  const client = makeClient();

  return (
    <ApolloProvider client={client}>
      <BrowserRouter> 
        <Switch>
          <Route path="/" exact>
            <HomePage />
          </Route>
          <Route path="/about/" exact>
            <AboutPage />
          </Route>
          <Route path="/projects/" exact>
            <ProjectsPage />
          </Route>
        </Switch>
      </BrowserRouter>
    </ApolloProvider>
  );
}
