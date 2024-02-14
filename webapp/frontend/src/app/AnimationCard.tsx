"use client";

import React, { useState } from 'react';
import { selectAnimation, updateParameters, resetParameters, openEditor } from '@/reducers/animationsReducer';
import { useAppDispatch } from '@/hooks/hooks';

const AnimationCard = (props: any) => {
  const dispatch = useAppDispatch();
  const [editing, setEditing] = useState(false);
  const [cardClickAnimation, setCardClickAnimation] = useState(false);
  const [parameters, setParameters] = useState(props.params);

  const handleChange = (parameter_key: string, e: any) => {
    setParameters((oldState: any) => ({
      ...oldState,
      [parameter_key]: e.target.value
    }));
  };

  const handleParameterEdit = (e: any) => {
    e.preventDefault();
    setEditing(false);
    dispatch(updateParameters({animationId: props.light_id, newParams: parameters}));
  };

  const handleResetButtonClick = (e: any) => {
    e.stopPropagation();
    dispatch(resetParameters(props.light_id));
    setParameters(props.default_params);
  }

  const handleEditButtonClick = (e: any) => {
    e.stopPropagation();
    dispatch(openEditor(props.light_id));
    // setEditing(true);
  }

  const handleCancelButtonClick = (e: any) => {
    e.stopPropagation();
    setEditing(false);
  }

  const handleCardClicked = (e: any) => {
    e.stopPropagation();
    setCardClickAnimation(true);
    dispatch(selectAnimation(props.light_id));
  };

  const cardClassName = `${cardClickAnimation ? 'animate-click' : ''} relative aspect-4/3 rounded-lg overflow-hidden shadow-md hover:shadow-lg`;

  const displayCard = (
    <div className={cardClassName} onClick={handleCardClicked} onAnimationEnd={() => setCardClickAnimation(false)}>
      <img className="w-full h-auto object-cover" src={props.image_url} alt={props.light_name} />
      <div className="absolute top-4 right-4" onClick={handleEditButtonClick}>
        <img className="w-[25px] h-[25px]" src="cog-white.png" alt="edit" />
      </div>
      <div className="px-3 py-2 absolute bottom-0 left-0">
        <p className="font-bold text-white text-xl">{props.name}</p>
      </div>
    </div>
  );

  const editingCard = (
    <div className="bg-gray-300 p-4 w-full aspect-4/3 overflow-auto text-center rounded-lg shadow-md scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-300">
      <form onSubmit={handleParameterEdit}>
        <p className="font-bold text-black text-md mb-2">Edit parameters for {props.light_name}</p>
        {/* TODO: Figure out how to represent this custom style component using tailwind css */}
        <div className="grid gap-2 mb-2" style={{gridTemplateColumns: 'auto 1fr'}}>
          {Object.entries(props.params).map(([key, value]) => (
            <React.Fragment key={key}>
              <label htmlFor={key} className="text-black text-right text-md">{key}</label>
              <input className='w-full text-black text-md px-1' type="text" name={key} value={parameters[key]} onChange={(e) => handleChange(key, e)} />
            </React.Fragment>
          ))}
        </div>
        <div className="flex gap-2 justify-center">
          <button type="submit" className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded text-sm">Save</button>
          <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-sm" onClick={handleCancelButtonClick}>Cancel</button>
          <button className="bg-slate-500 hover:bg-slate-700 text-white font-bold py-1 px-2 rounded text-sm" onClick={handleResetButtonClick}>Reset</button>
        </div>

      </form>
    </div>
  );

  return editing ? editingCard : displayCard;
}

export default AnimationCard;