import Project from "@/components/Project";
import Head from "next/head";

export default function Projects({title, text, projects}) {
  return (
    <main>
      <Head>
        <title>{title} - Sam Ireland</title>
      </Head>
      <div dangerouslySetInnerHTML={{__html: text}} />
      <div>
        {projects.map(project => (
          <Project key={project.id} project={project} />
        ))}
      </div>
    </main>
  )
}

export async function getStaticProps() {
  const res = await fetch(`${process.env.API_URL}/projects`)
  const data = await res.json()

  return {
    props: {
      title: data.title,
      text: data.text,
      projects: data.projects,
    }
  }
}
