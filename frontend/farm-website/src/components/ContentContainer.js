'use client';

const ContentContainer = ({ children }) => {
  return (
    <div className="absolute top-1/2 right-[5%] transform -translate-y-1/2 w-[55%] h-[80%] bg-white/80 rounded-2xl backdrop-blur-sm p-8 overflow-scroll shadow-content flex flex-col">
      {children}
    </div>
  );
};

export default ContentContainer;