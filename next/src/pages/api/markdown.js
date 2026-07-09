import { parse } from "node-html-parser";
import { NodeHtmlMarkdown } from "node-html-markdown";

export default async function handler(req, res) {
  const page = await getHtml(req.query.path || "/");
  if (!page) return res.status(400).send("Invalid path");

  const document = parse(page.html);
  const header = getHeader(document);
  const body = getBody(document, req.query.path === "/");



  const markdown = `${header}\n\n${body}`;
  res.status(page.status);
  res.setHeader("Content-Type", "text/markdown; charset=utf-8");
  res.setHeader("x-markdown-tokens", Math.ceil(body.length / 4));
  res.setHeader("Vary", "Accept");
  res.send(markdown);
}

const getHtml = async (path) => {
  const base = `http://127.0.0.1:${process.env.PORT || 3000}`;
  let url;
  try {
    url = new URL(path, base);
  } catch {
    return null;
  }
  if (url.origin !== base) return null;
  const resp = await fetch(url, { headers: { Accept: "text/html" } });
  return { status: resp.status, html: await resp.text() };
}

const getHeader = document => {
  const title = document.querySelector("title")?.text;
  const description = document.querySelector("meta[name=description]")?.getAttribute("content") || "";
  const lines = [
    "---",
    `title: ${JSON.stringify(title)}`,
    `description: ${JSON.stringify(description)}`,
    "---",
  ];
  return lines.join("\n");
}

const getBody = (document, isRoot) => {
  const lines = [
    getH1(document),
    getIntro(document) || getP(document),
    getTime(document),
    getArticle(document),
    getH2Blocks(document),
    isRoot ? getHomeLinks(document) : "",
  ]
  return lines.filter(Boolean).join("\n\n");
}

const getH1 = document => {
  const h1 = document.querySelector("h1");
  return h1 ? NodeHtmlMarkdown.translate(h1.toString()) : "";
}

const getIntro = document => {
  const intro = document.querySelector(".intro")?.toString();
  return NodeHtmlMarkdown.translate(intro || "");
}

const getP = document => {
  const allP = document.querySelectorAll("p");
  if (allP.length === 1) return NodeHtmlMarkdown.translate(allP[0].toString());
  return ""
}

const getTime = document => {
  const allTime = document.querySelectorAll("time");
  if (allTime.length === 1) return NodeHtmlMarkdown.translate(allTime[0].toString());
  return ""
;}

const getArticle = document => {
  const article = document.querySelector("article");
  if (!article) return "";
  const prose = article.querySelector(".prose");
  if (!prose) return "";
  return NodeHtmlMarkdown.translate(prose.toString());
}

const getH2Blocks = document => {
  if (document.querySelector("article")) return "";
  const seen = new Set();
  const blocks = document.querySelectorAll("h2").reduce((blocks, h2) => {
    let block = h2;
    while (block.parentNode?.querySelectorAll("h2").length === 1) block = block.parentNode;
    if (!seen.has(block)) { seen.add(block); blocks.push(block); }
    return blocks;
  }, []);
  if (blocks.length === 0) return "";
  const seenTitles = new Set();
  const blocksAreLinks = blocks.every(block => block.querySelector("a") || block.tagName === "A");
  return blocks.map(block => {
    const h2 = block.querySelector("h2");
    if (seenTitles.has(h2.text)) return "";
    seenTitles.add(h2.text);
    const h2Line = NodeHtmlMarkdown.translate(h2.toString());
    const date = block.querySelector("time")?.toString();
    const dateLine = date ? NodeHtmlMarkdown.translate(date) : "";
    const paragraphs = block.querySelectorAll("p");
    const paragraphLines = paragraphs.map(paragraph => NodeHtmlMarkdown.translate(paragraph.toString()));
    let link = "";
    if (blocksAreLinks) {
      let a = block.querySelector("a")?.getAttribute("href");
      if (!a) a = block.getAttribute("href");
      link = a ? `[Link to content](${a})` : "";
    }
    return [
      h2Line,
      dateLine,
      paragraphLines.join("\n\n"),
      link,
    ].filter(Boolean).join("\n\n");
  }).join("\n\n");
}

const getHomeLinks = document => {
  const links = document.querySelectorAll("a").filter(link => link.textContent.trim());
  return links.map(link => `[${link.text}](${link.getAttribute("href")})`).join("\n\n");
}