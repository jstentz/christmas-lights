"use client";

import { useSearchParams } from "next/navigation";
import { App } from './app';
import { store, axiosInstance } from "@/lib/store";
import { Provider } from 'react-redux'
import { useMemo, Suspense } from "react";

const Home = () => {
  const password = useSearchParams().get('p') || "";
  useMemo(() => axiosInstance.defaults.headers.common['API_AUTH'] = password, [password]);

  return (
    <Provider store={store}>
      <App />
    </Provider>
  );
}

const Root = () => { 
  return (
    <Suspense>
      <Home />
    </Suspense>
  );
}

export default Root;