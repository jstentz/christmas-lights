import { createSlice } from "@reduxjs/toolkit";

export type Animation = {
  id: number,
  animation_id: number,
  image_url: string,
  parameters_json: string,
  default_parameters_json: string,
  title: string,
  description: string,
  position: number,
};

export type AnimationsState = {
  animations: {
    [index: number]: Animation,
  },
  selectedAnimation: number,
  apiAuth: string,
};

export const createAnimationSlice = (apiAuth: string) => {
  const initialState: AnimationsState = {
    animations: {},
    selectedAnimation: 0,
    apiAuth: apiAuth,
  };
  return createSlice({
    name: 'animation',
    initialState: initialState,
    reducers: {
      selectAnimation: (state, action) => {
        state.selectedAnimation = action.payload
      }
    }
  });
};