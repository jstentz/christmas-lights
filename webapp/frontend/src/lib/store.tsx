import { configureStore } from '@reduxjs/toolkit'
import { createAnimationSlice } from '@/reducers/rootReducer'

export const createStore = (apiAuth: string) => {
  const animationSlice = createAnimationSlice(apiAuth);
  return configureStore({
    reducer: {
      animation: animationSlice.reducer
    }
  });
};

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<ReturnType<typeof createStore>['getState']>;
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = ReturnType<typeof createStore>['dispatch'];