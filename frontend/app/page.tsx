import { apiFetch } from "@/lib/api";

export default async function Home() {
  const data = await apiFetch<{ status: string }>("/api/v1/health");

  return (
    <main>
      <h1>Enterprise Device Management</h1>
      <p>Backend status: {data.status}</p>
    </main>
  );
}