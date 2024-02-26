"use client";

import { FC, useEffect, MouseEvent } from "react";
import { Button } from "@radix-ui/themes";
import { GearIcon } from "@radix-ui/react-icons";
import { useAppSelector } from "@/hooks/hooks";
import { selectStatus } from "@/reducers/animationsReducer";

export type WaitingScreen = {
  onNext: () => void,
  onClose: () => void,
  hidden: boolean,
};

export const WaitingScreen: FC<WaitingScreen> = ({onNext, onClose, hidden}) => {
  const status = useAppSelector(selectStatus);

  useEffect(() => {
    if(!hidden && status == 'succeeded-generate') {
      onNext();
    }
  }, [status, hidden, onNext]);

  const handleClose = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onClose();
  }

  const waitingScreen = (
    <div>
      <div className="flex flex-col items-center">
        <GearIcon width="50" height="50" color="black" className="animate-spin" />
        <p>Generating...</p>
        <p>Can take upwards of 30 seconds</p>
      </div>
      <div className="flex justify-between pt-4">
        <Button variant="soft" color="red" onClick={handleClose}>Cancel</Button>
      </div>
    </div>
  );

  return hidden ? <></> : waitingScreen;
};