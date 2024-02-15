"use client";

import { Dialog, Button, Code, TextField, Text } from "@radix-ui/themes";
import * as Form from '@radix-ui/react-form';
import { FC, useState, MouseEvent, FormEvent } from "react";
import { updateParameters, resetParameters } from "@/reducers/animationsReducer";
import { useAppDispatch } from "@/hooks/hooks";

export type EditDialog = {
  animationId: number,
  animationTitle: string,
  parameters: {[index: string]: string},
  defaultParameters: {[index: string]: string},
  onClose: () => void,
};

export const EditDialog: FC<EditDialog> = ({animationId, animationTitle, parameters, defaultParameters, onClose}) => {
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
    <Dialog.Root open={true} defaultOpen={true}>
      <Dialog.Content>
        <Dialog.Title>Edit parameters for <Code>{animationTitle}</Code></Dialog.Title>
        <Form.Root onSubmit={handleSubmit}>
          {Object.entries(parameters).map(([key, _]) => (
            <Form.Field name={key} className="pb-2" key={key}>
              <Form.Label>
                <div className="pb-1"><Text size="2" color="gray">{key}</Text></div>
              </Form.Label>
              <Form.Control asChild><TextField.Input value={newParameters[key]} onChange={(e) => handleOnChange(key, e)}/></Form.Control>
            </Form.Field>
          ))}
          <div className="flex justify-between pt-2">
            <Button variant="soft" color="red" onClick={handleReset}>
              Reset
            </Button>
            <div className="flex justify-end gap-2">
              <Dialog.Close>
                <Button variant="soft" color="gray" onClick={() => onClose()}>
                  Close
                </Button>
              </Dialog.Close>
              <Form.FormSubmit asChild>
                <Button variant="soft" color="green">Save</Button>
              </Form.FormSubmit>
            </div>
          </div>
        </Form.Root>
      </Dialog.Content>
    </Dialog.Root>
  )
};