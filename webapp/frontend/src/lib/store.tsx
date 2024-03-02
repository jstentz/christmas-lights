import { configureStore } from '@reduxjs/toolkit'
import { animationSlice } from '@/reducers/animationsReducer';
import axios from 'axios';

export const axiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL
});

export const store = configureStore({
  reducer: {
    animation: animationSlice.reducer
  },
  middleware: (getDefaultMiddleware) => 
    getDefaultMiddleware(
      {
        thunk: {extraArgument: axiosInstance},
      }
    )
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;