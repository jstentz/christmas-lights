"use client";

import { FC, useEffect } from "react";
import { Button, Dialog } from "@radix-ui/themes";
import { GearIcon } from "@radix-ui/react-icons";
import { useAppSelector } from "@/hooks/hooks";
import { selectStatus } from "@/reducers/animationsReducer";

export type WaitingScreen = {
  onNext: () => void,
  onBack: () => void,
  onReset: () => void,
  hidden: boolean,
};

export const WaitingScreen: FC<WaitingScreen> = ({onNext, hidden}) => {
  const status = useAppSelector(selectStatus);

  useEffect(() => {
    if(status == 'succeeded-generate') {
      onNext();
    }
  }, [status, onNext]);

  const waitingScreen = (
    <div>
      <div className="flex flex-col items-center">
        <GearIcon width="50" height="50" color="black" className="animate-spin" />
        <p>Generating...</p>
        <p>Can take upwards of 30 seconds</p>
      </div>
      <div className="flex justify-between pt-4">
        <Dialog.Close>
          <Button variant="soft" color="red">Cancel</Button>
        </Dialog.Close>
      </div>
    </div>
  );

  return hidden ? <></> : waitingScreen;
};