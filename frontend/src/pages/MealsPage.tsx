import { Card } from "@/components/ui/Card";
import { UtensilsCrossed } from "lucide-react";

export function MealsPage() {
  return (
    <div className="px-6 py-8">
      <h1 className="text-2xl font-bold font-[var(--font-heading)] mb-6">
        Mes Repas
      </h1>
      <Card className="p-6 text-center">
        <UtensilsCrossed size={48} className="mx-auto mb-4 text-nutrition" />
        <p className="text-muted-foreground">
          Photographiez vos repas pour une analyse nutritionnelle IA.
        </p>
        <p className="text-sm text-muted-foreground mt-2">
          Cadrage positif — pas de comptage de calories.
        </p>
      </Card>
    </div>
  );
}
