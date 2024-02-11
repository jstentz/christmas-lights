import React, { useCallback, useEffect, createContext, useState } from "react";

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

export type AnimationMap = {
  [index: number]: Animation
};

export type Status = {
  error: boolean,
  message: string | null
};

function fetchAPI(path: string, method: string, body: string | null, apiAuth: string, headers: HeadersInit | null = null) {
  return fetch(process.env.NEXT_PUBLIC_API_BASE_URL + path, {
    method: method,
    headers: {
      ...headers,
      API_AUTH: apiAuth
    },
    body: body,
  });
}

function getAPI(path: string, apiAuth: string, headers: HeadersInit | null = null) {
  return fetchAPI(path, "GET", null, apiAuth, headers);
}

function postAPI(path: string, body: string, apiAuth: string, headers : HeadersInit | null = null) {
  return fetchAPI(path, "POST", body, apiAuth, {...headers, "Content-Type": 'application/json'});
}

export type BackendAPI = {
  animations: AnimationMap,
  selectedAnimation: number | null,
  selectAnimation: (animation_id: number) => void,
  resetParameters: (animation_id: number) => void,
  updateParameters: (animation_id: number, new_params: {}) => void,
  status: Status,
  clearStatus: () => void,
}

export const BackendContext = createContext<BackendAPI | null>(null);

type BackendContextProvider = {
  apiAuth: string
};

export function BackendContextProvider({ children, apiAuth } : React.PropsWithChildren<BackendContextProvider>) {
  /* Define local state for the backend. */
  const [animations, setAnimations] = useState<AnimationMap>({});
  const [selectedAnimation, setSelectedAnimation] = useState<number | null>(null);
  const [status, setStatus] = useState<Status>({error: false, message: ""});

  /* Define the backend functions. */
  const selectAnimation = useCallback(
    (animation_id: number) => {
      const date = new Date();
      date.setTime(date.getTime() - date.getTimezoneOffset() * 60 * 1000);
      const selectionPayload = {
        light_pattern_id: animation_id,
        timestamp: date.toISOString(),
      };

      postAPI("/api/selections/", JSON.stringify(selectionPayload), apiAuth)
        .then(() => setSelectedAnimation(animation_id))
        .catch((err) => setStatus({message: err, error: true}));

      const updatePayload = {
        light_pattern_id: animation_id,
        light_pattern_name: animations[animation_id].animation_id,
      };

      postAPI("/api/selections/updatepi/", JSON.stringify(updatePayload), apiAuth)
        .catch((err) => setStatus({message: err, error: true}));
    }, 
    [animations, setSelectedAnimation, setStatus, apiAuth]);

  const getAnimations = useCallback(
    async () => {
      const res = await getAPI("/api/options/", apiAuth);
      res.json()
        .then((obj) => {
          const test = obj.map((e: Animation) => [e.id, e]);
          setAnimations(Object.fromEntries(test));
        })
        .catch((err) => setStatus({message: err, error: true}));
    },
  [setAnimations, setStatus, apiAuth]);

  const getSelectedAnimation = useCallback(
    async () => {
      const res = await getAPI("/api/selections/last/", apiAuth);
      res.json()
        .then((obj) => {
          setSelectedAnimation(obj.light_pattern_id);
        })
        .catch((err) => setStatus({message: err, error: true}));
    },
    [setSelectedAnimation, setStatus, apiAuth]
  );

  const resetParameters = useCallback(
    async (animation_id: number) => {
      const resetPayload = {
        light_pattern_id: animation_id,
      };
      const res = await postAPI("/api/options/reset_parameters/", JSON.stringify(resetPayload), apiAuth)
      if(!res.ok) {
        res.text().then((message) => setStatus({message: message, error: true}));
      }
    },
    [animations, setStatus, apiAuth]
  );

  const updateParameters = useCallback(
    async (animation_id: number, new_params: {}) => {
      const updatePayload = {
        light_pattern_id: animation_id,
        parameters: new_params,
      };
      const res = await postAPI("/api/options/update_parameters/", JSON.stringify(updatePayload), apiAuth);
      if(!res.ok) {
          res.text().then((message) => setStatus({message: message, error: true}));
      }
    },
    [animations, setStatus, apiAuth]
  );

  const clearStatus = useCallback(
    () => {
      setStatus({message: "", error: false});
    },
    [setStatus]
  );

  useEffect(
    () => {
      getAnimations();
      getSelectedAnimation();
    },
    [getAnimations, getSelectedAnimation]
  );

  const exposedData = {
    animations,
    selectedAnimation,
    selectAnimation,
    resetParameters,
    updateParameters,
    status,
    clearStatus,
  };

  return (
    <BackendContext.Provider value={exposedData}>
      {children}
    </BackendContext.Provider>
  );
}