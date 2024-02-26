"use client";

import { Dialog } from "@radix-ui/themes";
import { FC, useState, useCallback, useEffect } from "react";
import { PlusCircledIcon } from "@radix-ui/react-icons";
import { PromptScreen } from "./PromptScreen";
import { WaitingScreen } from "./WaitingScreen";
import { SubmitScreen } from "./SubmitScreen";

export type CreateAnimationWizard = {};

export const CreateAnimationWizard: FC<CreateAnimationWizard> = () => {
  const [open, setOpen] = useState(false);
  const [screen, setScreen] = useState(0);

  const handleBack = useCallback(() => {
    setScreen((oldScreen) => (oldScreen > 0) ? oldScreen - 1 : oldScreen);
  }, [setScreen]);

  const handleNext = useCallback(() => {
    setScreen((oldScreen) => oldScreen + 1);
  }, [setScreen]);

  const handleReset = useCallback(() => {
    setScreen(0);
  }, [setScreen]);

  const handleClose = useCallback(() => {
    setScreen(0);
    setOpen(false);
  }, [setOpen, setScreen]);

  const handleOnOpenChange = useCallback((open: boolean) => {
    setOpen(open);
    if(!open) {
      setScreen(0);
    }
  }, [setOpen, setScreen]);

  const promptScreen = <PromptScreen onNext={handleNext} onBack={handleBack} onClose={handleClose} hidden={screen != 0} />;
  const waitingScreen = <WaitingScreen onNext={handleNext} onClose={handleClose} hidden={screen != 1} />;
  const submitScreen = <SubmitScreen onReset={handleReset} onClose={handleClose} hidden={screen != 2} />;

  return (
    <Dialog.Root open={open} onOpenChange={handleOnOpenChange}>
      <Dialog.Trigger>
        <PlusCircledIcon height={25} width={25} color="white" />
      </Dialog.Trigger>
      <Dialog.Content onOpenAutoFocus={(e) => e.preventDefault()}>
        <Dialog.Title>Create a new animation!</Dialog.Title>
        {promptScreen}
        {waitingScreen}
        {submitScreen}
      </Dialog.Content>
    </Dialog.Root>
  );
};