import { FormEvent, useEffect, useState } from "react";
import ErmaAvatar from "../components/ErmaAvatar";
import StatusPanel from "../components/StatusPanel";
import { getState, sendCommand, sleepErma, wakeErma } from "../services/api";
import type { ErmaResponse, ErmaState } from "../types/erma";

const initialState: ErmaState = {
  status: "idle",
  emotion: "neutral",
  message: "ERMA esta activa",
};

export default function Home() {
  const [state, setState] = useState<ErmaState>(initialState);
  const [command, setCommand] = useState("");
  const [lastResponse, setLastResponse] = useState<ErmaResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getState()
      .then(setState)
      .catch(() => setError("No pude conectar con el backend de ERMA."));
  }, []);

  async function runAction(action: () => Promise<ErmaResponse>) {
    setLoading(true);
    setError("");

    try {
      const response = await action();
      setState({
        status: response.status,
        emotion: response.emotion,
        message: response.message,
      });
      setLastResponse(response);
    } catch (apiError) {
      setError(apiError instanceof Error ? apiError.message : "Error inesperado.");
    } finally {
      setLoading(false);
    }
  }

  function submitCommand(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!command.trim()) {
      setError("Escribi un comando para ERMA.");
      return;
    }

    runAction(() => sendCommand(command));
    setCommand("");
  }

  return (
    <main className="min-h-screen bg-[#071014] px-4 py-5 text-cyan-50 sm:px-6">
      <div className="mx-auto flex min-h-[calc(100vh-40px)] max-w-5xl flex-col gap-5">
        <header className="flex flex-col gap-1 border-b border-cyan-300/20 pb-4">
          <p className="text-sm uppercase tracking-[0.28em] text-cyan-200/70">Asistente local</p>
          <h1 className="text-4xl font-bold tracking-normal text-cyan-100 sm:text-5xl">
            INFINITY ERMA
          </h1>
        </header>

        <section className="grid flex-1 gap-5 lg:grid-cols-[320px_1fr]">
          <div className="rounded-lg border border-cyan-300/20 bg-[#0b1b21] p-5">
            <ErmaAvatar status={state.status} emotion={state.emotion} />
          </div>

          <div className="grid gap-5">
            <StatusPanel state={state} />

            <form className="rounded-lg border border-cyan-300/20 bg-[#0b1b21] p-4" onSubmit={submitCommand}>
              <label className="text-sm text-cyan-100" htmlFor="command">
                Comando escrito
              </label>
              <div className="mt-3 flex flex-col gap-3 sm:flex-row">
                <input
                  id="command"
                  className="min-h-12 flex-1 rounded-md border border-cyan-300/30 bg-[#061217] px-4 text-cyan-50 outline-none focus:border-cyan-200"
                  value={command}
                  onChange={(event) => setCommand(event.target.value)}
                  placeholder="Ej: ERMA dormite un rato"
                />
                <button
                  className="min-h-12 rounded-md bg-cyan-300 px-6 font-semibold text-[#061217] disabled:opacity-60"
                  disabled={loading}
                  type="submit"
                >
                  Enviar
                </button>
              </div>
            </form>

            <section className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <button className="min-h-14 rounded-md border border-cyan-300/30 bg-cyan-300/10 font-semibold" onClick={() => runAction(sleepErma)}>
                Dormir
              </button>
              <button className="min-h-14 rounded-md border border-cyan-300/30 bg-cyan-300/10 font-semibold" onClick={() => runAction(wakeErma)}>
                Despertar
              </button>
              <button className="min-h-14 rounded-md border border-cyan-300/30 bg-cyan-300/10 font-semibold" onClick={() => runAction(() => sendCommand("hola"))}>
                Saludar
              </button>
              <button className="min-h-14 rounded-md border border-cyan-300/30 bg-cyan-300/10 font-semibold" onClick={() => runAction(() => sendCommand("motivame"))}>
                Frase
              </button>
            </section>

            <section className="min-h-28 rounded-lg border border-cyan-300/20 bg-white/5 p-4">
              <p className="text-xs uppercase tracking-[0.18em] text-cyan-200/70">Respuesta</p>
              {error ? <p className="mt-3 text-red-200">{error}</p> : null}
              {lastResponse ? (
                <div className="mt-3 text-sm leading-6 text-cyan-50">
                  <p>Intent: {lastResponse.intent}</p>
                  <p>Mensaje: {lastResponse.message}</p>
                  <p>Keywords: {lastResponse.matched_keywords.join(", ") || "sin coincidencias"}</p>
                </div>
              ) : (
                <p className="mt-3 text-cyan-100/70">ERMA esta esperando un comando.</p>
              )}
            </section>
          </div>
        </section>
      </div>
    </main>
  );
}
