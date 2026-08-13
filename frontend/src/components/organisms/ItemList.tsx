// Organism: fetches data (via api/client) and renders it. Re-fetches when
// `version` changes — the page bumps it after mutations.

import { useEffect, useState } from "react";
import { listItems } from "../../api/client";
import type { Item } from "../../api/types";

interface Props {
  version: number;
}

export function ItemList({ version }: Props) {
  const [items, setItems] = useState<Item[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    listItems()
      .then((data) => {
        if (!cancelled) setItems(data);
      })
      .catch((e) => {
        if (!cancelled) setError(e instanceof Error ? e.message : String(e));
      });
    return () => {
      cancelled = true;
    };
  }, [version]);

  if (error) return <p className="error" role="alert">{error}</p>;
  if (items === null) return <p data-testid="items-loading">Loading…</p>;
  if (items.length === 0) return <p data-testid="items-empty">No items yet.</p>;

  return (
    <ul data-testid="item-list">
      {items.map((item) => (
        <li key={item.id} data-testid="item-row">
          {item.name} <small>({item.source})</small>
        </li>
      ))}
    </ul>
  );
}
