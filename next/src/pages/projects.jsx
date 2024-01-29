import React from "react";
import Project from "@/components/Project";
import Tags from "@/components/Tags";
import Head from "next/head";
import { useState } from "react";
import { fetchRemoteData } from "@/fetch";

export default function Projects({title, text, projects, meta}) {

  const [selectedTags, setSelectedTags] = useState([]);

  const filteredProjects = selectedTags.length ? projects.filter(project => {
    return project.tags.some(tag => selectedTags.includes(tag.name));
  }) : projects;

  const makeProjectRows = (projects, columnCount) => {
    const featuredProjects = projects.filter(project => project.featured_overview);
    const otherProjects = projects.filter(project => !project.featured_overview);
    const otherRows = otherProjects.reduce((acc, project, index) => {
      if (index % columnCount === 0) acc.push([project]);
      else acc[acc.length - 1].push(project);
      return acc;
    }, []);
    const featureRowCount = featuredProjects.length >= otherRows.length ? 2 : 1;
    const rows = [];
    while (featuredProjects.length || otherRows.length) {
      for (let i = 0; i < featureRowCount; i++) {
        if (featuredProjects.length) {
          rows.push([featuredProjects.shift()]);
        }
      }
      if (otherRows.length) {
        rows.push(otherRows.shift());
      }
    }
    return rows;
  }

  const rowsOneColumn = makeProjectRows(filteredProjects, 1);
  const rowsTwoColumns = makeProjectRows(filteredProjects, 2);
  const rowsThreeColumns = makeProjectRows(filteredProjects, 3);
  const rowsFourColumns = makeProjectRows(filteredProjects, 4);

  const rowClass = "gap-x-6 md:gap-x-12 lg:gap-x-4 xl:gap-x-10";

  return (
    <main className="max-w-[100rem] mx-auto">
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
      <h1 className="title">{title}</h1>
      <div dangerouslySetInnerHTML={{__html: text}} className="intro" />
      <Tags
        projects={projects}
        selectedTags={selectedTags}
        setSelectedTags={setSelectedTags}
        className="mb-8 sm:mb-14"
      />

      <div className="flex flex-col gap-y-16 xs:gap-y-20">
        {rowsOneColumn.map((row, index) => (
          <div key={index} className="grid grid-cols-1 sm:hidden">
            {row.map(project => (
              <Project key={project.name} project={project} />
            ))}
          </div>
        ))}
        {rowsTwoColumns.map((row, index) => (
          <div key={index} className={`${row[0].featured_overview ? "grid-cols-1" : "grid-cols-2"} ${rowClass} hidden sm:grid lg:hidden`}>
            {row.map(project => (
              <Project key={project.name} project={project} />
            ))}
          </div>
        ))}
        {rowsThreeColumns.map((row, index) => (
          <div key={index} className={`${row[0].featured_overview ? "grid-cols-1" : "grid-cols-3"} ${rowClass} hidden lg:grid 2xl:hidden`}>
            {row.map(project => (
              <Project key={project.name} project={project} />
            ))}
          </div>
        ))}
        {rowsFourColumns.map((row, index) => (
          <div key={index} className={`${row[0].featured_overview ? "grid-cols-1" : "grid-cols-4"} ${rowClass} hidden 2xl:grid`}>
            {row.map(project => (
              <Project key={project.name} project={project} />
            ))}
          </div>
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
