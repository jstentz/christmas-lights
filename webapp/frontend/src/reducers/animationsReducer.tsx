import { createAsyncThunk, createSlice, isPending, isRejectedWithValue } from "@reduxjs/toolkit";
import axios, { AxiosInstance } from "axios";
import { AppDispatch, RootState } from "@/lib/store";

export type AnimationParams = {
  [index: string]: string,
}

export type Animation = {
  id: number,
  animation_id: number,
  image_url: string,
  parameters_json: AnimationParams,
  default_parameters_json: AnimationParams,
  title: string,
  description: string,
  position: number,
};

export type GeneratedAnimation = {
  id: number,
  parameters_json: AnimationParams
};

export type AnimationsMap = {
  [index: number]: Animation,
}

export type AnimationsState = {
  animations: AnimationsMap,
  selectedAnimation: number,
  status: 'idle' | 'loading' | 'succeeded' | 'failed' | 'succeeded-generate',
  error: string | null,
  generate: {
    generatedAnimation: GeneratedAnimation | null,
    status: 'idle' | 'loading' | 'generated' | 'failed'
  },
};

const initialState: AnimationsState = {
  animations: {},
  selectedAnimation: 0,
  status: 'idle',
  error: null,
  generate: {
    generatedAnimation: null,
    status: 'idle',
  }
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
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
);

export const restartSelectedAnimation = createAppAsyncThunk<void, void>(
  'animations/restartSelectedAnimation',
  (_, thunkAPI) => {
    thunkAPI.dispatch(selectAnimation(thunkAPI.getState().animation.selectedAnimation));
  }
);

export const getAnimations = createAppAsyncThunk<AnimationsMap>(
  'animations/getAnimations',
  (_, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    return axiosInstance.get('/api/options/')
      .then((res) => Object.fromEntries(res.data.map((a: Animation) => [a.id, a])))
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
);

export const getSelectedAnimation = createAppAsyncThunk<number>(
  'animations/getSelectedAnimation',
  (_, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    return axiosInstance.get('/api/selections/last/')
      .then((res) => res.data.light_pattern_id)
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
);

export const resetParameters = createAppAsyncThunk<void, number>(
  'animations/resetParameters',
  (animationId, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const resetPayload = {
      light_pattern_id: animationId,
    };

    return axiosInstance.post('/api/options/reset_parameters/', resetPayload)
      .then(() => {})
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
);

export const updateParameters = createAppAsyncThunk<{animationId: number, params: AnimationParams}, {animationId: number, newParams: AnimationParams}>(
  'animations/updateParameters',
  ({animationId, newParams}, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const updatePayload = {
      light_pattern_id: animationId,
      parameters: newParams,
    };

    return axiosInstance.post('/api/options/update_parameters/', updatePayload)
      .then(() => ({animationId: animationId, params: newParams}))
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
);

export const generateAnimation = createAppAsyncThunk<GeneratedAnimation, string>(
  'animations/generate/generateAnimation',
  (prompt, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const generatePayload = {
      prompt: prompt,
    };

    return axiosInstance.post('/api/generate/generate/', generatePayload)
      .then((res) => JSON.parse(res.data))
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
);

export const previewGeneratedAnimation = createAppAsyncThunk<void, number>(
  'animations/generate/previewGeneratedAnimation',
  (generatedAnimationId, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const previewPayload = {
      id: generatedAnimationId,
    };

    return axiosInstance.post('/api/generate/preview/', previewPayload)
      .then(() => {})
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
);

export const updateGeneratedAnimationParameters = createAppAsyncThunk<void, {generatedAnimationId: number, parameters_json: AnimationParams}>(
  'animations/generate/updateGeneratedAnimationParameters',
  ({generatedAnimationId, parameters_json}, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const updatePayload = {
      id: generatedAnimationId,
      parameters_json: parameters_json
    };

    return axiosInstance.post('/api/generate/update_parameters/', updatePayload)
      .then(() => {})
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
)

export const submitGeneratedAnimation = createAppAsyncThunk<void, {generatedAnimationId: number, title: string, author: string}>(
  'animations/generate/submitGeneratedAnimation',
  ({generatedAnimationId, title, author}, thunkAPI) => {
    const axiosInstance = thunkAPI.extra;
    const submitPayload = {
      id: generatedAnimationId,
      title: title,
      author: author,
    };

    return axiosInstance.post('/api/generate/submit/', submitPayload)
      .then(() => {})
      .catch((err) => thunkAPI.rejectWithValue(err.response.data));
  }
);

export const animationSlice = createSlice({
  name: 'animation',
  initialState: initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
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
      .addCase(updateParameters.fulfilled, (state, action) => {
        state.animations[action.payload.animationId].parameters_json = action.payload.params;
      })
      .addCase(generateAnimation.pending, (state, _) => {
        state.status = 'loading';
      })
      .addCase(generateAnimation.fulfilled, (state, action) => {
        state.generate.status = 'generated';
        state.generate.generatedAnimation = action.payload;
      })
      .addCase(previewGeneratedAnimation.pending, (state, _) => {
        state.generate.status = 'idle';
      })
      .addMatcher(isRejectedWithValue, (state, action) => {
        state.status = 'failed';
        state.error = action.payload as string;
      })
      .addMatcher(isPending, (state, _) => {
        state.error = null;
      })
  }
});

export const { clearError } = animationSlice.actions;

export default animationSlice.reducer;

export const selectAllAnimations = (state: RootState) => state.animation.animations;

export const selectSelectedAnimation = (state: RootState) => state.animation.selectedAnimation;

export const selectStatus = (state: RootState) => state.animation.status;

export const selectError = (state: RootState) => state.animation.error;

export const selectGeneratedAnimation = (state: RootState) => state.animation.generate.generatedAnimation;

export const selectGenerateStatus = (state: RootState) => state.animation.generate.status;