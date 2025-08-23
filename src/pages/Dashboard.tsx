import React from 'react';
import { useGodmodeStore } from '../store/godmodeStore';
import Header from '../components/layout/Header';
import NormalMode from '../components/dashboard/NormalMode';
import GlobeView from '../components/globe/GlobeView';

const Dashboard: React.FC = () => {
  const { isActive } = useGodmodeStore();

  return (
    <div className="h-screen flex flex-col">
      {isActive ? (
        <GlobeView />
      ) : (
        <>
          <Header />
          <main className="flex-1 overflow-hidden">
            <NormalMode />
          </main>
        </>
      )}
    </div>
  );
};

export default Dashboard;
