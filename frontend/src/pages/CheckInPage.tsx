import { useState, useCallback, type ReactNode } from "react";
import {
  Moon,
  Zap,
  Smile,
  Meh,
  Frown,
  CloudRain,
  Sun,
  Flame,
  Check,
  Coffee,
} from "lucide-react";
import { useAuth } from "@/lib/use-auth";
import { useAsyncData } from "@/lib/use-async-data";
import { api, type CheckInData } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { cn } from "@/lib/utils";

const SLEEP_LABELS = ["Tres mal", "Mal", "Correct", "Bien", "Tres bien"];
const ENERGY_LABELS = [
  "Epuise",
  "Fatigue",
  "Normal",
  "En forme",
  "Plein d'energie",
];

const MOOD_OPTIONS = [
  { value: "bien", label: "Bien", icon: Sun, color: "text-primary" },
  { value: "calme", label: "Calme", icon: Coffee, color: "text-sleep" },
  {
    value: "neutre",
    label: "Neutre",
    icon: Meh,
    color: "text-muted-foreground",
  },
  { value: "fatigue", label: "Fatigue", icon: Frown, color: "text-activity" },
  {
    value: "stresse",
    label: "Stresse",
    icon: CloudRain,
    color: "text-destructive",
  },
] as const;

function formatTodayDate(): string {
  return new Date().toLocaleDateString("fr-FR", {
    weekday: "long",
    day: "numeric",
    month: "long",
  });
}

export function CheckInPage() {
  const { patientId, displayName } = useAuth();

  const safePatientId = patientId ?? "";

  const {
    data: status,
    error: statusError,
    isLoading: statusLoading,
    retry: retryStatus,
  } = useAsyncData(
    () =>
      safePatientId
        ? api.checkIns.status(safePatientId)
        : Promise.reject(new Error("Patient ID manquant")),
    [safePatientId],
  );

  const [sleepQuality, setSleepQuality] = useState<number | null>(null);
  const [energyLevel, setEnergyLevel] = useState<number | null>(null);
  const [mood, setMood] = useState<string | null>(null);
  const [symptoms, setSymptoms] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [justCompleted, setJustCompleted] = useState(false);

  const canSubmit =
    sleepQuality !== null && energyLevel !== null && mood !== null;

  const handleSubmit = useCallback(async () => {
    if (!canSubmit || !patientId) return;
    setIsSubmitting(true);
    setSubmitError(null);

    const data: CheckInData = {
      patient_id: patientId,
      sleep_quality: sleepQuality!,
      energy_level: energyLevel!,
      mood: mood!,
      symptoms: symptoms.trim() || undefined,
    };

    try {
      await api.checkIns.submit(data);
      setJustCompleted(true);
    } catch (err) {
      setSubmitError(
        err instanceof Error ? err.message : "Erreur lors de l'envoi",
      );
    } finally {
      setIsSubmitting(false);
    }
  }, [canSubmit, patientId, sleepQuality, energyLevel, mood, symptoms]);

  if (statusLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <LoadingSpinner message="Chargement..." />
      </div>
    );
  }

  if (statusError) {
    return (
      <div className="px-6 py-8">
        <ErrorBanner message={statusError} onRetry={retryStatus} />
      </div>
    );
  }

  const completedToday = status?.completed_today || justCompleted;
  const streak = justCompleted
    ? (status?.streak ?? 0) + 1
    : (status?.streak ?? 0);
  const greeting = displayName ? `Bonjour ${displayName}` : "Bonjour";

  if (completedToday) {
    return <CompletedView greeting={greeting} streak={streak} />;
  }

  return (
    <div className="px-6 py-6 max-w-lg mx-auto">
      <header className="mb-6">
        <h1 className="text-2xl font-bold font-[var(--font-heading)]">
          {greeting}
        </h1>
        <p className="text-muted-foreground capitalize">{formatTodayDate()}</p>
        {streak > 0 && (
          <div className="flex items-center gap-1.5 mt-2 text-sm text-activity">
            <Flame size={16} />
            <span>
              Serie de {streak} jour{streak > 1 ? "s" : ""}
            </span>
          </div>
        )}
      </header>

      <div className="flex flex-col gap-6">
        <ScaleSelector
          label="Comment avez-vous dormi ?"
          icon={<Moon size={20} className="text-sleep" />}
          value={sleepQuality}
          onChange={setSleepQuality}
          labels={SLEEP_LABELS}
          activeClass="bg-sleep/15 border-sleep text-sleep"
        />

        <ScaleSelector
          label="Votre niveau d'energie ?"
          icon={<Zap size={20} className="text-activity" />}
          value={energyLevel}
          onChange={setEnergyLevel}
          labels={ENERGY_LABELS}
          activeClass="bg-activity/15 border-activity text-activity"
        />

        <MoodSelector value={mood} onChange={setMood} />

        <Card className="p-4">
          <label
            htmlFor="symptoms"
            className="block text-sm font-medium text-muted-foreground mb-2"
          >
            Douleurs ou remarques ? (optionnel)
          </label>
          <textarea
            id="symptoms"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            placeholder="Ex: mal au dos, bien dormi, beaucoup marche..."
            rows={2}
            className="w-full rounded-lg border border-border bg-background px-4 py-3 text-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </Card>

        {submitError && <ErrorBanner message={submitError} />}

        <Button
          onClick={handleSubmit}
          disabled={!canSubmit || isSubmitting}
          className="w-full text-lg min-h-[56px]"
        >
          {isSubmitting ? "Envoi..." : "Valider mon bilan"}
        </Button>
      </div>
    </div>
  );
}

