"use client";

import { useAppDispatch, useAppSelector } from "@/hooks/hooks";
import { clearError, selectError } from "@/reducers/animationsReducer";
import { Cross2Icon } from "@radix-ui/react-icons";

const ErrorMessage = (props: any) => {
  const dispatch = useAppDispatch();
  const error = useAppSelector(selectError);

  return (
    <div className="z-10 fixed left-1/2 transform -translate-x-1/2 shadow-lg bg-red-400 rounded-lg p-4 max-w-screen-sm" hidden={!error}>
      <div className="absolute top-0 right-0 p-1">
        <button onClick={() => dispatch(clearError())}>
          <Cross2Icon width="20" height="20" />
        </button>
      </div>
      <p className="text-slate-800 font-semibold">{error}</p>
    </div>
  )
}

export default ErrorMessage;