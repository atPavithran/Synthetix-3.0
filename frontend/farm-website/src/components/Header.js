'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const Header = () => {
  const pathname = usePathname();

  return (
    <header className="fixed top-0 left-0 w-full h-[70px] bg-black/70 flex items-center justify-between px-10 z-50">
      <div className="text-white text-2xl font-bold">Farm Management</div>
      <nav className="flex gap-8">
        <Link 
          href="/" 
          className={`text-lg transition-colors ${
            pathname === '/' ? 'text-green-400 font-bold' : 'text-white hover:text-green-400'
          }`}
        >
          Home
        </Link>
        <Link 
          href="/second-page" 
          className={`text-lg transition-colors ${
            pathname === '/second-page' ? 'text-green-400 font-bold' : 'text-white hover:text-green-400'
          }`}
        >
          Dashboard
        </Link>
        <Link 
          href="/third-page" 
          className={`text-lg transition-colors ${
            pathname === '/third-page' ? 'text-green-400 font-bold' : 'text-white hover:text-green-400'
          }`}
        >
          Visual
        </Link>
      </nav>
    </header>
  );
};

export default Header;