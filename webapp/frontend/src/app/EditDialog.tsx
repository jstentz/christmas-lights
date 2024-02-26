"use client";

import { Dialog, Button, Code, TextField, Text } from "@radix-ui/themes";
import { FC, useState, MouseEvent, FormEvent } from "react";
import { updateParameters, resetParameters } from "@/reducers/animationsReducer";
import { useAppDispatch } from "@/hooks/hooks";

export type EditDialog = {
  animationId: number,
  animationTitle: string,
  parameters: {[index: string]: string},
  defaultParameters: {[index: string]: string},
  onClose: () => void,
  onOpenChange: (open: boolean) => void,
};

export const EditDialog: FC<EditDialog> = ({animationId, animationTitle, parameters, defaultParameters, onClose, onOpenChange}) => {
  const dispatch = useAppDispatch();
  const [newParameters, setNewParameters] = useState(parameters);

  const handleOnChange = (parameter_key: string, e: any) => {
    setNewParameters((oldParams) => ({
      ...oldParams,
      [parameter_key]: e.target.value,
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dispatch(updateParameters({animationId: animationId, newParams: newParameters}));
    onClose();
  };

  const handleReset = (e: MouseEvent) => {
    e.preventDefault();
    dispatch(resetParameters(animationId));
    setNewParameters(defaultParameters);
  };

  return (
    <Dialog.Root open={true} defaultOpen={false} onOpenChange={onOpenChange}>
      <Dialog.Content onOpenAutoFocus={(e) => e.preventDefault()}>
        <Dialog.Title>Edit parameters for <Code>{animationTitle}</Code></Dialog.Title>
        <form onSubmit={() => {}}>
          {Object.entries(parameters).map(([key, _]) => (
            <div className="pb-2" key={key}>
              <label>
                <div className="pb-1"><Text size="2" color="gray">{key}</Text></div>
              </label>
              <TextField.Input value={newParameters[key]} onChange={(e) => handleOnChange(key, e)}/>
            </div>
          ))}
          <div className="flex justify-between pt-2">
            <div className="flex justify-start gap-2">
              <Button variant="soft" color="red" onClick={() => onClose()}>
                Close
              </Button>
              <Button variant="soft" color="gray" onClick={handleReset}>
                Reset
              </Button>
            </div>
            <Button variant="soft" color="green" onClick={(e) => handleSubmit(e)}>Save</Button>
          </div>
        </form>
      </Dialog.Content>
    </Dialog.Root>
  )
};