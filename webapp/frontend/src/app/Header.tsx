"use client";

import { FC, useState } from "react";
import { PlusCircledIcon, HamburgerMenuIcon } from "@radix-ui/react-icons";
import { Code } from "@radix-ui/themes";
import { AlertDialog, Button } from "@radix-ui/themes";

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
      <div className="flex flex-col justify-center">
        <p className="leading-tight max-w-fit text-xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-rose-600 to-green-600">
            {title}
        </p>
        <p className="text-xs text-slate-200 text-center">
          Now Playing: <span> </span>
          <Code color="sky">{selectedAnimationName}</Code>
        </p>
      </div>
      <AlertDialog.Root>
      <AlertDialog.Trigger>
        <PlusCircledIcon height={25} width={25} color="white" />
      </AlertDialog.Trigger>
      <AlertDialog.Content style={{ maxWidth: 450 }}>
        <AlertDialog.Title>Coming Soon!</AlertDialog.Title>
        <AlertDialog.Description size="2">
          Check back soon for the ability to create custom animations!
        </AlertDialog.Description>

        <div className="flex justify-end gap-3 mt-4">
          <AlertDialog.Cancel>
            <Button variant="soft" color="green">
              Okay!
            </Button>
          </AlertDialog.Cancel>
        </div>
      </AlertDialog.Content>
    </AlertDialog.Root>
    </header>
  );
}