"use client";

import { Dialog, Button, Code, TextField, Text } from "@radix-ui/themes";
import { FC, useState, MouseEvent, FormEvent } from "react";
import { updateParameters, resetParameters } from "@/reducers/animationsReducer";
import { useAppDispatch } from "@/hooks/hooks";

export type CreateAnimationDialog = {};

export const CreateAnimationDialog: FC<CreateAnimationDialog> = () => {
  return (
    <Dialog.Root>
      <Dialog.Content onOpenAutoFocus={(e) => e.preventDefault}>
        <Dialog.Title>Create a new animation!</Dialog.Title>
        <form onSubmit={() => {}}>
          <label htmlFor="prompt">
            <div className="pb-1"><Text size="2" color="gray"></Text></div>
          </label>
        </form>
      </Dialog.Content>
    </Dialog.Root>
  );
};