import './globals.css';

export const metadata = {
  title: 'Farm Management App',
  description: 'A modern farm management application',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className='overflow-hidden'>
        {children}
      </body>
    </html>
  );
}