import React from 'react';
import TrinityNav from '../components/TrinityNav';

// This component wraps the entire Docusaurus application.
export default function Root({children}: {children: React.ReactNode}) {
  return (
    <>
      <TrinityNav />
      {children}
    </>
  );
}
