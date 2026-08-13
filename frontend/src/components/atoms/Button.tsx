// Atom: no state, no children components. Placement rules:
// docs/03-technical/01-project-organization/01-repo-layout.md §frontend

import type { ButtonHTMLAttributes } from "react";

export function Button(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button className="btn" {...props} />;
}
