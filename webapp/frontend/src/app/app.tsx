"use client";

import { useEffect } from "react";
import AnimationCard from "./AnimationCard";
import ErrorMessage from "./ErrorMessage";
import { getAnimations, getSelectedAnimation, selectAllAnimations, selectSelectedAnimation, selectStatus } from "@/reducers/animationsReducer";
import { useAppDispatch, useAppSelector } from "@/hooks/hooks";

export const App = () => {

  const status = useAppSelector(selectStatus);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if(status == 'idle') {
      dispatch(getAnimations());
      dispatch(getSelectedAnimation());
    }
  }, [dispatch, status]);

  const animations = useAppSelector(selectAllAnimations);
  const selectedAnimation = useAppSelector(selectSelectedAnimation);

  let selectionText, selectionDescription;
  if (selectedAnimation === 0 || Object.keys(animations).length == 0) {
    selectionText = "None! Select one below.";
    selectionDescription = "None! Select one below.";
  } else {
    selectionText = animations[selectedAnimation].title;
    selectionDescription = animations[selectedAnimation].description;
  }
  const lightPatternList = Object.values(animations).sort((a, b) => a.position - b.position);

  return (
    <div className="bg-gray-200 p-4">
      <ErrorMessage />
      <p className="leading-tight text-center max-w-fit mx-auto text-5xl font-extrabold text-transparent bg-clip-text text-center bg-gradient-to-r from-rose-600 to-green-600">
          Plaid Family Lights
      </p>
      <p className="text-2xl text-center text-slate-800 font-bold">
        Select an animation
      </p>
      <p className="text-lg text-center font-semibold text-slate-700">
        Current Selection: {selectionText}
      </p>
      <p className="pb-4 text-md text-center text-slate-700">
          {selectionDescription}
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4">
        {lightPatternList.map((choice) => 
            <AnimationCard 
              animation={choice}
            />
          )}
      </div>
  </div>
  );
}