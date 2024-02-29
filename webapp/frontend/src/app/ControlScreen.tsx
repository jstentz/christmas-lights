"use client";

import { FC, useCallback, useEffect, useState, MouseEvent } from "react";
import { ReloadIcon, StopIcon } from "@radix-ui/react-icons";
import { Text, TextField, Button, Separator } from "@radix-ui/themes";
import { useAppDispatch, useAppSelector } from "@/hooks/hooks";
import { previewGeneratedAnimation, selectGeneratedAnimation, selectGenerateStatus, submitGeneratedAnimation, restartSelectedAnimation, generateAnimation } from "@/reducers/animationsReducer";

export type ControlScreen = {
  onNext: () => void,
  onReset: () => void,
  onClose: () => void,
  hidden: boolean,
};

export const ControlScreen: FC<ControlScreen> = ({onNext, onReset, onClose, hidden}) => {
  const dispatch = useAppDispatch();

  const generatedAnimation = useAppSelector(selectGeneratedAnimation);
  const status = useAppSelector(selectGenerateStatus);

  const [newParameters, setNewParameters] = useState(generatedAnimation?.parameters_json || {});

  const previewAnimation = useCallback((animationId: number) => {
    dispatch(previewGeneratedAnimation(animationId));
  }, [dispatch]);

  useEffect(() => {
    if(!hidden && status == 'generated' && generatedAnimation) {
      previewAnimation(generatedAnimation.id);
      setNewParameters(generatedAnimation.parameters_json);
    }
  }, [previewAnimation, generatedAnimation, hidden, status, setNewParameters]);

  const handleNext = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onNext();
  };
  
  const handleReset = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onReset();
  };

  const handleClose = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    onClose();
  };

  const handleStop = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    dispatch(restartSelectedAnimation());
  };

  const handleRestart = (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if(generatedAnimation) { 
      previewAnimation(generatedAnimation.id);
    }
  };

  const handleOnChange = (parameter_key: string, e: any) => {
    setNewParameters((oldParams) => ({
      ...oldParams,
      [parameter_key]: e.target.value,
    }));
  };

  const handleUpdateParams = (e: MouseEvent) => {

  };

  const controlScreen = (
    <div>
      <p>Your animation should start playing on the tree shortly. You can stop and restart the animation using the controls below</p>
      <div className="flex justify-center gap-2 p-2">
        <Button color="red" onClick={handleStop}><StopIcon /></Button>
        <Button color="gray" onClick={handleRestart}><ReloadIcon /></Button>
      </div>
      <Separator my="3" size="4" />
      <form onSubmit={(e) => {e.preventDefault()}}>
      {Object.entries(generatedAnimation?.parameters_json || {}).map(([key, _]) => (
        <div className="pb-2" key={key}>
          <label>
            <div className="pb-1"><Text size="2" color="gray">{key}</Text></div>
          </label>
          <TextField.Input value={newParameters[key]} onChange={(e) => handleOnChange(key, e)}/>
        </div>
      ))}
      </form>
      <div className="flex justify-between pt-4">
        <div className="flex justify-start gap-2">
          <Button variant="soft" color="red" onClick={handleClose}>
            Cancel
          </Button>
          <Button variant="soft" color="gray" onClick={handleReset}>
            Restart
          </Button>
        </div>
        <div className="flex justify-end gap-2">
          <Button variant="soft" color="gray" onClick={handleUpdateParams}>
            Update
          </Button>
          <Button variant="soft" color="green" onClick={handleNext}>
            Next
          </Button>
        </div>
      </div>
    </div>
  );

  return hidden ? <></> : controlScreen;
};