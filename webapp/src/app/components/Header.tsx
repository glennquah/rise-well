'use client';
import { motion } from 'framer-motion';

interface HeroSectionProps {
  name: string;
}

export default function HeroSection({
  name,
}: HeroSectionProps & {
  name: string;
}) {
  return (
    <section className="py-10 md:py-20">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center max-w-3xl mx-auto"
      >
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground">
          Welcome {name} to RiseWell
        </h1>
        <p className="mt-6 text-lg md:text-xl text-foreground/70">
          Enhance your sleep routine with smart tracking and gentle wake-ups
        </p>
      </motion.div>
    </section>
  );
}
