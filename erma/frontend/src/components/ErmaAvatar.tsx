import type { ErmaEmotion, ErmaStatus } from "../types/erma";

type ErmaAvatarProps = {
  status: ErmaStatus;
  emotion: ErmaEmotion;
};

type Mood = {
  leftEye: string;
  rightEye: string;
  mouth: string;
  label: string;
};

const moods: Record<ErmaEmotion, Mood> = {
  neutral: {
    leftEye: "erma-eye-calm",
    rightEye: "erma-eye-calm",
    mouth: "erma-mouth-neutral",
    label: "neutral",
  },
  alegre: {
    leftEye: "erma-eye-happy",
    rightEye: "erma-eye-happy",
    mouth: "erma-mouth-happy",
    label: "alegre",
  },
  cansado: {
    leftEye: "erma-eye-sleepy",
    rightEye: "erma-eye-sleepy",
    mouth: "erma-mouth-sleepy",
    label: "cansada",
  },
  curioso: {
    leftEye: "erma-eye-curious-left",
    rightEye: "erma-eye-curious-right",
    mouth: "erma-mouth-curious",
    label: "curiosa",
  },
};

export default function ErmaAvatar({ status, emotion }: ErmaAvatarProps) {
  const isSleeping = status === "sleep";
  const isTalking = status === "talking" || status === "greeting";
  const mood = isSleeping
    ? {
        leftEye: "erma-eye-sleep",
        rightEye: "erma-eye-sleep",
        mouth: "erma-mouth-sleep",
        label: "durmiendo",
      }
    : moods[emotion];

  return (
    <div className="flex min-h-[260px] items-center justify-center">
      <div
        aria-label={`ERMA ${mood.label}`}
        className={[
          "erma-avatar relative flex h-56 w-56 items-center justify-center rounded-full border border-cyan-200/70 bg-[#0a252b]",
          isSleeping ? "erma-avatar-sleeping" : "",
          isTalking ? "erma-avatar-talking" : "",
        ].join(" ")}
      >
        <div className="erma-halo erma-halo-outer" />
        <div className="erma-halo erma-halo-inner" />
        <div className="absolute inset-5 rounded-full border border-cyan-100/15" />
        <div className="absolute inset-10 rounded-full bg-cyan-200/5 blur-sm" />

        {isSleeping ? (
          <div className="erma-sleep-bubbles" aria-hidden="true">
            <span>z</span>
            <span>z</span>
            <span>z</span>
          </div>
        ) : null}

        <div className="relative z-10 grid gap-5">
          <div className="flex items-center justify-center gap-9">
            <span className={`erma-eye ${mood.leftEye}`} />
            <span className={`erma-eye ${mood.rightEye}`} />
          </div>
          <div className="flex justify-center">
            <span className={`erma-mouth ${mood.mouth}`} />
          </div>
        </div>

        <div className="erma-status-light" />
      </div>
    </div>
  );
}
