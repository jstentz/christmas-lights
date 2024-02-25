"use client";

import { useEffect } from "react";
import AnimationCard from "./AnimationCard";
import ErrorMessage from "./ErrorMessage";
import { Header } from "./Header";
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
    <div>
      <Header title="Plaid Family Lights" selectedAnimationName={selectionText} />
    <div className="p-4 pt-20">
      <ErrorMessage />
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4">
        {lightPatternList.map((choice) => 
            <AnimationCard 
              animation={choice}
              key={choice.id}
            />
          )}
      </div>
  </div>
  </div>
  );
}