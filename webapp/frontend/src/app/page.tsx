"use client";

import { useSearchParams } from "next/navigation";
import { App } from './app';
import { store, axiosInstance } from "@/lib/store";
import { Provider } from 'react-redux'
import { useMemo } from "react";

const Home = () => {
  const password = useSearchParams().get('p') || "";
  useMemo(() => axiosInstance.defaults.headers.common['API_AUTH'] = password, [password]);
  
  return (
      <Provider store={store}>
        <App />
      </Provider>
  );
}

export default Home;