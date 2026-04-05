import { useState, useCallback } from "react";
import {
  Flame,
  Check,
  Plus,
  Moon,
  Apple,
  Footprints,
  Heart,
  X,
  ChevronRight,
} from "lucide-react";
import { useAuth } from "@/lib/use-auth";
import { useAsyncData } from "@/lib/use-async-data";
import { api, type HabitResponse, type HabitTemplate } from "@/lib/api";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { ErrorBanner } from "@/components/ui/ErrorBanner";
import { cn } from "@/lib/utils";

const DIMENSION_META: Record<
  string,
  { icon: typeof Moon; color: string; label: string }
> = {
  sleep: { icon: Moon, color: "text-sleep", label: "Sommeil" },
  nutrition: { icon: Apple, color: "text-nutrition", label: "Nutrition" },
  activity: { icon: Footprints, color: "text-activity", label: "Activite" },
  mood: { icon: Heart, color: "text-mood", label: "Humeur" },
};

const MAX_ACTIVE = 3;

export function HabitsPage() {
  const { patientId } = useAuth();
  const safePatientId = patientId ?? "";
  const [showBrowser, setShowBrowser] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const {
    data: habits,
    error,
    isLoading,
    retry,
  } = useAsyncData(
    () =>
      safePatientId
        ? api.habits.list(safePatientId)
        : Promise.reject(new Error("Patient ID manquant")),
    [safePatientId, refreshKey],
  );

  const handleCompleted = useCallback(() => {
    setRefreshKey((k) => k + 1);
  }, []);

  const handleActivated = useCallback(() => {
    setShowBrowser(false);
    setRefreshKey((k) => k + 1);
  }, []);

  if (isLoading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <LoadingSpinner message="Chargement..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="px-6 py-8">
        <ErrorBanner message={error} onRetry={retry} />
      </div>
    );
  }

  const activeHabits = habits ?? [];
  const canAddMore = activeHabits.length < MAX_ACTIVE;

  if (showBrowser) {
    return (
      <TemplateBrowser
        patientId={safePatientId}
        activeTemplateIds={activeHabits.map((h) => h.template_id)}
        onActivated={handleActivated}
        onClose={() => setShowBrowser(false)}
      />
    );
  }

  return (
    <div className="px-6 py-6 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-6">
        Mes Habitudes
      </h1>

      {activeHabits.length === 0 ? (
        <EmptyState onAdd={() => setShowBrowser(true)} />
      ) : (
        <div className="flex flex-col gap-4">
          {activeHabits.map((habit) => (
            <HabitCard
              key={habit.id}
              habit={habit}
              onCompleted={handleCompleted}
            />
          ))}

          {canAddMore && (
            <button
              type="button"
              onClick={() => setShowBrowser(true)}
              className="flex items-center justify-center gap-2 rounded-lg border-2 border-dashed border-border p-4 text-muted-foreground hover:border-primary hover:text-primary transition-colors min-h-[56px]"
              aria-label="Ajouter une habitude"
            >
              <Plus size={20} />
              <span>Ajouter une habitude</span>
            </button>
          )}
        </div>
      )}
    </div>
  );
}

function HabitCard({
  habit,
  onCompleted,
}: {
  habit: HabitResponse;
  onCompleted: () => void;
}) {
  const [completing, setCompleting] = useState(false);
  const [justDone, setJustDone] = useState(false);
  const [completeError, setCompleteError] = useState<string | null>(null);

  const meta = DIMENSION_META[habit.dimension] ?? DIMENSION_META.mood;
  const Icon = meta.icon;
  const completed = habit.completed_today || justDone;

  const handleComplete = useCallback(async () => {
    setCompleting(true);
    setCompleteError(null);
    try {
      await api.habits.complete(habit.id);
      setJustDone(true);
      onCompleted();
    } catch (err) {
      setCompleteError(err instanceof Error ? err.message : "Erreur");
    } finally {
      setCompleting(false);
    }
  }, [habit.id, onCompleted]);

  const streak = justDone ? habit.current_streak + 1 : habit.current_streak;

  return (
    <Card className="p-4">
      <div className="flex items-start gap-3">
        <div
          className={cn(
            "w-12 h-12 rounded-full flex items-center justify-center shrink-0",
            completed ? "bg-primary/15" : "bg-muted",
          )}
        >
          {completed ? (
            <Check size={24} className="text-primary" />
          ) : (
            <Icon size={24} className={meta.color} />
          )}
        </div>

        <div className="flex-1 min-w-0">
          <p
            className={cn(
              "font-medium",
              completed && "line-through text-muted-foreground",
            )}
          >
            {habit.name}
          </p>
          <div className="flex items-center gap-3 mt-1">
            <span
              className={cn(
                "text-xs px-2 py-0.5 rounded-full",
                `bg-${habit.dimension}/10`,
                meta.color,
              )}
            >
              {meta.label}
            </span>
            {streak > 0 && (
              <span className="flex items-center gap-1 text-xs text-activity">
                <Flame size={12} />
                {streak} jour{streak > 1 ? "s" : ""}
              </span>
            )}
          </div>
        </div>

        {!completed && (
          <button
            type="button"
            onClick={handleComplete}
            disabled={completing}
            className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center shrink-0 hover:opacity-90 transition-opacity disabled:opacity-50"
            aria-label={`Completer ${habit.name}`}
          >
            {completing ? (
              <div className="w-5 h-5 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
            ) : (
              <Check size={20} />
            )}
          </button>
        )}
      </div>
      {completeError && (
        <p className="text-xs text-destructive mt-2">{completeError}</p>
      )}
    </Card>
  );
}

