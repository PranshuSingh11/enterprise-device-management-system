import { NextResponse } from "next/server";

import { serverApiFetch } from "@/lib/server-api";

import type { BranchListResponse } from "@/types/branch";

export async function GET() {
  try {
    const branches = await serverApiFetch<BranchListResponse>(
      "/api/v1/branches?page=1&page_size=100"
    );

    return NextResponse.json(branches);
  } catch (error) {
    console.error("Failed to fetch branches:", error);

    return NextResponse.json(
      {
        detail: "Failed to fetch branches",
      },
      {
        status: 500,
      }
    );
  }
}


export async function POST(request: Request) {
  try {
    const body = await request.json();

    const branch = await serverApiFetch(
      "/api/v1/branches",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    return NextResponse.json(branch, {
      status: 201,
    });
  } catch (error) {
    console.error(
      "Failed to create branch:",
      error
    );

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
        detail: "Failed to create branch",
      },
      {
        status: 500,
      }
    );
  }
}
