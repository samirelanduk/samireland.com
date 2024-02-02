import Link from "next/link"
import { useEffect, useRef, useState } from "react";

const Nav = () => {

  const ref = useRef();

  const [path, setPath] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    setPath(window.location.pathname);
  });

  useEffect(() => {
    const handleScroll = () => {
      const nav = ref.current;
      const fromTranslucent = "from-background-2/80";
      const fromInvisible = "from-background-2/0";
      const toTranslucent = "to-background-3/80";
      const toInvisible = "to-background-3/0";
      if (window.scrollY > 0) {
        if (nav.classList.contains(fromInvisible)) nav.classList.remove(fromInvisible);
        if (nav.classList.contains(toInvisible)) nav.classList.remove(toInvisible);
        if (!nav.classList.contains(fromTranslucent)) nav.classList.add(fromTranslucent);
        if (!nav.classList.contains(toTranslucent)) nav.classList.add(toTranslucent);
      } else {
        if (nav.classList.contains(fromTranslucent)) nav.classList.remove(fromTranslucent);
        if (nav.classList.contains(toTranslucent)) nav.classList.remove(toTranslucent);
        if (!nav.classList.contains(fromInvisible)) nav.classList.add(fromInvisible);
        if (!nav.classList.contains(toInvisible)) nav.classList.add(toInvisible);
      }
    }
    handleScroll();
    const handleResize = () => setMenuOpen(false);
    window.addEventListener("scroll", handleScroll);
    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("scroll", handleScroll);
      window.removeEventListener("resize", handleResize);
    }
  }, []);

  const isWriting = path.startsWith("/writing");
  const isProjects = path === "/projects";
  const isAbout = path === "/about";

  const lineClass = "absolute -bottom-0.5 left-0 w-full h-0.5 bg-green-sidc/70 xs:h-1 xs:-bottom-1";
  const linkClass = "xs:subtle-link relative";

  const menuClass = "h-1 rounded w-5 transition-width duration-500 ";

  return (
    <nav ref={ref} className="flex fixed z-50 bg-gradient-to-r from-background-2 border- to-background-3 top-0 left-0 w-full transition duration-500 justify-between h-12 items-center px-6 sm:px-10 md:px-12 lg:px-20 xl:h-14 3xl:h-16 3xl:px-20">
      <Link href="/" className="text-base font-semibold text-slate-800 subtle-link xs:text-lg md:text-xl xl:text-2xl 3xl:text-3xl">
        Sam Ireland
      </Link>
      <div className="flex relative z-50 flex-col gap-1 items-end group cursor-pointer xs:hidden" onClick={() => setMenuOpen(!menuOpen)}>
        <div className={`${menuClass} ${menuOpen ? "bg-white w-7" : "bg-green-sidc w-5 group-hover:w-6" } `} />
        <div className={`${menuClass} ${menuOpen ? "bg-white w-5" : "bg-green-sidc w-6 group-hover:w-7" } `} />
        <div className={`${menuClass} ${menuOpen ? "bg-white w-6" : "bg-green-sidc w-7 group-hover:w-5" } `} />
      </div>
      <div
        className={`bg-green-sidc pt-20 gap-y-6 fixed w-full transition-[left] duration-100 ${menuOpen ? "left-0" : "left-full"} right-0 top-0 flex flex-col text-white text-3xl items-center h-full gap-3 xs:static xs:pt-0 xs:w-fit xs:flex-row xs:bg-inherit xs:font-semibold xs:text-slate-600 xl:text-slate-600 xs:text-base xs:gap-3.5 sm:gap-6 lg:gap-7 xl:gap-8 3xl:gap-10 3xl:text-lg`}
        onClick={() => setMenuOpen(false)}
      >
        <Link href="/about/" className={linkClass}>
          About
          {isAbout && <div className={lineClass} />}
        </Link>
        <Link href="/projects/" className={linkClass}>
          Projects
          {isProjects && <div className={lineClass} />}
        </Link>
        <Link href="/writing/" className={linkClass}>
          Writing
          {isWriting && <div className={lineClass} />}
        </Link>
      </div>
    </nav>
  )
};

Nav.propTypes = {
  
};

export default Nav;