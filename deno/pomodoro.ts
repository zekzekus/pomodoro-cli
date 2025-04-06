import { v4 as uuidv4 } from "https://deno.land/std@0.95.0/uuid/mod.ts";

type PomodoroSession = {
  id: string;
  workSessions: number;
  isWorkSession: boolean;
}

const SESSIONS_FILE = "./sessions.json";
const WORK_DURATION: number = 4;
const SHORT_REST_DURATION: number = 2;
const _LONG_REST_DURAITON: number = 3;

async function loadSessions():
  Promise<Record<string, PomodoroSession>> {
  try {
    const data = await Deno.readTextFile(SESSIONS_FILE);
    return JSON.parse(data);
  } catch {
    return {};
  }
}

async function saveSessions(sessions: Record<string, PomodoroSession>) {
  await Deno.writeTextFile(SESSIONS_FILE, JSON.stringify(sessions));
}

export async function startPomodoro(id?: string) {
  const sessions = await loadSessions();
  if (!id || !sessions[id]) {
    id = uuidv4.generate();
    sessions[id] = { id, workSessions: 0, isWorkSession: true };
  }

  const session = sessions[id];
  const duration = session.isWorkSession ? WORK_DURATION : SHORT_REST_DURATION;

  console.log(`Session ID: ${id}`);
  console.log(`Starting ${session.isWorkSession ? "work" : "break"} session for ${duration} seconds...`);

  await new Promise((resolve) => setTimeout(resolve, duration * 1000));

  if (session.isWorkSession) {
    session.workSessions++;
  }
  session.isWorkSession = !session.isWorkSession;

  console.log(`Session ID: ${id}, Work sessions: ${session.workSessions}`);

  await saveSessions(sessions);

}
