import { cookies } from "next/headers";
import { redirect } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function serverApiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token")?.value;

  if (!token) {
    redirect("/login");
  }

  const headers = new Headers(options?.headers);

  headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    redirect("/login");
  }

  if (!response.ok) {
    let detail = `API request failed: ${response.status}`;

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        detail = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    const error = new Error(detail);

    Object.assign(error, {
      status: response.status,
    });

    throw error;
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}