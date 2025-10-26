import React from 'react'
import Headerdash from './header'
import News from '../pages/News'
import Prism from './ui/Prism'

const MainDashboard = () => {
  return (
    <div
      style={{
        position: 'relative',
        width: '100%',
        minHeight: '100vh',
        overflow: 'hidden',
        backgroundColor: '#0a0a0a',
      }}
    >
      <Headerdash />
      {/* Background Prism Layer */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          zIndex: 0,
          pointerEvents: 'none',
        }}
      >
        <Prism
          animationType="rotate"
          timeScale={0.6}
          height={4.5}
          baseWidth={8}
          scale={1.5}
          glow={1.3}
          bloom={1.2}
          hueShift={0.5}
          colorFrequency={0.8}
          noise={0.15}
          transparent={true}
        />
      </div>

      {/* Foreground Content */}
      <div
        style={{
          position: 'relative',
          zIndex: 10, 
        }}
      >
        
        <News />
      </div>
    </div>
  )
}

export default MainDashboard
