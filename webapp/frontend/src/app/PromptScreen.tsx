"use client";

import { FC, useState, useCallback } from "react";
import { useAppDispatch } from "@/hooks/hooks";
import { generateAnimation } from "@/reducers/animationsReducer";
import { TextArea, Button } from "@radix-ui/themes";
import { MouseEvent } from "react";
import { ExclamationTriangleIcon } from "@radix-ui/react-icons";

export type PromptScreen = {
  onNext: () => void,
  onBack: () => void,
  onClose: () => void,
  hidden: boolean,
};

export const PromptScreen: FC<PromptScreen> = ({onNext, onClose, hidden}) => {
  const dispatch = useAppDispatch();
  const [prompt, setPrompt] = useState("");

  const submitPrompt = useCallback((prompt: string) => {
    dispatch(generateAnimation(prompt));
    onNext();
  }, [onNext, dispatch]);

  const onPromptNext = (e: MouseEvent) => {
    e.stopPropagation();
    submitPrompt(prompt);
  };

  const onPromptClose = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onClose();
  }

  const maxPromptLength = Number(process.env.NEXT_PUBLIC_MAX_PROMPT_LENGTH);
  const promptScreen = (
    <form onSubmit={() => {}}>
      <label>
        <div className="p-1"><p className="text-sm">Please describe the kind of animation you would like to create ({prompt.length}/{maxPromptLength})</p></div>
      </label>
      <TextArea 
        value={prompt} 
        maxLength={maxPromptLength} 
        onChange={(e) => setPrompt(e.target.value)} 
        placeholder={process.env.NEXT_PUBLIC_PROMPT_PLACEHOLDER}
        className="h-32"
      />
      <div className="flex flex-col items-center pt-4">
        <div className="flex items-center gap-1 w-full bg-red-400 p-1 pl-2">
          <ExclamationTriangleIcon color="white" />
          <p className="text-white font-semibold">Warning!</p>
        </div>
        <div className="bg-red-200 p-2">
          <p className="text-sm">Generated animations may contain flashing lights, which can trigger seizures for people with photosensitive epilepsy</p>
        </div>
      </div>
      <div className="flex justify-between pt-4">
        <Button variant="soft" color="red" onClick={onPromptClose}>Cancel</Button>
        <div className="flex justify-end gap-2">
          <Button variant="soft" color="green" onClick={onPromptNext}>
            Next
          </Button>
        </div>
      </div>
  </form>
  );
  
  return hidden ? <></> : promptScreen
};