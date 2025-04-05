import { startPomodoro } from "./pomodoro.ts";

if (import.meta.main) {
  const args = Deno.args;
  const id = args[0];
  await startPomodoro(id);
}
