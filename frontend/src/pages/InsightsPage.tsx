import { Card } from "@/components/ui/Card";
import { Lightbulb, Lock } from "lucide-react";

export function InsightsPage() {
  return (
    <div className="px-6 py-8">
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-6">
        Mes Insights
      </h1>
      <Card className="p-6 text-center">
        <div className="relative inline-block mb-4">
          <Lightbulb size={48} className="text-mood mx-auto" />
          <Lock
            size={20}
            className="absolute -bottom-1 -right-1 text-muted-foreground"
          />
        </div>
        <p className="text-muted-foreground">
          Continuez vos bilans pour debloquer vos insights personnels.
        </p>
        <p className="text-sm text-muted-foreground mt-2">
          Apres 14 jours de donnees, l'IA revelera vos correlations
          personnelles.
        </p>
      </Card>
    </div>
  );
}
