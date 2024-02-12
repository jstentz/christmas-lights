"use client";

import { useSearchParams } from "next/navigation";
import { App } from './app';
import { createStore } from "@/lib/store";
import { Provider } from 'react-redux'

const Home = () => {
  const password = useSearchParams().get('p') || "";
  const store = createStore(password);
  
  return (
      <Provider store={store}>
        <App />
      </Provider>
  );
}

export default Home;