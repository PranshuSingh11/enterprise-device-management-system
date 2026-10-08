import { NextResponse } from "next/server";

import { serverApiFetch } from "@/lib/server-api";

export async function POST(request: Request) {
  try {
    const body = await request.json();

    const scanner = await serverApiFetch("/api/v1/scanners", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    return NextResponse.json(scanner, {
      status: 201,
    });
  } catch (error) {
    console.error("Failed to create scanner:", error);

    if (
      error instanceof Error &&
      "status" in error &&
      typeof error.status === "number"
    ) {
      return NextResponse.json(
        {
          detail: error.message,
        },
        {
          status: error.status,
        }
      );
    }

    return NextResponse.json(
      {
        detail: "Failed to create scanner",
      },
      {
        status: 500,
      }
    );
  }
}