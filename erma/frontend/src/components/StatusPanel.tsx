import type { ErmaState } from "../types/erma";

type StatusPanelProps = {
  state: ErmaState;
};

export default function StatusPanel({ state }: StatusPanelProps) {
  return (
    <section className="grid gap-3 text-left">
      <div className="rounded-lg border border-cyan-300/20 bg-white/5 p-4">
        <p className="text-xs uppercase tracking-[0.18em] text-cyan-200/70">Estado</p>
        <p className="mt-1 text-2xl font-semibold text-cyan-100">{state.status}</p>
      </div>
      <div className="rounded-lg border border-cyan-300/20 bg-white/5 p-4">
        <p className="text-xs uppercase tracking-[0.18em] text-cyan-200/70">Emocion</p>
        <p className="mt-1 text-2xl font-semibold text-cyan-100">{state.emotion}</p>
      </div>
      <div className="rounded-lg border border-cyan-300/20 bg-white/5 p-4">
        <p className="text-xs uppercase tracking-[0.18em] text-cyan-200/70">Mensaje</p>
        <p className="mt-2 text-lg text-cyan-50">{state.message}</p>
      </div>
    </section>
  );
}
