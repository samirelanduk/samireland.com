import Link from "next/link"
import { useEffect, useRef } from "react";

const Nav = () => {

  const ref = useRef();

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
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav ref={ref} className="flex fixed bg-gradient-to-r from-background-2/0 to-background-3/0 top-0 left-0 w-full transition duration-500 justify-between h-12 items-center px-4 sm:px-6 md:px-10 xl:px-14 xl:h-14 3xl:h-16 3xl:px-18">
      <Link href="/" className="text-sm font-semibold text-slate-800 subtle-link sm:text-base md:text-lg xl:text-xl 3xl:text-2xl">
        Sam Ireland
      </Link>
      <div className="flex items-center h-full gap-3 text-xs text-slate-600 sm:text-sm sm:gap-3.5 md:text-base md:gap-4 lg:gap-6 xl:gap-8 xl:text-lg 3xl:text-xl 3xl:gap-10">
        <Link href="/projects/" className="subtle-link">
          Projects
        </Link>
        <Link href="/about/" className="subtle-link">
          About
        </Link>
        <Link href="/writing/" className="subtle-link">
          Writing
        </Link>
      </div>
    </nav>
  )
};

Nav.propTypes = {
  
};

export default Nav;