import type { ErmaEmotion, ErmaStatus } from "../types/erma";

type ErmaAvatarProps = {
  status: ErmaStatus;
  emotion: ErmaEmotion;
};

const faces: Record<ErmaEmotion, string> = {
  neutral: "--",
  alegre: "^^",
  cansado: "-_",
  curioso: "o?",
};

export default function ErmaAvatar({ status, emotion }: ErmaAvatarProps) {
  const isSleeping = status === "sleep";

  return (
    <div className="flex items-center justify-center">
      <div className="relative flex h-44 w-44 items-center justify-center rounded-full border border-cyan-300/70 bg-cyan-400/10 shadow-[0_0_45px_rgba(34,211,238,0.25)]">
        <div className="absolute inset-4 rounded-full border border-cyan-200/20" />
        <div className="text-center">
          <div className="font-mono text-5xl tracking-normal text-cyan-100">
            {isSleeping ? "zz" : faces[emotion]}
          </div>
          <div className="mt-3 h-1 w-20 rounded-full bg-cyan-300/80" />
        </div>
      </div>
    </div>
  );
}
