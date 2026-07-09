export async function getServerSideProps({ req, res }) {
  const host = req.headers["x-forwarded-host"] || req.headers.host;
  const origin = `${req.headers["x-forwarded-proto"] || "http"}://${host}`;
  const text = [
    "User-agent: *",
    "Content-Signal: ai-train=no, search=yes, ai-input=no",
    "Allow: /",
    "Disallow: /admin",
    "Disallow: /api",
    "",
    `Sitemap: ${origin}/sitemap.xml`,
    "",
  ].join("\n");

  res.setHeader("Content-Type", "text/plain");
  res.write(text);
  res.end();
  return { props: {} };
}

export default function Robots() {
  return null;
}
