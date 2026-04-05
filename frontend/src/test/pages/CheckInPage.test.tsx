import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import { CheckInPage } from "@/pages/CheckInPage";
import { AuthContext, type AuthContextValue } from "@/lib/auth-context-value";

vi.mock("@/lib/api", () => ({
  api: {
    checkIns: {
      status: vi.fn().mockResolvedValue({
        completed_today: false,
        streak: 5,
        today_check_in: null,
      }),
      submit: vi.fn().mockResolvedValue({}),
    },
  },
  ApiRequestError: class extends Error {
    status: number;
    code: string;
    constructor(status: number, code: string, message: string) {
      super(message);
      this.status = status;
      this.code = code;
    }
  },
}));

const mockAuth: AuthContextValue = {
  isAuthenticated: true,
  isLoading: false,
  patientId: "00000000-0000-0000-0000-000000000001",
  displayName: "Marie",
  login: vi.fn(),
  register: vi.fn(),
  logout: vi.fn(),
};

function renderCheckIn() {
  return render(
    <MemoryRouter>
      <AuthContext value={mockAuth}>
        <CheckInPage />
      </AuthContext>
    </MemoryRouter>,
  );
}

describe("CheckInPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows greeting with user name", async () => {
    renderCheckIn();
    expect(await screen.findByText("Bonjour Marie")).toBeInTheDocument();
  });

  it("shows streak counter", async () => {
    renderCheckIn();
    expect(await screen.findByText(/Serie de 5 jours/)).toBeInTheDocument();
  });

  it("shows sleep quality selector", async () => {
    renderCheckIn();
    expect(
      await screen.findByText("Comment avez-vous dormi ?"),
    ).toBeInTheDocument();
  });

  it("shows energy level selector", async () => {
    renderCheckIn();
    expect(
      await screen.findByText("Votre niveau d'energie ?"),
    ).toBeInTheDocument();
  });

  it("shows mood selector", async () => {
    renderCheckIn();
    expect(await screen.findByText("Votre humeur ?")).toBeInTheDocument();
  });

  it("submit button is disabled until all fields selected", async () => {
    renderCheckIn();
    const button = await screen.findByText("Valider mon bilan");
    expect(button).toBeDisabled();
  });
});
