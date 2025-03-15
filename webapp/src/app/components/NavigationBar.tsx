'use client';

import { SignedIn, UserButton } from '@clerk/nextjs';
import Link from 'next/link';
import { useState } from 'react';
import { AiOutlineClose } from 'react-icons/ai';
import { BiMenuAltRight } from 'react-icons/bi';
import ResponsiveContainer from './ResponsiveContainer';

const NavigationBar = () => {
  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => setMenuOpen((prev) => !prev);
  const closeMenu = () => setMenuOpen(false);

  return (
    <header className="bg-black-900 text-white fixed w-full z-50">
      <ResponsiveContainer>
        <div className="flex justify-between items-center h-16">
          <Link href="/">
            <h1
              className="text-2xl font-bold cursor-pointer"
              onClick={closeMenu}
            >
              RiseWell
            </h1>
          </Link>
          {/* DESKTOP NAV */}
          <nav className="hidden md:flex space-x-4 items-center">
            <Link
              href="/"
              className="px-4 py-2 rounded hover:bg-gray-700"
              onClick={closeMenu}
            >
              Home
            </Link>
            <Link
              href="/sleep-analytics"
              className="px-4 py-2 rounded hover:bg-gray-700"
              onClick={closeMenu}
            >
              Sleep Analytics
            </Link>
            <Link
              href="/wake-up-analytics"
              className="px-4 py-2 rounded hover:bg-gray-700"
              onClick={closeMenu}
            >
              Wake Up Analytics
            </Link>
            <SignedIn>
              <UserButton showName={false} />
            </SignedIn>
          </nav>
          {/* Menu Toggle */}
          <div className="md:hidden">
            <button onClick={toggleMenu} className="text-3xl text-white">
              {menuOpen ? <AiOutlineClose /> : <BiMenuAltRight />}
            </button>
          </div>
        </div>
      </ResponsiveContainer>
      {/* MOBILE NAV */}
      <nav
        className={`md:hidden fixed inset-0 bg-black-900 bg-opacity-90 backdrop-blur-sm flex flex-col justify-center items-center space-y-6 transform transition-transform duration-300 ${
          menuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <button
          onClick={closeMenu}
          className="absolute top-4 right-4 text-3xl text-white"
        >
          <AiOutlineClose />
        </button>
        <Link
          href="/"
          className="text-xl px-6 py-3 rounded hover:bg-gray-700"
          onClick={closeMenu}
        >
          Home
        </Link>
        <Link
          href="/sleep-analytics"
          className="text-xl px-6 py-3 rounded hover:bg-gray-700"
          onClick={closeMenu}
        >
          Sleep Analytics
        </Link>
        <Link
          href="/wake-up-analytics"
          className="text-xl px-6 py-3 rounded hover:bg-gray-700"
          onClick={closeMenu}
        >
          Wake Up Analytics
        </Link>
        <SignedIn>
          <UserButton showName={false} />
        </SignedIn>
      </nav>
    </header>
  );
};

export default NavigationBar;
