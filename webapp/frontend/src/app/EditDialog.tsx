"use client";

import { Dialog, Button } from "@radix-ui/themes";
import { FC, useState } from "react";
import { updateParameters } from "@/reducers/animationsReducer";
import { useAppDispatch, useAppSelector } from "@/hooks/hooks";

export type EditDialog = {
  animationId: number,
  animationTitle: string,
  open: boolean,
  parameters: {[index: string]: string},
  defaultParameters: {[index: string]: string},
  onClose: () => void,
};

export const EditDialog: FC<EditDialog> = ({animationId, animationTitle, open, parameters, defaultParameters, onClose}) => {
  const dispatch = useAppDispatch();
  const [newParameters, setNewParameters] = useState(parameters);

  const handleOnClose = (e: any) => {
    e.stopPropagation();
    onClose();
  }

  return (
    <Dialog.Root open={open}>
      <Dialog.Content>
        <Dialog.Title>Users</Dialog.Title>
        <Dialog.Description>
          Edit parameters for {animationTitle}
        </Dialog.Description>
        {Object.entries(parameters).map(([key, _]) => (
          <div>
            <p>{key}</p>
            <p>{parameters[key]}</p>
          </div>
        ))}
        <Dialog.Close onClick={handleOnClose}>
          <Button variant="soft" color="gray">
            Close
          </Button>
        </Dialog.Close>
      </Dialog.Content>
    </Dialog.Root>
  )
};