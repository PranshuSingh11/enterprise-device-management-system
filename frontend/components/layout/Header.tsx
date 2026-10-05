"use client";

import { useRouter } from "next/navigation";

export default function Header() {
  const router = useRouter();

  async function handleLogout() {
    await fetch("/api/auth/logout", {
      method: "POST",
    });

    router.push("/login");
    router.refresh();
  }

  return (
    <header className="h-16 border-b bg-white">
      <div className="flex h-full items-center justify-between px-6">
        <h2 className="text-sm font-medium text-gray-700">
          Device Management
        </h2>

        <button
          onClick={handleLogout}
          className="text-sm font-medium text-gray-500 hover:text-gray-900"
        >
          Logout
        </button>
      </div>
    </header>
  );
}