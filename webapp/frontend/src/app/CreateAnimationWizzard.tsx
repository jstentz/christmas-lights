"use client";

import { Dialog, Button, Code, TextField, Text, TextArea } from "@radix-ui/themes";
import { FC, useState, MouseEvent, FormEvent, useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/hooks/hooks";
import { selectGeneratedAnimationId, selectStatus, generateAnimation, previewGeneratedAnimation } from "@/reducers/animationsReducer";
import { PlusCircledIcon, GearIcon, ReloadIcon } from "@radix-ui/react-icons";

export type CreateAnimationWizzard = {};

export const CreateAnimationWizzard: FC<CreateAnimationWizzard> = () => {
  const dispatch = useAppDispatch();
  const [screen, setScreen] = useState(0);
  const [prompt, setPrompt] = useState("");
  const [animationTitle, setAnimationTitle] = useState("");
  const [animationAuthor, setAnimationAuthor] = useState("");

  const status = useAppSelector(selectStatus);
  const generatedAnimationId = useAppSelector(selectGeneratedAnimationId);

  const maxPromptLength = Number(process.env.NEXT_PUBLIC_MAX_PROMPT_LENGTH);
  const promptScreen = 
    <form onSubmit={() => {}}>
      <label>
        <div className="pb-1"><Text size="2" color="gray">Please describe the kind of animation you would like to see ({prompt.length}/{maxPromptLength})</Text></div>
      </label>
      <TextArea 
        value={prompt} 
        maxLength={maxPromptLength} 
        onChange={(e) => setPrompt(e.target.value)} 
        placeholder={process.env.NEXT_PUBLIC_PROMPT_PLACEHOLDER}
      />
    </form>
  const promptNext = (e: MouseEvent) => {
    dispatch(generateAnimation(prompt));
    handleNext(e);
  };

  const waitingScreen = 
    <div className="flex flex-col items-center">
      <GearIcon width="50" height="50" color="black" className="animate-spin" />
      <p>Loading...</p>
    </div>

  const maxTitleLength = Number(process.env.NEXT_PUBLIC_MAX_TITLE_LENGTH);
  const maxAuthorNameLength = Number(process.env.NEXT_PUBLIC_MAX_AUTHOR_LENGTH);
  const previewScreen = 
    <div>
      <p>Done! Your animation should be playing on the tree now</p>
      <p>If not, you can try reloading the animation using this button</p>
      <ReloadIcon color="black" />
      <form>
        Want to see your animation on the homepage? Fill out the fields below!
        <label>
          <div className="pb-1"><Text size="2" color="gray">Animation title ({animationTitle.length}/{maxTitleLength})</Text></div>
        </label>
        <TextField.Input maxLength={maxTitleLength} value={animationTitle} onChange={(e) => setAnimationTitle(e.target.value)} />
        <label>
          <div className="pb-1"><Text size="2" color="gray">Your name ({animationAuthor.length}/{maxAuthorNameLength})</Text></div>
        </label>
        <TextField.Input maxLength={maxAuthorNameLength} value={animationAuthor} onChange={(e) => setAnimationAuthor(e.target.value)} />
      </form>
    </div>

  const screens = [promptScreen, waitingScreen, previewScreen];

  const handleBack = (e: MouseEvent | null) => {
    setScreen((oldScreen) => (oldScreen > 0) ? oldScreen - 1 : oldScreen);
  };

  const handleNext = (e: MouseEvent | null) => {
    setScreen((oldScreen) => (oldScreen < screens.length - 1) ? oldScreen + 1 : oldScreen);
  };

  useEffect(() => {
    if(status == 'succeeded-generate') {
      dispatch(previewGeneratedAnimation(generatedAnimationId));
      setScreen((oldScreen) => (oldScreen < screens.length - 1) ? oldScreen + 1 : oldScreen);
    }
  }, [status, dispatch, generatedAnimationId, setScreen]);

  return (
    <Dialog.Root>
      <Dialog.Trigger>
        <PlusCircledIcon height={25} width={25} color="white" />
      </Dialog.Trigger>
      <Dialog.Content onOpenAutoFocus={(e) => e.preventDefault()}>
        <Dialog.Title>Create a new animation!</Dialog.Title>
        {screens[screen]}
        <div className="flex justify-between pt-2">
          <Dialog.Close>
            <Button variant="soft" color="red">Cancel</Button>
          </Dialog.Close>
          <div className="flex justify-end gap-2">
            {screen != 0 ?
              <Button variant="soft" color="gray" onClick={handleBack}>
                Back
              </Button>
            : null}
            {screen == 0 ? 
              <Button variant="soft" color="green" onClick={promptNext}>
                Next
              </Button>
            : null}
          </div>
      </div>
      </Dialog.Content>
    </Dialog.Root>
  );
};