"use client";

import { Dialog, Button } from "@radix-ui/themes";
import { FC, useState, useCallback } from "react";
import { PlusCircledIcon } from "@radix-ui/react-icons";
import { PromptScreen } from "./PromptScreen";
import { WaitingScreen } from "./WaitingScreen";
import { SubmitScreen } from "./SubmitScreen";

export type CreateAnimationWizzard = {};

export const CreateAnimationWizzard: FC<CreateAnimationWizzard> = () => {
  const [screen, setScreen] = useState(0);

  const handleBack = useCallback(() => {
    setScreen((oldScreen) => (oldScreen > 0) ? oldScreen - 1 : oldScreen);
  }, [setScreen]);

  const handleNext = useCallback(() => {
    setScreen((oldScreen) => (oldScreen < screens.length - 1) ? oldScreen + 1 : oldScreen);
  }, [setScreen]);

  const handleReset = useCallback(() => {
    setScreen(0);
  }, [setScreen]);

  const promptScreen = <PromptScreen onNext={handleNext} onBack={handleBack} onReset={handleReset} hidden={screen != 0} />;
  const waitingScreen = <WaitingScreen onNext={handleNext} onBack={handleBack} onReset={handleReset} hidden={screen != 1} />;
  const submitScreen = <SubmitScreen onNext={handleNext} onBack={handleBack} onReset={handleReset} hidden={screen != 2} />;

  const screens = [promptScreen, waitingScreen, submitScreen];

  return (
    <Dialog.Root>
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