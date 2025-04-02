'use client';

import Image from 'next/image';
import Header from './Header';
import ContentContainer from './ContentContainer';

const Layout = ({ children }) => {
  return (
    <div className="relative w-full h-screen overflow-hidden">
      <Image
        src="/images/bg.png"
        alt="Farm background"
        fill
        priority
        className="object-cover z-[-1]"
      />
      <Header />
      <main className="pt-[70px] h-full relative">
        <ContentContainer>
          {children}
        </ContentContainer>
      </main>
    </div>
  );
};

export default Layout;