"use client";

import React, { useEffect, useState } from 'react';
import AnimationCard from "./AnimationCard";
import ErrorMessage from './ErrorMessage';
import { useSearchParams } from 'next/navigation';
import axios from "axios";

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

const Home = () => {
  const [lightPatternDict, setLightPatternDict] = useState<LightPatternList>({});
  const [selectedLightPattern, setSelectedLightPattern] = useState<number|null>(null);
  const [errorMessage, setErrorMessage] = useState<ErrorState>({ message: "", hidden: true });

  const password = useSearchParams().get('p');
  const instance = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_BASE_URL
  });
  instance.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  instance.defaults.xsrfCookieName = "csrftoken";
  instance.defaults.headers.common['API_AUTH'] = password;

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [res1, res2] = await axios.all([
          instance.get("/api/options/"),
          instance.get("/api/selections/last/")
        ]);
        const lightPatternDict = convertToDict(res1.data);
        const lightPatternSelection = res2.data.light_pattern_id;
        setLightPatternDict(lightPatternDict);
        setSelectedLightPattern(lightPatternSelection);
      } catch (err) {
        handleAxiosError(err);
      }
    };
    fetchData();
  }, []);

  const convertToDict = (lpList: Array<LightPattern>) => {
    const lightPatternDict: LightPatternList = {};
    for (let i = 0; i < lpList.length; i++) {
      lightPatternDict[lpList[i].id] = lpList[i];
    }
    return lightPatternDict;
  };

  const getSelectedLightPattern = () => {
    instance
      .get("/api/selections/last/")
      .then((res) => setSelectedLightPattern(res.data.light_pattern_id))
      .catch((err) => handleAxiosError(err));
  };

  const handleSelection = (selection_id: number, selection_name: string) => {
    const date = new Date();
    date.setTime(date.getTime()-date.getTimezoneOffset()*60*1000);
    const selection = {
      light_pattern_id: selection_id,
      timestamp: date.toISOString(),
    };

    instance
      .post("/api/selections/", selection)
      .then(() => getSelectedLightPattern())
      .catch((err) => handleAxiosError(err));

      instance
      .post("/api/selections/updatepi/", { "light_pattern_id": selection_id, "light_pattern_name": selection_name })
      .catch((err) => handleAxiosError(err));
  };

  const handleResetParameters = (selection_id: number, selection_name: string) => {
    console.log(lightPatternDict);
    instance
      .post("/api/options/reset_parameters/", { "light_pattern_id": selection_id, "light_pattern_name": selection_name })
      .catch((err) => handleAxiosError(err));
  };

  const handleEditParameters = (selection_id: number, selection_name: string, new_params: any) => {
    instance
      .post("/api/options/update_parameters/", { "light_pattern_id": selection_id, "light_pattern_name": selection_name, "parameters": new_params })
      .catch((err) => handleAxiosError(err));
  };

  const handleAxiosError = (err: any) => {
    setErrorMessage({ message: err.response.data, hidden: false });
  };

  const handleErrorClose = () => {
    setErrorMessage({ message: "", hidden: true });
  };

  const renderChoices = () => {
    let selectionText, selectionDescription;
    if (selectedLightPattern === null || lightPatternDict === null || Object.keys(lightPatternDict).length === 0) {
      selectionText = "None! Select one below.";
      selectionDescription = "None! Select one below.";
    } else {
      selectionText = lightPatternDict[selectedLightPattern].title;
      selectionDescription = lightPatternDict[selectedLightPattern].description;
    }
    const lightPatternList = Object.values(lightPatternDict).sort((a, b) => a.position - b.position);

    return (
      <div className="bg-gray-200 p-4">
        <ErrorMessage 
          message={errorMessage.message} 
          hide={errorMessage.hidden} 
          errorMessageCloseCallback={handleErrorClose} 
        />
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
              selectionCallback={handleSelection}
              resetParametersCallback={handleResetParameters}
              editParametersCallback={handleEditParameters}
              params={choice.parameters_json}
              default_params={choice.default_parameters_json}
              name={choice.title} 
              image_url={choice.image_url} 
              key={choice.id} 
              light_id={choice.id} 
              light_name={choice.animation_id}/>
            )}
        </div>
    </div>
    );
  };

  return renderChoices();
};

export default Home;