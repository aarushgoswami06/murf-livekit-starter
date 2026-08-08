import { Button } from '@/components/ui/button';

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
}: WelcomeViewProps) => {
  return (
    <div className="flex min-h-screen w-full items-center justify-center px-6">
      <section className="flex w-full max-w-xl flex-col items-center text-center">
        <p className="mb-3 text-sm font-medium tracking-widest text-indigo-500 uppercase">
          TechFlow Support
        </p>

        <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
          Meet Suchi
        </h1>

        <p className="mt-4 max-w-md text-base leading-7 text-muted-foreground md:text-lg">
          Your AI support assistant for account, billing, and product help.
        </p>

        <p className="mt-2 text-sm text-muted-foreground">
          Hindi, English, or Hinglish — baat kijiye naturally.
        </p>

        <Button
          size="lg"
          onClick={onStartCall}
          className="mt-8 w-64 rounded-full font-semibold"
        >
          {startButtonText}
        </Button>

        <p className="mt-4 text-xs text-muted-foreground">
          Click the button and allow microphone access to start.
        </p>
      </section>
    </div>
  );
};