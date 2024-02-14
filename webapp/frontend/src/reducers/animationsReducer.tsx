import { createAsyncThunk, createSlice, isPending, isRejected } from "@reduxjs/toolkit";
import axios, { AxiosInstance } from "axios";
import { AppDispatch, RootState } from "@/lib/store";

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

export type AnimationsMap = {
  [index: number]: Animation,
}

export type AnimationsState = {
  animations: AnimationsMap,
  selectedAnimation: number,
  status: 'idle' | 'loading' | 'succeeded' | 'failed',
  editorOpen: boolean,
  editingAnimation: number,
  error: string | null,
};

const initialState: AnimationsState = {
  animations: {},
  selectedAnimation: 0,
  status: 'idle',
  editorOpen: false,
  editingAnimation: 0,
  error: null,
};

const createAppAsyncThunk = createAsyncThunk.withTypes<{
  state: RootState,
  dispatch: AppDispatch,
  rejectValue: string,
  extra: AxiosInstance
}>();

export const selectAnimation = createAppAsyncThunk<number, number>(
  'animations/selectAnimation', 
  (animationId, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const date = new Date();
    date.setTime(date.getTime() - date.getTimezoneOffset() * 60 * 1000);

    const selectionPayload = {
      light_pattern_id: animationId,
      timestamp: date.toISOString(),
    };
    const updatePayload = {
      light_pattern_id: animationId,
    };

    return axios.all([
      axiosInstance.post('/api/selections/', selectionPayload),
      axiosInstance.post('/api/selections/updatepi/', updatePayload),
    ])
      .then(axios.spread((res1, res2) => animationId))
  }
);

export const getAnimations = createAppAsyncThunk<AnimationsMap>(
  'animations/getAnimations',
  async (_, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const res = await axiosInstance.get('/api/options/');
    return Object.fromEntries(res.data.map((a: Animation) => [a.id, a]));
  }
);

export const getSelectedAnimation = createAppAsyncThunk<number>(
  'animations/getSelectedAnimation',
  async (_, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const res = await axiosInstance.get('/api/selections/last/');
    return res.data.light_pattern_id;
  }
);

export const resetParameters = createAppAsyncThunk<void, number>(
  'animations/resetParameters',
  (animationId, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const resetPayload = {
      light_pattern_id: animationId,
    };

    return axiosInstance.post('/api/options/reset_parameters/', resetPayload);
  }
)

export const updateParameters = createAppAsyncThunk<void, {animationId: number, newParams: {}}>(
  'animations/updateParameters',
  ({animationId, newParams}, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const updatePayload = {
      light_pattern_id: animationId,
      parameters: newParams,
    };

    return axiosInstance.post('/api/options/update_parameters/', updatePayload);
  }
)

export const animationSlice = createSlice({
  name: 'animation',
  initialState: initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    openEditor: (state, action) => {
      state.editorOpen = true;
      state.editingAnimation = action.payload;
    },
    closeEditor: (state) => {
      state.editorOpen = false;
    }
  },
  extraReducers(builder) {
    builder
      .addCase(selectAnimation.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.selectedAnimation = action.payload;
      })
      .addCase(selectAnimation.rejected, (state, action) => {
        state.status = 'failed'
        state.error = action.error.message || null;
      })
      .addCase(getAnimations.pending, (state, _) => {
        state.status = 'loading';
      })
      .addCase(getAnimations.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.animations = action.payload;
      })
      .addCase(getSelectedAnimation.fulfilled, (state, action) => {
        state.selectedAnimation = action.payload;
      })
      .addMatcher(isRejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message || null;
      })
      .addMatcher(isPending, (state, _) => {
        state.error = null;
      })
  }
});

export const { clearError, openEditor, closeEditor } = animationSlice.actions;

export default animationSlice.reducer;

export const selectAllAnimations = (state: RootState) => state.animation.animations;

export const selectAnimationById = (animationId: number) => (state: RootState) => state.animation.animations[animationId];

export const selectSelectedAnimation = (state: RootState) => state.animation.selectedAnimation;

export const selectStatus = (state: RootState) => state.animation.status;

export const selectError = (state: RootState) => state.animation.error;

export const selectEditorOpen = (state: RootState) => state.animation.editorOpen;

export const selectEditingAnimation = (state: RootState) => state.animation.editingAnimation;