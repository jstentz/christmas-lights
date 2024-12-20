"use client";

import { FC, useCallback, useEffect, useState, MouseEvent } from "react";
import { ReloadIcon, StopIcon } from "@radix-ui/react-icons";
import { Text, TextField, Button, Separator } from "@radix-ui/themes";
import { useAppDispatch, useAppSelector } from "@/hooks/hooks";
import { previewGeneratedAnimation, selectGeneratedAnimation, selectStatus, submitGeneratedAnimation, restartSelectedAnimation } from "@/reducers/animationsReducer";

export type SubmitScreen = {
  onReset: () => void,
  onClose: () => void,
  hidden: boolean,
};

export const SubmitScreen: FC<SubmitScreen> = ({onReset, onClose, hidden}) => {
  const dispatch = useAppDispatch();
  const [animationTitle, setAnimationTitle] = useState("");
  const [animationAuthor, setAnimationAuthor] = useState("");

  const generatedAnimation = useAppSelector(selectGeneratedAnimation);

  const handleSubmit = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if(generatedAnimation) {
      dispatch(submitGeneratedAnimation({generatedAnimationId: generatedAnimation.id, title: animationTitle, author: animationAuthor}));
    }
    onClose();
  };

  const handleReset = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onReset();
  };

  const handleClose = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onClose();
  };

  const maxTitleLength = Number(process.env.NEXT_PUBLIC_MAX_TITLE_LENGTH);
  const maxAuthorNameLength = Number(process.env.NEXT_PUBLIC_MAX_AUTHOR_LENGTH);

  const submitScreen = (
    <div>
      <form>
        Want your animation featured on the homepage? Fill out the fields below!
        <label>
          <div className="pb-1"><Text size="2" color="gray">Animation title ({animationTitle.length}/{maxTitleLength})</Text></div>
        </label>
        <TextField.Input maxLength={maxTitleLength} value={animationTitle} onChange={(e) => setAnimationTitle(e.target.value)} />
        <label>
          <div className="pb-1"><Text size="2" color="gray">Your name ({animationAuthor.length}/{maxAuthorNameLength})</Text></div>
        </label>
        <TextField.Input maxLength={maxAuthorNameLength} value={animationAuthor} onChange={(e) => setAnimationAuthor(e.target.value)} />
      </form>
      <div className="flex justify-between pt-4">
        <div className="flex justify-start gap-2">
        <Button variant="soft" color="red" onClick={handleClose}>
          Cancel
        </Button>
        <Button variant="soft" color="gray" onClick={handleReset}>
          Restart
        </Button>
        </div>
        <Button variant="soft" color="green" onClick={handleSubmit}>
          Submit
        </Button>
      </div>
    </div>
  );

  return hidden ? <></> : submitScreen;
};