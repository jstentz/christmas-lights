"use client";

import { BackendContextProvider } from "@/context/backend";
import { useSearchParams } from "next/navigation";
import { App } from './app';
import { store } from "@/lib/store";
import { Provider } from 'react-redux'

const Home = () => {
  const password = useSearchParams().get('p') || "";
  
  return (
      <Provider store={store}>
        <App />
      </Provider>
  );
}

export default Home;