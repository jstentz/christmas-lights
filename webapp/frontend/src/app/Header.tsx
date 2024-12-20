"use client";

import { FC, useState } from "react";
import { PlusCircledIcon, HamburgerMenuIcon } from "@radix-ui/react-icons";
import { Code } from "@radix-ui/themes";
import { AlertDialog, Button } from "@radix-ui/themes";
import { CreateAnimationWizard } from "./CreateAnimationWizard";

type Props = {
  title: string,
  selectedAnimationName: string,
};

export const Header: FC<Props> = ({
  title,
  selectedAnimationName
}) => {
  return (
    <header className="bg-gray-800 p-2 pr-4 pl-4 flex justify-between items-center fixed w-full top-0 z-10">
      <HamburgerMenuIcon height={25} width={25} color="white" />
      <div className="flex flex-col justify-center items-center">
        <p className="leading-tight max-w-fit text-xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-rose-600 to-green-600">
            {title}
        </p>
        <p className="text-xs text-slate-200 text-center">
          Now Playing: <span> </span>
          <Code color="teal">{selectedAnimationName}</Code>
        </p>
      </div>

      <CreateAnimationWizard />
    </header>
  );
}