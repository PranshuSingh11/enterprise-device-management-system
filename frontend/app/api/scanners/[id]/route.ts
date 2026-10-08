import { NextResponse } from "next/server";

import { serverApiFetch } from "@/lib/server-api";

interface ScannerRouteProps {
  params: Promise<{
    id: string;
  }>;
}

export async function PUT(
  request: Request,
  { params }: ScannerRouteProps
) {
  const { id } = await params;

  try {
    const body = await request.json();

    const scanner = await serverApiFetch(
      `/api/v1/scanners/${id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    );

    return NextResponse.json(scanner);
  } catch (error) {
    console.error("Failed to update scanner:", error);

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
        detail: "Failed to update scanner",
      },
      {
        status: 500,
      }
    );
  }
}

export async function DELETE(
  request: Request,
  { params }: ScannerRouteProps
) {
  const { id } = await params;

  try {
    await serverApiFetch(`/api/v1/scanners/${id}`, {
      method: "DELETE",
    });

    return new NextResponse(null, {
      status: 204,
    });
  } catch (error) {
    console.error("Failed to delete scanner:", error);

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
        detail: "Failed to delete scanner",
      },
      {
        status: 500,
      }
    );
  }
}