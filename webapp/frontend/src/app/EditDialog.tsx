"use client";

import { Dialog, Button } from "@radix-ui/themes";
import { FC } from "react";
import { selectEditorOpen, closeEditor, selectAnimationById, selectEditingAnimation } from "@/reducers/animationsReducer";
import { useAppDispatch, useAppSelector } from "@/hooks/hooks";

export type EditDialog = {};

export const EditDialog: FC<EditDialog> = (props) => {
  const dispatch = useAppDispatch();
  const open = useAppSelector(selectEditorOpen);
  const animationId = useAppSelector(selectEditingAnimation);
  const animation = useAppSelector(selectAnimationById(animationId))

  return (
    <Dialog.Root open={open}>
      <Dialog.Content>
        <Dialog.Title>Users</Dialog.Title>
        <Dialog.Description>
          The following users have access to this project.
        </Dialog.Description>
        <p>{open ? animation.description : ""}</p>
        <Dialog.Close onClick={() => dispatch(closeEditor())}>
          <Button variant="soft" color="gray">
            Close
          </Button>
        </Dialog.Close>
      </Dialog.Content>
    </Dialog.Root>
  )
};