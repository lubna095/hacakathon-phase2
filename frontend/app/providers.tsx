"use client";

import { AuthProvider } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export function Providers({ children }: { children: React.ReactNode }) {
  return <AuthProvider>{children}</AuthProvider>;
}