function ScaleSelector({
  label,
  icon,
  value,
  onChange,
  labels,
  activeClass,
}: {
  label: string;
  icon: ReactNode;
  value: number | null;
  onChange: (v: number) => void;
  labels: string[];
  activeClass: string;
}) {
  return (
    <Card className="p-4">
      <div className="flex items-center gap-2 mb-3">
        {icon}
        <span className="font-medium">{label}</span>
      </div>
      <div className="flex gap-2">
        {[1, 2, 3, 4, 5].map((n) => (
          <button
            key={n}
            type="button"
            onClick={() => onChange(n)}
            aria-label={`${labels[n - 1]} (${n}/5)`}
            className={cn(
              "flex-1 flex flex-col items-center justify-center rounded-lg py-3 min-h-[56px] transition-all border-2",
              value === n
                ? activeClass
                : "bg-muted/50 border-transparent text-muted-foreground hover:bg-muted",
            )}
          >
            <span className="text-lg font-bold">{n}</span>
            <span className="text-xs leading-tight mt-0.5">
              {labels[n - 1]}
            </span>
          </button>
        ))}
      </div>
    </Card>
  );
}

function MoodSelector({
  value,
  onChange,
}: {
  value: string | null;
  onChange: (v: string) => void;
}) {
  return (
    <Card className="p-4">
      <div className="flex items-center gap-2 mb-3">
        <Smile size={20} className="text-mood" />
        <span className="font-medium">Votre humeur ?</span>
      </div>
      <div className="flex gap-2">
        {MOOD_OPTIONS.map(({ value: v, label, icon: Icon, color }) => (
          <button
            key={v}
            type="button"
            onClick={() => onChange(v)}
            aria-label={label}
            className={cn(
              "flex-1 flex flex-col items-center justify-center rounded-lg py-3 min-h-[56px] transition-all border-2",
              value === v
                ? "bg-mood/15 border-mood"
                : "bg-muted/50 border-transparent hover:bg-muted",
            )}
          >
            <Icon size={22} className={value === v ? "text-mood" : color} />
            <span className="text-xs leading-tight mt-1">{label}</span>
          </button>
        ))}
      </div>
    </Card>
  );
}

function CompletedView({
  greeting,
  streak,
}: {
  greeting: string;
  streak: number;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] px-6 text-center">
      <div className="w-20 h-20 rounded-full bg-primary/15 flex items-center justify-center mb-6">
        <Check size={40} className="text-primary" />
      </div>
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-2">
        {greeting}
      </h1>
      <p className="text-lg text-muted-foreground mb-4">
        Bilan du jour complete
      </p>
      {streak > 0 && (
        <div className="flex items-center gap-2 text-activity text-lg font-medium">
          <Flame size={24} />
          <span>
            Serie de {streak} jour{streak > 1 ? "s" : ""}
          </span>
        </div>
      )}
      <p className="text-sm text-muted-foreground mt-6 max-w-xs">
        Revenez demain pour maintenir votre serie et ameliorer votre score de
        vitalite.
      </p>
    </div>
  );
}
