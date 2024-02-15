"use client";

import { FC, useState } from 'react';
import { selectAnimation } from '@/reducers/animationsReducer';
import { useAppDispatch } from '@/hooks/hooks';
import { Animation } from '@/reducers/animationsReducer';
import { EditDialog } from './EditDialog';
import { GearIcon } from '@radix-ui/react-icons';

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
        <GearIcon color="white" height={25} width={25} />
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

  return displayCard;
}

export default AnimationCard;