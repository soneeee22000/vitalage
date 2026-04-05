import { createContext } from "react";

export interface AuthContextValue {
  isAuthenticated: boolean;
  isLoading: boolean;
  patientId: string | null;
  displayName: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: {
    email: string;
    password: string;
    given_name: string;
    family_name: string;
    display_name: string;
  }) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextValue | null>(null);
