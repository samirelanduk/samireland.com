import { fetchRemoteData } from "@/fetch";

const STATIC_PATHS = ["/", "/about", "/projects", "/writing", "/reading"];

export async function getServerSideProps({ req, res }) {
  const host = req.headers["x-forwarded-host"] || req.headers.host;
  const origin = `${req.headers["x-forwarded-proto"] || "http"}://${host}`;
  const writing = await fetchRemoteData("writing", { articles: [] });
  const reading = await fetchRemoteData("reading", { queues: [] });

  const paths = [...STATIC_PATHS];
  for (const article of writing?.articles || []) {
    paths.push(`/writing/${article.slug}`);
  }
  for (const queue of reading?.queues || []) {
    paths.push(`/reading/${queue.slug}`);
    for (const book of queue.books || []) {
      paths.push(`/reading/${queue.slug}/${book.slug}`);
    }
  }

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...paths.map(path => `  <url><loc>${origin}${path}</loc></url>`),
    "</urlset>",
  ].join("\n");

  res.setHeader("Content-Type", "application/xml");
  res.write(xml);
  res.end();
  return { props: {} };
}

export default function Sitemap() {
  return null;
}
