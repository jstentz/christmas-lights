"use client";

import { BackendContextProvider } from "@/context/backend";
import { useSearchParams } from "next/navigation";
import { App } from './app';

const Home = () => {
  const password = useSearchParams().get('p') || "";
  
  return (
    <BackendContextProvider apiAuth={password}>
      <App />
    </BackendContextProvider>
  );
}

export default Home;