function TemplateBrowser({
  patientId,
  activeTemplateIds,
  onActivated,
  onClose,
}: {
  patientId: string;
  activeTemplateIds: string[];
  onActivated: () => void;
  onClose: () => void;
}) {
  const {
    data: templates,
    isLoading,
    error,
  } = useAsyncData(() => api.habits.templates(), []);

  const [activating, setActivating] = useState<string | null>(null);
  const [activateError, setActivateError] = useState<string | null>(null);

  const handleActivate = useCallback(
    async (templateId: string) => {
      setActivating(templateId);
      setActivateError(null);
      try {
        await api.habits.activate({
          patient_id: patientId,
          template_id: templateId,
        });
        onActivated();
      } catch (err) {
        setActivateError(err instanceof Error ? err.message : "Erreur");
      } finally {
        setActivating(null);
      }
    },
    [patientId, onActivated],
  );

  const dimensions = ["sleep", "nutrition", "activity", "mood"];

  return (
    <div className="px-6 py-6 max-w-lg mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold font-[var(--font-heading)]">
          Choisir une habitude
        </h1>
        <button
          type="button"
          onClick={onClose}
          className="w-10 h-10 rounded-full bg-muted flex items-center justify-center"
          aria-label="Fermer"
        >
          <X size={20} />
        </button>
      </div>

      {isLoading && <LoadingSpinner message="Chargement..." />}
      {error && <ErrorBanner message={error} />}
      {activateError && <ErrorBanner message={activateError} />}

      {templates && (
        <div className="flex flex-col gap-6">
          {dimensions.map((dim) => {
            const meta = DIMENSION_META[dim];
            if (!meta) return null;
            const Icon = meta.icon;
            const dimTemplates = templates.filter(
              (t: HabitTemplate) => t.dimension === dim,
            );
            if (dimTemplates.length === 0) return null;

            return (
              <div key={dim}>
                <div className="flex items-center gap-2 mb-3">
                  <Icon size={18} className={meta.color} />
                  <span className="font-medium">{meta.label}</span>
                </div>
                <div className="flex flex-col gap-2">
                  {dimTemplates.map((t: HabitTemplate) => {
                    const isActive = activeTemplateIds.includes(t.id);
                    return (
                      <button
                        key={t.id}
                        type="button"
                        disabled={isActive || activating !== null}
                        onClick={() => handleActivate(t.id)}
                        className={cn(
                          "flex items-center justify-between rounded-lg border p-4 text-left transition-colors min-h-[56px]",
                          isActive
                            ? "border-border bg-muted/50 text-muted-foreground"
                            : "border-border hover:border-primary",
                          activating === t.id && "opacity-50",
                        )}
                      >
                        <div>
                          <p className="font-medium">{t.name}</p>
                          <p className="text-xs text-muted-foreground mt-0.5">
                            {t.description}
                          </p>
                        </div>
                        {isActive ? (
                          <Check
                            size={18}
                            className="text-primary shrink-0 ml-2"
                          />
                        ) : (
                          <ChevronRight
                            size={18}
                            className="text-muted-foreground shrink-0 ml-2"
                          />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function EmptyState({ onAdd }: { onAdd: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] text-center">
      <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mb-6">
        <Flame size={36} className="text-muted-foreground" />
      </div>
      <h2 className="text-xl font-bold font-[var(--font-heading)] mb-2">
        Pas encore d'habitudes
      </h2>
      <p className="text-muted-foreground mb-6 max-w-xs">
        Choisissez 3 micro-habitudes pour ameliorer votre vitalite au quotidien.
      </p>
      <Button onClick={onAdd}>Choisir mes habitudes</Button>
    </div>
  );
}
