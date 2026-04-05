import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { MealsPage } from "@/pages/MealsPage";
import { AuthContext, type AuthContextValue } from "@/lib/auth-context-value";

vi.mock("@/lib/api", async () => {
  const meals = [
    {
      id: "m1",
      patient_id: "p1",
      photo_url: "demo://photo",
      analysis: {
        summary: "Salade nicoise avec oeuf",
        foods_identified: ["salade", "oeuf"],
        nutritional_highlights: ["Riche en proteines"],
        quality_score: 78,
        micro_tip: "Ajoutez du pain complet",
      },
      nutrition_score: 78,
      meal_type: "lunch",
      date: "2026-04-05",
      created_at: "2026-04-05T12:30:00Z",
    },
  ];

  return {
    api: {
      meals: {
        history: vi.fn().mockResolvedValue(meals),
        analyze: vi.fn().mockResolvedValue(meals[0]),
      },
    },
    ApiRequestError: class extends Error {
      status: number;
      code: string;
      constructor(s: number, c: string, m: string) {
        super(m);
        this.status = s;
        this.code = c;
      }
    },
  };
});

const mockAuth: AuthContextValue = {
  isAuthenticated: true,
  isLoading: false,
  patientId: "p1",
  displayName: "Marie",
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
};

function renderMeals() {
  return render(
    <MemoryRouter>
      <AuthContext value={mockAuth}>
        <MealsPage />
      </AuthContext>
    </MemoryRouter>,
  );
}

describe("MealsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows the page heading", async () => {
    renderMeals();
    expect(await screen.findByText("Mes Repas")).toBeInTheDocument();
  });

  it("shows the camera button", async () => {
    renderMeals();
    expect(await screen.findByText("Prendre une photo")).toBeInTheDocument();
  });

  it("shows meal type selector", async () => {
    renderMeals();
    expect(await screen.findByText("Dejeuner")).toBeInTheDocument();
    expect(screen.getByText("Diner")).toBeInTheDocument();
  });

  it("shows meal history", async () => {
    renderMeals();
    expect(
      await screen.findByText("Salade nicoise avec oeuf"),
    ).toBeInTheDocument();
  });
});
