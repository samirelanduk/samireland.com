import Project from "@/components/Project";
import Tags from "@/components/Tags";
import Head from "next/head";
import { useState } from "react";
import { fetchRemoteData } from "@/fetch";

export default function Projects({title, text, projects, meta}) {

  const [selectedTags, setSelectedTags] = useState([]);

  const filteredProjects = selectedTags.length ? projects.filter(project => {
    return project.tags.some(tag => selectedTags.includes(tag));
  }) : projects;

  return (
    <main>
      <Head>
        <title>{`${meta.title} - Sam Ireland`}</title>
        <meta name="description" content={meta.description} />
        <meta content="summary_large_image" name="twitter:card"/>
        <meta content="@samirelanduk" name="twitter:site"/>
        <meta content={meta.title} name="twitter:title"/>
        <meta content={meta.description} name="twitter:description"/>
        <meta content="https://samireland.com/images/social-card.png" name="twitter:image"/>
        <meta content="https://samireland.com/images/social-card.png" property="og:image"/>
        <meta property="og:title" content={meta.title} />
        <meta property="og:description" content={meta.description} />
      </Head>
      <h1>{title}</h1>
      <div dangerouslySetInnerHTML={{__html: text}} />
      <Tags projects={projects} selectedTags={selectedTags} setSelectedTags={setSelectedTags} />
      <div>
        {filteredProjects.map(project => (
          <Project key={project.name} project={project} />
        ))}
      </div>
    </main>
  )
}

export async function getStaticProps() {
  const data = await fetchRemoteData("projects", {
    title: "", text: "", projects: [], meta: {}
  });
  if (!data) return {notFound: true};
  return {
    props: {
      title: data.title,
      text: data.text,
      projects: data.projects,
      meta: data.meta
    }
  }
}
