import Sidebar from "@/components/layout/Sidebar";
import Header from "@/components/layout/Header"
import type { ReactNode } from "react";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

interface DashboardLayoutProps {
  children: ReactNode;
}

export default async function DashboardLayout({
  children,
}: DashboardLayoutProps) {

  const cookieStore = await cookies();
  const token = cookieStore.get("access_token");

  if (!token) {
    redirect("/login");
  }
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />

      <main className="flex-1">
        <Header />

        <section className="p-6">
          {children}
        </section>
      </main>
    </div>
  );
}