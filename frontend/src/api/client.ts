// Thin fetch wrapper. Surfaces FastAPI error bodies ({"detail": "..."}) as Error
// messages so components can show them directly.

import type { Item } from "./types";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`;
    try {
      const body = (await res.json()) as { detail?: unknown };
      if (typeof body.detail === "string") detail = body.detail;
    } catch {
      // non-JSON error body — keep the status text
    }
    throw new Error(detail);
  }
  return (await res.json()) as T;
}

export function listItems(): Promise<Item[]> {
  return request<Item[]>("/api/items");
}

export function createItem(name: string, source: string): Promise<Item> {
  return request<Item>("/api/items", {
    method: "POST",
    body: JSON.stringify({ name, source }),
  });
}
