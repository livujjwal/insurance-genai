export interface User {
  id: string;
  email: string;
  name: string;
  role: "employee" | "admin";
  created_at: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setUser: (user: User | null) => void;
  logout: () => void;
}
