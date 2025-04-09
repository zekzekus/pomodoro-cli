import { v4 as uuidv4 } from "https://deno.land/std@0.95.0/uuid/mod.ts";
import { progress } from "@ryweal/progress";

type PomodoroSession = {
  id: string;
  workSessions: number;
  isWorkSession: boolean;
}

const SESSIONS_FILE = "./sessions.json";
const WORK_DURATION: number = 4;
const SHORT_REST_DURATION: number = 2;
const LONG_REST_DURAITON: number = 3;
const BASE_TIME: number = 1000; // seconds

/**
 * Loads the Pomodoro sessions from the sessions file.
 *
 * @returns A promise that resolves to a record of Pomodoro sessions, where each session is identified by a unique string ID.
 * If the sessions file cannot be read or parsed, it returns an empty record.
 */
async function loadSessions():
  Promise<Record<string, PomodoroSession>> {
  try {
    const data = await Deno.readTextFile(SESSIONS_FILE);
    return JSON.parse(data);
  } catch {
    return {};
  }
}

/**
 * Saves the Pomodoro sessions to the sessions file.
 *
 * @param sessions - A record of Pomodoro sessions, where each session is identified by a unique string ID.
 *
 * @returns A promise that resolves when the sessions have been successfully written to the file.
 * If the file cannot be written, the promise will be rejected with an error.
 */
async function saveSessions(sessions: Record<string, PomodoroSession>) {
  await Deno.writeTextFile(SESSIONS_FILE, JSON.stringify(sessions));
}

/**
 * Handles the progress of a session by updating the progress bar at regular intervals.
 *
 * @param duration - The duration for which the progress should be tracked, in seconds.
 * @param p - The progress bar instance to be updated.
 *
 * @returns A promise that resolves when the duration has elapsed.
 */
// deno-lint-ignore no-explicit-any
async function handleProgress(duration: number, p: any): Promise<void> {
  await new Promise<void>((resolve) => {
    const interval = setInterval(() => {
      p.next();
      duration--;
      if (duration <= 0) {
        clearInterval(interval);
        resolve();
      }
    }, BASE_TIME);
  });
}

export async function startPomodoro(id?: string) {
  const sessions = await loadSessions();
  if (!id || !sessions[id]) {
    id = uuidv4.generate();
    sessions[id] = { id, workSessions: 0, isWorkSession: true };
  }

  const session = sessions[id];
  const duration = session.isWorkSession
    ? WORK_DURATION
    : (session.workSessions % 4 === 0 ? LONG_REST_DURAITON : SHORT_REST_DURATION);

  console.log(`Session ID: ${id}`);
  console.log(`Starting ${session.isWorkSession ? "work" : "break"} session for ${duration} seconds...`);
  const p = progress("Progress: [[bar]]", { total: duration});

  handleProgress(duration, p);

  if (session.isWorkSession) {
    session.workSessions++;
  }
  session.isWorkSession = !session.isWorkSession;

  console.log(`Session ID: ${id}, Work sessions: ${session.workSessions}`);

  await saveSessions(sessions);

}
