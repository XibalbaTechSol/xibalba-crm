import React, { useRef, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';

const AudioOrb = () => {
    const meshRef = useRef<THREE.Mesh>(null);
    const [distort, setDistort] = React.useState(0);

    // Simulate audio reactivity
    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        // Create a pulsing effect simulating voice/audio
        const pulse = Math.sin(time * 3) * 0.2 + 0.3;

        // Random "voice" bursts
        const burst = Math.random() > 0.95 ? 0.4 : 0;

        const targetDistort = pulse + burst;

        // Smoothly interpolate to target
        setDistort(d => d + (targetDistort - d) * 0.1);

        if (meshRef.current) {
            meshRef.current.rotation.x = time * 0.2;
            meshRef.current.rotation.y = time * 0.3;
        }
    });

    return (
        <Sphere ref={meshRef} args={[1, 64, 64]} scale={2}>
            <MeshDistortMaterial
                color="#8a2be2" // Purple/Violet like Xibalba theme
                attach="material"
                distort={distort}
                speed={4}
                roughness={0.2}
                metalness={0.8}
            />
        </Sphere>
    );
};

const AIModulePage: React.FC = () => {
    return (
        <div style={{ height: 'calc(100vh - 60px)', display: 'flex', flexDirection: 'column' }}>
            <div style={{ padding: '2rem' }}>
                <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>AI Module: Audio Orb</h1>
                <p style={{ color: 'var(--text-muted)' }}>Interactive 3D visualization reacting to AI Voice.</p>
            </div>

            <div style={{ flex: 1, position: 'relative', width: '100%' }}>
                <Canvas>
                    <ambientLight intensity={0.5} />
                    <directionalLight position={[10, 10, 5]} intensity={1} />
                    <pointLight position={[-10, -10, -10]} intensity={0.5} />
                    <AudioOrb />
                </Canvas>
            </div>
        </div>
    );
};

export default AIModulePage;
