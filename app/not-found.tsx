import { SITE_NAME } from "@/lib/constants";
import { Button } from "@/components/ui/Button";
import { Container } from "@/components/ui/Container";

export default function NotFound() {
  return (
    <Container className="py-24 text-center">
      <p className="text-xs font-bold uppercase tracking-[0.2em] text-coral-600">404</p>
      <h1 className="heading-glow mt-3 font-display text-4xl font-extrabold text-ink-900">
        That Toy Wandered Off.
      </h1>
      <p className="mx-auto mt-3 max-w-md text-ink-500">
        The page is missing, but {SITE_NAME} still has a shelf full of better ideas.
      </p>
      <div className="mt-8 flex justify-center gap-3">
        <Button href="/">Home</Button>
        <Button href="/shop" variant="outline">
          Shop
        </Button>
      </div>
    </Container>
  );
}
