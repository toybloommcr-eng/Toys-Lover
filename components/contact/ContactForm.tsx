"use client";

import { useState } from "react";
import { Input, Select, Textarea } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";

export function ContactForm() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <form
        className="space-y-4 rounded-[1.75rem] bg-gradient-to-br from-[#E85D8C] via-[#FF8A3D] to-[#FFE566] p-[3px] shadow-[0_0_28px_rgba(232,93,140,0.45)]"
        onSubmit={(event) => {
          event.preventDefault();
          setOpen(true);
        }}
      >
        <div className="space-y-4 rounded-[1.6rem] bg-white p-6 sm:p-8">
          <h2 className="heading-glow font-display text-2xl font-extrabold text-[#E85D8C]">Write To The Floor Team</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <Input label="Name" name="name" required placeholder="Your name" />
            <Input label="Email" name="email" type="email" required placeholder="you@example.com" />
          </div>
          <Select label="Subject" name="subject" defaultValue="order">
            <option value="order">Order help</option>
            <option value="safety">Safety question</option>
            <option value="wholesale">Schools & wholesale</option>
            <option value="other">Something else</option>
          </Select>
          <Textarea
            label="Your note"
            name="message"
            required
            placeholder="How can we help?"
            className="min-h-[160px] border-2 border-[#E85D8C] bg-gradient-to-br from-coral-50 via-sun-50 to-white shadow-[0_0_18px_rgba(255,193,7,0.35)] focus:ring-[#E85D8C]/30"
          />
          <Button type="submit" size="lg" variant="buy">
            Send message
          </Button>
        </div>
      </form>
      <Modal open={open} onClose={() => setOpen(false)} title="Note received">
        <div className="rounded-2xl bg-gradient-to-r from-coral-50 via-sun-50 to-amber-50 p-4 ring-2 ring-coral-200">
          <p className="text-sm leading-relaxed text-ink-700">
            This is a frontend preview — nothing was emailed. In a live shop, the Manchester team
            would reply within one working day.
          </p>
        </div>
        <Button className="mt-5" variant="buy" onClick={() => setOpen(false)}>
          Close
        </Button>
      </Modal>
    </>
  );
}
