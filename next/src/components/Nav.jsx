import React from "react";
import Link from "next/link"

const Nav = () => {

  const iconClass = "w-6 fill-red-500 fill-current hover:fill-current hover:fill-red-600 transition-colors";

  return (
    <nav className="flex flex-col flex-shrink-0 gap-8 px-6 py-8">
      <Link href="/">
        <img src="/images/home.svg" alt="Home" className={iconClass} />
      </Link>
      <Link href="/projects/">
        <img src="/images/projects.svg" alt="Projects" className={iconClass} />
      </Link>
      <Link href="/about/">
        <img src="/images/timeline.svg" alt="About" className={iconClass} />
      </Link>
      <Link href="/writing/">
        <img src="/images/writing.svg" alt="Writing" className={iconClass} />
      </Link>
    </nav>
  );
};

Nav.propTypes = {
  
};

export default Nav;