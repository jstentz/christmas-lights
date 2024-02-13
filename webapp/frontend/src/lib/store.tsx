import { configureStore } from '@reduxjs/toolkit'
import { animationSlice } from '@/reducers/animationsReducer';
import axios from 'axios';

export const createStore = (apiAuth: string) => {

  const instance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL
  });
  // instance.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  // instance.defaults.xsrfCookieName = "csrftoken";
  instance.defaults.headers.common['API_AUTH'] = apiAuth;

  return configureStore({
    reducer: {
      animation: animationSlice.reducer
    },
    middleware: (getDefaultMiddleware) => 
      getDefaultMiddleware(
        {
          thunk: {extraArgument: instance},
        }
      )
  });
};

export type RootState = ReturnType<ReturnType<typeof createStore>['getState']>;
export type AppDispatch = ReturnType<typeof createStore>['dispatch'];