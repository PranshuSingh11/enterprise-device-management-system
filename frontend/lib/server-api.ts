import { cookies } from "next/headers";
import { redirect } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function serverApiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token")?.value;

  const headers = new Headers(options?.headers);

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

if (response.status === 401) {
    redirect("/login");
  }

  if (!response.ok) {
  const error = new Error(
    `API request failed: ${response.status}`
  );

  Object.assign(error, {
    status: response.status,
  });

  throw error;
}

  return response.json();
}