import React from 'react'
import SplitText from '../text-animations/SplitText'


const Headerdash = () => {
  return (
    <h1 style={{ fontSize: '2rem', lineHeight: '1', textAlign:'center' }}>
        <SplitText
        text="Kaonewz"
        className="font-bold text-center text-white"
        delay={100}
        duration={0.6}
        ease="power3.out"
        splitType="chars"
        from={{ opacity: 0, y: 40 }}
        to={{ opacity: 1, y: 0 }}
        threshold={0.1}
        rootMargin="-100px"
        />
    </h1>
  )
}

export default Headerdash