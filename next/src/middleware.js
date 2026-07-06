import { NextResponse } from "next/server";

export function middleware(request) {
  const accept = request.headers.get("accept") || "";

  if (request.method === "GET" && accept.includes("text/markdown")) {
    const url = request.nextUrl.clone();
    url.pathname = "/api/markdown";
    url.search = `?path=${encodeURIComponent(request.nextUrl.pathname)}`;
    return NextResponse.rewrite(url);
  }

  const response = NextResponse.next();
  response.headers.set("Vary", "Accept");
  return response;
}

export const config = {
  matcher: ["/((?!api|_next|images|.*\\..*).*)"],
};
