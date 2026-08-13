// Page: wires the full atomic chain (template ← organism + molecule ← atoms).
// The `source` sent with UI-created items follows the data rule: manual:<who>.

import { useState } from "react";
import { createItem } from "../../api/client";
import { ItemForm } from "../molecules/ItemForm";
import { ItemList } from "../organisms/ItemList";
import { MainLayout } from "../templates/MainLayout";

export function HomePage() {
  const [version, setVersion] = useState(0);

  async function handleCreate(name: string) {
    await createItem(name, "manual:ui");
    setVersion((v) => v + 1);
  }

  return (
    <MainLayout>
      <ItemForm onCreate={handleCreate} />
      <ItemList version={version} />
    </MainLayout>
  );
}
