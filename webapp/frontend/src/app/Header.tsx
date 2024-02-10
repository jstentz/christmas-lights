"use client";

import { FC, useState } from "react";

type Props = {
  title: string,
};

export const Header: FC<Props> = ({
  title
}) => {
  const [isSearching, setIsSearching] = useState(false);
  
  const searchBox = 
    <input
      type="text"
      placeholder="Search for animation..."
      className="px-3 py-1 mr-2 rounded-md bg-gray-700 text-white focus:outline-none"
    />
  return (
    <header className="bg-gray-800 p-4 flex justify-between items-center fixed w-full top-0 z-10">
      <h1 className="text-white text-lg font-bold">{title}</h1>
      <div className="flex items-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6 text-white cursor-pointer"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M10 21l-2-2m0 0l-2-2m2 2l2-2m-2 2l2 2m7-10a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>
    </header>
  );
}