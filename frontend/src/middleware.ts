import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Protected path prefixes
const PROTECTED_PATHS = ["/chat", "/documents", "/search", "/settings"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const isProtected = PROTECTED_PATHS.some((path) => pathname.startsWith(path));
  const token = request.cookies.get("access_token")?.value;

  if (isProtected && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Redirect authenticated users away from /login or /signup
  if ((pathname === "/login" || pathname === "/signup") && token) {
    return NextResponse.redirect(new URL("/chat", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/chat/:path*",
    "/documents/:path*",
    "/search/:path*",
    "/settings/:path*",
    "/login",
    "/signup",
  ],
};
