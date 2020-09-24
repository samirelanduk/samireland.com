import { ApolloLink } from "apollo-link";
import { InMemoryCache } from "apollo-cache-inmemory";
import { createHttpLink } from "apollo-link-http";
import ApolloClient from "apollo-client";

export const isDevelopment = () => {
  /**
   * Returns true if app is running locally.
   */
  return !process.env.NODE_ENV || process.env.NODE_ENV === "development";
}


export const getApiLocation = () => {
  /**
   * Gets the URL of the API.
   */

  if (isDevelopment()) {
    return "http://localhost:8010/graphql";
  } else {
    return "https://api.samireland.com/graphql";
  }
}


export const makeClient = () => {
  /**
   * Creates an apollo client with automatic token insertion, and catchall
   * error handling.
   */

  const httpLink = createHttpLink({ uri: getApiLocation() });
  const link = ApolloLink.from([httpLink]);
  return new ApolloClient({link: link, cache: new InMemoryCache()});
}
