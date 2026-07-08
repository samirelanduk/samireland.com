import { fetchRemoteData } from "@/fetch";
import Head from "next/head";
import { useState, useEffect } from "react";
import CurrentlyReading from "@/components/CurrentlyReading";
import ReadingTimeline from "@/components/ReadingTimeline";

export default function Reading({title, text, meta, queues}) {

  const [timelineHeight, setTimelineHeight] = useState(250);

  useEffect(() => {
    const smallHeight = 225;
    const largeHeight = 250;
    const handleResize = () => {
      if (window.innerWidth < 640) {
        setTimelineHeight(smallHeight);
      } else {
        setTimelineHeight(largeHeight);
      }
    };
    window.addEventListener("resize", handleResize);
    handleResize();
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <main className="">
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


      <div className="flex flex-col justify-between gap-x-8 border-b border-slate-300 pb-5 mb-10 sm:pb-7 sm:mb-12 xl:mb-16 3xl:mb-20 xl:flex-row xl:items-start xl:gap-10 2xl:gap-16">
        <div className="">
          <h1 className="title">{title}</h1>
          <div dangerouslySetInnerHTML={{__html: text}} className="intro border-none mb-0 pb-0 max-w-none" />
        </div>
        <CurrentlyReading queues={queues} className="-mt-4 border-t border-slate-300 pt-6 xl:border-none xl:pt-0" />
      </div>


      <div style={{ height: timelineHeight * queues.length + 20 }}>
        <div
          className="absolute left-0 right-0 overflow-x-auto px-6 sm:px-10 md:px-12 lg:px-20 3xl:px-36 [direction:rtl]"
        >
          <div className="w-max pl-8 ml-8 [direction:ltr]">
            <ReadingTimeline queues={queues} vertical={false} timelineHeight={timelineHeight} pixelsPerDay={20} />
          </div>
        </div>
      </div>
    </main>
  )
}


export async function getStaticProps() {
  const data = await fetchRemoteData("reading", {
    title: "", text: "", queues: [], meta: {}
  });
  if (!data) return {notFound: true};
  return {
    props: {
      title: data.title,
      text: data.text,
      queues: data.queues,
      meta: data.meta
    }
  }
}
