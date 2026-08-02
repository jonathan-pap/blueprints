# macros — Tabular Editor 3 macros

> **Macros** are saved C# actions bound to the TE3 UI (right-click menus, toolbar) so a bulk operation
> is one click away. Macros are a **TE3** feature; TE2 has no macro manager. Keep the *logic* portable
> ([`../compatibility.md`](../compatibility.md)) so the same body also works as a plain
> [`../scripts/`](../scripts/) file in TE2.

## How macros work (TE3)

- Author in *C# Script* → *Save as Macro*; TE3 stores them in `Preferences → Macros` (a JSON with the
  script body, name, tooltip, and a **context** — which object types the macro appears for).
- A macro body is the **same C#** as a script here. The only extra is the UI binding (context/enabled).
- To share: export the macro JSON, or keep the portable body in [`../scripts/`](../scripts/) and register
  it as a macro on each machine.

## Convention for this folder

- Store each macro's **body** as a `.cs` file here (portable, TE2-runnable), plus a one-line header
  comment for its intended **context** (e.g. `// macro-context: Measure`).
- Keep the shared list in this index.

| Macro (.cs) | Context | Does |
|---|---|---|
| _(none yet — add portable macro bodies here)_ | | |

## Adding a macro

1. Write the body against the [portability rules](../compatibility.md) (so it also runs in TE2).
2. Save it here as `<name>.cs` with a `// macro-context: <ObjectType>` header.
3. In TE3: *C# Script → paste → Save as Macro*, set the same context.
4. Add a row above.
