import { NextResponse } from "next/server";

import { serverApiFetch } from "@/lib/server-api";

import type { BranchListResponse } from "@/types/branch";

interface BranchRouteProps {
  params: Promise<{ id: string }>;
}


export async function PUT(
  request: Request,
  { params }: BranchRouteProps
) {
  const { id } = await params;

  try {
    const body = await request.json();

    const branch = await serverApiFetch(
      `/api/v1/branches/${id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    return NextResponse.json(branch);
  } catch (error) {
    console.error("Failed to update branch:", error);

    if (
      error instanceof Error &&
      "status" in error &&
      typeof error.status === "number"
    ) {
      return NextResponse.json(
        { detail: error.message },
        { status: error.status }
      );
    }

    return NextResponse.json(
      { detail: "Failed to update branch" },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: Request,
  { params }: BranchRouteProps
) {
  const { id } = await params;

  try {
    await serverApiFetch(`/api/v1/branches/${id}`, {
      method: "DELETE",
    });

    return new NextResponse(null, { status: 204 });
  } catch (error) {
    console.error("Failed to delete branch:", error);

    if (
      error instanceof Error &&
      "status" in error &&
      typeof error.status === "number"
    ) {
      return NextResponse.json(
        { detail: error.message },
        { status: error.status }
      );
    }

    return NextResponse.json(
      { detail: "Failed to delete branch" },
      { status: 500 }
    );
  }
}