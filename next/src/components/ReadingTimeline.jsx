import React, { useLayoutEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import BookPreview from "@/components/BookPreview";
import { bookCategoryColor } from "@/utils";

const MS_DAY = 86400000;
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

const parseDateParts = value => {
  if (value instanceof Date) {
    return { y: value.getUTCFullYear(), m: value.getUTCMonth(), d: value.getUTCDate() };
  }
  const [y, m, d] = String(value).slice(0, 10).split("-").map(Number);
  return { y, m: m - 1, d };
};

const midnightUtc = value => {
  const { y, m, d } = parseDateParts(value);
  return Date.UTC(y, m, d);
};

const noonUtc = value => {
  const { y, m, d } = parseDateParts(value);
  return Date.UTC(y, m, d, 12);
};

const msToPixels = (ms, pixelsPerDay) => ms / MS_DAY * pixelsPerDay;


const relaxedLinkStarts = slots => {
  let offset = 0;
  const offsets = [];
  const targets = slots.map(slot => {
    offsets.push(offset);
    const target = slot.ideal - offset;
    offset += slot.size;
    return target;
  });
  const clusters = [];
  for (const target of targets) {
    let cluster = { sum: target, count: 1 };
    while (clusters.length && clusters[clusters.length - 1].sum / clusters[clusters.length - 1].count >= cluster.sum / cluster.count) {
      const previous = clusters.pop();
      cluster = { sum: previous.sum + cluster.sum, count: previous.count + cluster.count };
    }
    clusters.push(cluster);
  }
  const positions = [];
  for (const cluster of clusters) {
    const value = cluster.sum / cluster.count;
    for (let c = 0; c < cluster.count; c++) positions.push(value);
  }
  let minimum = 0;
  return slots.map((slot, i) => {
    let position = Math.max(positions[i] + offsets[i], minimum);
    if (Math.abs(position - slot.ideal) < 1e-6) position = slot.ideal;
    minimum = position + slot.size;
    return position;
  });
};

const computeBooks = (queues, { vertical, pixelsPerDay, now, timelineOrigin, timelineSpan, dateWidth, dateHeight, timelineWidth, queueTimelineHeight, timelinePadding, linkHeight, linkWidth, measuredWidths }) => {
  const books = [];
  let bookIndex = 0;
  for (let q = 0; q < queues.length; q++) {
    const queue = queues[q];
    const queueBooks = [...queue.books].sort((a, b) => noonUtc(b.started) - noonUtc(a.started));
    const entries = queueBooks.map(book => {
      const endTime = book.finished ? noonUtc(book.finished) : now;
      const endFromBottom = msToPixels(endTime - timelineOrigin, pixelsPerDay);
      const startFromBottom = msToPixels(noonUtc(book.started) - timelineOrigin, pixelsPerDay);
      const dimension = vertical ? linkHeight : (measuredWidths?.[bookIndex] ?? linkWidth);
      return {
        book: book,
        start: timelineSpan - endFromBottom,
        size: endFromBottom - startFromBottom - 1,
        dimension: dimension,
        index: bookIndex++,
      };
    });
    const linkStarts = relaxedLinkStarts(entries.map(entry => ({
      ideal: entry.start,
      size: entry.dimension + (vertical ? 4 : 12),
    })));
    entries.forEach((entry, e) => {
      books.push({
        start: entry.start,
        linkStart: linkStarts[e],
        size: entry.size,
        offset: (vertical ? dateWidth : dateHeight) + (q * (vertical ? timelineWidth : queueTimelineHeight)) + timelinePadding,
        completed: Boolean(entry.book.finished),
        href: `/reading/${queue.slug}/${entry.book.slug}`,
        data: entry.book,
        queue: queue,
        index: entry.index,
      });
    });
  }
  return books;
};

const ReadingTimeline = props => {

  const { queues, vertical=true, pixelsPerDay=10, timelineHeight=100, className="" } = props;

  const DATE_WIDTH = 30;
  const DATE_HEIGHT = 20;
  const TIMELINE_WIDTH = 700;
  const TIMELINE_HEIGHT = timelineHeight;
  const TIMELINE_PADDING = vertical ? 25 : 10;
  const BLOCK_WIDTH = 60;
  const LINK_HEIGHT = 75;
  const LINK_WIDTH = 275;
  const LINK_MARGIN = 15;

  const now = noonUtc(new Date());
  const [measuredWidths, setMeasuredWidths] = useState(null);
  const previewRefs = useRef([]);


  const timelineOrigin = Math.min(
    ...queues.flatMap(queue => queue.books.map(book => midnightUtc(book.started))),
  );

  const timelineSpan = msToPixels(now - timelineOrigin, pixelsPerDay);

  const years = [];
  const yearLabels = [];
  const months = [];
  const monthLabels = [];
  for (let t = timelineOrigin + MS_DAY; t < now; t += MS_DAY) {
    const d = new Date(t);
    if (d.getUTCDate() !== 1) continue;
    if (d.getUTCMonth() === 0) {
      years.push(t);
      yearLabels.push(`${d.getUTCFullYear()}`);
    } else {
      months.push(t);
      monthLabels.push(MONTHS[d.getUTCMonth()]);
    }
  }

  const toCoordinate = timestamp => msToPixels(timestamp - timelineOrigin, pixelsPerDay);
  const yearCoordinates = years.map(toCoordinate);
  const monthCoordinates = months.map(toCoordinate);

  let height = timelineSpan;
  let width = DATE_WIDTH + (TIMELINE_WIDTH * queues.length);
  if (!vertical) {
    width = timelineSpan;
    height = DATE_HEIGHT + (TIMELINE_HEIGHT * queues.length);
  }

  const books = useMemo(
    () => computeBooks(queues, {
      vertical,
      pixelsPerDay,
      now,
      timelineOrigin,
      timelineSpan,
      dateWidth: DATE_WIDTH,
      dateHeight: DATE_HEIGHT,
      timelineWidth: TIMELINE_WIDTH,
      queueTimelineHeight: TIMELINE_HEIGHT,
      timelinePadding: TIMELINE_PADDING,
      linkHeight: LINK_HEIGHT,
      linkWidth: LINK_WIDTH,
      measuredWidths: vertical ? null : measuredWidths,
    }),
    [queues, vertical, pixelsPerDay, now, timelineOrigin, timelineSpan, measuredWidths, TIMELINE_HEIGHT, TIMELINE_PADDING],
  );

  useLayoutEffect(() => {
    if (vertical) return;

    const measure = () => {
      const widths = previewRefs.current.map(el => el ? el.getBoundingClientRect().width : LINK_WIDTH);
      setMeasuredWidths(previous => {
        const changed = widths.some((width, i) => Math.abs(width - (previous?.[i] ?? LINK_WIDTH)) > 1);
        return changed ? widths : previous;
      });
    };

    measure();
    const observer = new ResizeObserver(measure);
    for (const el of previewRefs.current) {
      if (el) observer.observe(el);
    }
    return () => observer.disconnect();
  }, [vertical, queues]);

  // Line classes
  const labelClass = "text-xs uppercase tracking-wide text-slate-400 font-semibold absolute";
  const lineClass = `absolute bg-slate-300 opacity-50 ${vertical ? "right-0" : "top-4 bottom-0"}`;
  const yearLineClass = `${lineClass} ${vertical ? "h-[2px]" : "w-[2px]"}`;
  const monthLineClass = `${lineClass} ${vertical ? "h-px" : "w-px"}`;
  const timelineLineClass = `absolute bg-slate-300 ${vertical ? "w-px h-full" : "h-px w-full"}`;
  const blockClass = `absolute bg-opacity-90 transition-all duration-300 group-hover:bg-opacity-100 ${vertical ? "group-hover:scale-x-110" : "group-hover:scale-y-110"}`;
  const completedBlockClass = `${blockClass} rounded-xl`;
  const uncompletedBlockClass = `${blockClass} ${vertical ? "rounded-b-xl" : "rounded-l-xl"}`;


  return (
    <div style={{ height, width }} className={`${className} relative`}>
      {yearCoordinates.map((coordinate, y) => (
        <React.Fragment key={y}>
          <div
            className={yearLineClass}
            style={{
              [vertical ? "bottom" : "left"]: coordinate,
              [vertical ? "left" : "top"]: (vertical ? DATE_WIDTH : DATE_HEIGHT),
            }}
          />
          <div
            className={labelClass}
            style={{ [vertical ? "bottom" : "left"]: coordinate - (vertical ? 6 : 14) }}
          >
            {yearLabels[y]}
          </div>
        </React.Fragment>
      ))}
      {monthCoordinates.map((coordinate, m) => (
        <React.Fragment key={m}>
          <div
            className={monthLineClass}
            style={{
              [vertical ? "bottom" : "left"]: coordinate,
              [vertical ? "left" : "top"]: (vertical ? DATE_WIDTH : DATE_HEIGHT),
            }}
          />
          <div
            className={labelClass}
            style={{ [vertical ? "bottom" : "left"]: coordinate - (vertical ? 6 : 14) }}
          >
            {monthLabels[m]}
          </div>
        </React.Fragment>
      ))}
      {!vertical && queues.map((queue, q) => {
        if (!queue.title) return null;
        const queueBooks = books.filter(book => book.queue === queue);
        const reach = queueBooks.length ? Math.max(...queueBooks.map(book => book.start + book.size)) : 0;
        return (
          <div
            key={q}
            className="relative h-0 ml-auto"
            style={{
              width: reach,
              top: DATE_HEIGHT + (q * TIMELINE_HEIGHT) + TIMELINE_PADDING + LINK_MARGIN + (BLOCK_WIDTH * 2) + TIMELINE_PADDING + 12,
            }}
          >
            <Link
              href={`/reading/${queue.slug}`}
              className="subtle-link group/label sticky right-0 z-20 flex w-max ml-auto items-center gap-1.5 whitespace-nowrap text-sm font-semibold text-slate-500 sm:text-base"
            >
              {queue.title}
              <span className="transition-transform duration-300 group-hover/label:translate-x-1">→</span>
            </Link>
          </div>
        );
      })}
      {queues.map((queue, q) => (
        <div
          key={q}
          className={timelineLineClass}
          style={{ [vertical ? "left" : "top"]: (q * (vertical ? TIMELINE_WIDTH : TIMELINE_HEIGHT)) + (vertical ? DATE_WIDTH : DATE_HEIGHT) + TIMELINE_PADDING + (vertical ? 0 : LINK_HEIGHT + TIMELINE_PADDING) + (BLOCK_WIDTH / 2)}}//  }}
        />
      ))}
      {books.map((book, b) => (
        <div key={b} className="group">
          <Link
            href={book.href}
            className={`${book.completed ? completedBlockClass : uncompletedBlockClass} ${bookCategoryColor(book.data.category).blockColor}`}
            style={{
              [vertical ? "width" : "height"]: BLOCK_WIDTH,
              [vertical ? "height" : "width"]: book.size,
              [vertical ? "top" : "right"]: book.start,
              [vertical ? "left" : "top"]: book.offset + (vertical ? 0 : LINK_MARGIN + BLOCK_WIDTH + TIMELINE_PADDING),
            }}
          />
          {book.start !== book.linkStart && (
            <svg
              className={`absolute z-0 ${bookCategoryColor(book.data.category).textColor}`}
              style={{
                [vertical ? "width" : "height"]: (BLOCK_WIDTH / 2) + (vertical ? (LINK_MARGIN + (LINK_HEIGHT / 3)) : (LINK_HEIGHT / 2 + LINK_MARGIN)),
                [vertical ? "height" : "width"]: Math.abs(book.linkStart - book.start),
                [vertical ? "top" : "right"]: Math.min(book.start, book.linkStart),
                [vertical ? "left" : "top"]: book.offset + (vertical ? (BLOCK_WIDTH / 2) : (LINK_HEIGHT / 2)),
              }}
            >
              <line
                x1="0"
                y1={book.linkStart > book.start ? "0" : "100%"}
                x2="100%"
                y2={book.linkStart > book.start ? "100%" : "0"}
                stroke="currentColor"
                strokeWidth="1"
              />
            </svg>
          )}
          <div
            ref={el => { previewRefs.current[book.index] = el; }}
            className="absolute z-10 w-max"
            style={{
              [vertical ? "top" : "right"]: book.linkStart,
              [vertical ? "left" : "top"]: book.offset + (vertical ? LINK_MARGIN + BLOCK_WIDTH : 0),
            }}
          >
            <BookPreview
              book={book.data}
              queue={book.queue}
              bookHeight={LINK_HEIGHT}
              reversed={!vertical}
              compress={!vertical}
              className=""
              style={vertical ? { height: LINK_HEIGHT } : undefined}
            />
          </div>
        </div>
      ))}


    </div>
  )

}

export default ReadingTimeline;