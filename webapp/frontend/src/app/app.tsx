"use client";

import { useBackend } from "@/hooks/backend";
import { useState, useEffect } from "react";
import AnimationCard from "./AnimationCard";
import ErrorMessage from "./ErrorMessage";

interface LightPattern {
  id: number,
  animation_id: number,
  image_url: string,
  parameters_json: string,
  default_parameters_json: string,
  title: string, 
  description: string
}

interface LightPatternList {
  [index: number]: LightPattern
}

interface ErrorState {
  message: string,
  hidden: boolean
}

export const App = () => {
  return <div></div>;
  // const {animations, selectedAnimation} = useBackend();

  // let selectionText, selectionDescription;
  // if (selectedAnimation === null || Object.keys(animations).length == 0) {
  //   selectionText = "None! Select one below.";
  //   selectionDescription = "None! Select one below.";
  // } else {
  //   selectionText = animations[selectedAnimation].title;
  //   selectionDescription = animations[selectedAnimation].description;
  // }
  // const lightPatternList = Object.values(animations).sort((a, b) => a.position - b.position);

  // return (
  //   <div className="bg-gray-200 p-4 pt-16">
  //     <ErrorMessage />
  //     <p className="text-lg text-center font-semibold text-slate-700">
  //       Current Selection: {selectionText}
  //     </p>
  //     <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4">
  //       {lightPatternList.map((choice) => 
  //           <AnimationCard 
  //             selectionCallback={() => {}}
  //             resetParametersCallback={() => {}}
  //             editParametersCallback={() => {}}
  //             params={choice.parameters_json}
  //             default_params={choice.default_parameters_json}
  //             name={choice.title} 
  //             image_url={choice.image_url} 
  //             key={choice.id} 
  //             light_id={choice.id} 
  //             light_name={choice.animation_id}
  //           />
  //         )}
  //     </div>
  // </div>
  // );
}