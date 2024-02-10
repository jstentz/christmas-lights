import React from "react";
import { BackendContext } from "@/context/backend";

// Custom hook to provide the backend context data
export function useBackend() {
  const context = React.useContext(BackendContext);

  if (!context) {
    throw new Error(
      "useBackend must be used within the scope of BackendContextProvider"
    );
  }

  return context;
}
