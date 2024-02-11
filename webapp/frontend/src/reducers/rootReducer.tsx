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
};

const initialState: AnimationsState = {
  animations: {},
  selectedAnimation: 0, 
}

export const animationSlice = createSlice({
  name: 'animation',
  initialState: initialState,
  reducers: {
    selectAnimation: (state, action) => {
      state.selectedAnimation = action.payload
    }
  }
});

export const { selectAnimation } = animationSlice.actions

export const animationReducer = animationSlice.reducer