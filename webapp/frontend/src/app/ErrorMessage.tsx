"use client";

import { useBackend } from "@/hooks/backend";

const ErrorMessage = (props: any) => {
    const {status, clearStatus} = useBackend();

    const {message, error} = status;

    return (
      <div className="z-10 fixed left-1/2 transform -translate-x-1/2 shadow-lg bg-red-400 rounded-lg p-4 max-w-screen-sm" hidden={!error}>
        <div className="absolute top-0 right-0">
          <button onClick={clearStatus}>
            <svg className="fill-current w-6 h-6 text-slate-800" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5.293 5.293a1 1 0 0 1 1.414 0L10 8.586l3.293-3.293a1 1 0 1 1 1.414 1.414L11.414 10l3.293 3.293a1 1 0 0 1-1.414 1.414L10 11.414l-3.293 3.293a1 1 0 0 1-1.414-1.414L8.586 10 5.293 6.707a1 1 0 0 1 0-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
        <p className="text-slate-800 font-semibold">{message}</p>
      </div>
    )
}

export default ErrorMessage;