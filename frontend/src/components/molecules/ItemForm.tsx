// Molecule: composes atoms, owns only its form state. Data flows up via onCreate.

import { useState } from "react";
import type { FormEvent } from "react";
import { Button } from "../atoms/Button";
import { TextInput } from "../atoms/TextInput";

interface Props {
  onCreate: (name: string) => Promise<void>;
}

export function ItemForm({ onCreate }: Props) {
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await onCreate(name);
      setName("");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} data-testid="item-form">
      <TextInput
        data-testid="item-name"
        placeholder="New item name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        disabled={busy}
      />
      <Button type="submit" data-testid="item-submit" disabled={busy}>
        {busy ? "Adding…" : "Add"}
      </Button>
      {error && (
        <p className="error" role="alert" data-testid="item-error">
          {error}
        </p>
      )}
    </form>
  );
}
