export default async function handler(req, res) {
  if (!req.query.secret || req.query.secret !== process.env.REVALIDATE_TOKEN) {
    return res.status(401).json({ message: "Invalid token" })
  }
  try {
    console.log(new Date(), "Revalidating", req.query.path)
    await res.revalidate(req.query.path)
    console.log(new Date(), "Revalidated", req.query.path)
    return res.json({ revalidated: true })
  } catch (err) {
    return res.status(500).send("Error revalidating")
  }
}