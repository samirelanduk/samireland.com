import Project from "@/components/Project";
import Tags from "@/components/Tags";
import Head from "next/head";
import { useState } from "react";

export default function Projects({title, text, projects}) {

  const [selectedTags, setSelectedTags] = useState([]);

  const filteredProjects = selectedTags.length ? projects.filter(project => {
    return project.tags.some(tag => selectedTags.includes(tag));
  }) : projects;

  return (
    <main>
      <Head>
        <title>{title} - Sam Ireland</title>
      </Head>
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
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/projects`)
  const data = await res.json()

  return {
    props: {
      title: data.title,
      text: data.text,
      projects: data.projects,
    }
  }
}
