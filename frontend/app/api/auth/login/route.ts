import { NextResponse } from "next/server";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function POST(request: Request) {
  const body = await request.json();

  const formData = new URLSearchParams();

  formData.append("username", body.username);
  formData.append("password", body.password);

  const response = await fetch(`${API_URL}/api/v1/users/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  });

  if (!response.ok) {
    return NextResponse.json(
      { detail: "Invalid username or password" },
      { status: response.status }
    );
  }

  const data = await response.json();

  const responseObject = NextResponse.json({
    message: "Login successful",
  });

  responseObject.cookies.set("access_token", data.access_token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    path: "/",
  });

  return responseObject;
}