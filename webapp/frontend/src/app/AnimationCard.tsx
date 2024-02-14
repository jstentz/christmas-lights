"use client";

import React, { FC, useState } from 'react';
import { selectAnimation, updateParameters, resetParameters } from '@/reducers/animationsReducer';
import { useAppDispatch } from '@/hooks/hooks';
import { Animation } from '@/reducers/animationsReducer';
import { EditDialog } from './EditDialog';

export type AnimationCard = {
  animation: Animation,
};

const AnimationCard: FC<AnimationCard> = ({animation}) => {
  const dispatch = useAppDispatch();
  const [editing, setEditing] = useState(false);
  const [cardClickAnimation, setCardClickAnimation] = useState(false);

  const handleEditButtonClick = (e: any) => {
    e.stopPropagation();
    setEditing(true);
  }

  const handleCancelButtonClick = () => {
    setEditing(false);
  }

  const handleCardClicked = (e: any) => {
    e.stopPropagation();
    if(!editing) {
      setCardClickAnimation(true);
      dispatch(selectAnimation(animation.id));
    }
  };

  const cardClassName = `${cardClickAnimation ? 'animate-click' : ''} relative aspect-4/3 rounded-lg overflow-hidden shadow-md hover:shadow-lg`;

  const displayCard = (
    <div>
    <div className={cardClassName} onClick={handleCardClicked} onAnimationEnd={() => setCardClickAnimation(false)}>
      <img className="w-full h-auto object-cover" src={animation.image_url} alt={animation.title} />
      <div className="absolute top-4 right-4" onClick={handleEditButtonClick}>
        <img className="w-[25px] h-[25px]" src="cog-white.png" alt="edit" />
      </div>
      <div className="px-3 py-2 absolute bottom-0 left-0">
        <p className="font-bold text-white text-xl">{animation.title}</p>
      </div>
      </div>
      {editing ? 
        <EditDialog 
          animationId={animation.id}
          animationTitle={animation.title}
          parameters={animation.parameters_json}
          defaultParameters={animation.default_parameters_json}
          onClose={handleCancelButtonClick}
        /> : <></>}
    </div>
  );

  // const editingCard = (
  //   <div className="bg-gray-300 p-4 w-full aspect-4/3 overflow-auto text-center rounded-lg shadow-md scrollbar-thin scrollbar-thumb-gray-400 scrollbar-track-gray-300">
  //     <form onSubmit={handleParameterEdit}>
  //       <p className="font-bold text-black text-md mb-2">Edit parameters for {animation.animation_id}</p>
  //       {/* TODO: Figure out how to represent this custom style component using tailwind css */}
  //       <div className="grid gap-2 mb-2" style={{gridTemplateColumns: 'auto 1fr'}}>
  //         {Object.entries(animation.parameters_json).map(([key, value]) => (
  //           <React.Fragment key={key}>
  //             <label htmlFor={key} className="text-black text-right text-md">{key}</label>
  //             <input className='w-full text-black text-md px-1' type="text" name={key} value={parameters[key]} onChange={(e) => handleChange(key, e)} />
  //           </React.Fragment>
  //         ))}
  //       </div>
  //       <div className="flex gap-2 justify-center">
  //         <button type="submit" className="bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-2 rounded text-sm">Save</button>
  //         <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-sm" onClick={handleCancelButtonClick}>Cancel</button>
  //         <button className="bg-slate-500 hover:bg-slate-700 text-white font-bold py-1 px-2 rounded text-sm" onClick={handleResetButtonClick}>Reset</button>
  //       </div>

  //     </form>
  //   </div>
  // );

  return displayCard;
}

export default AnimationCard;