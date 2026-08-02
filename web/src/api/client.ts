/** Browser API client — paths must match backend OpenAPI / PR checklist. */

const JSON_HEADERS = { "Content-Type": "application/json" };

async function parse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = `${res.status}`;
    try {
      const body = await res.json();
      detail = body?.detail ?? detail;
    } catch {
      /* ignore */
    }
    throw new Error(String(detail));
  }
  return res.json() as Promise<T>;
}

export async function fetchHealth(): Promise<unknown> {
  const res = await fetch("/health");
  return parse(res);
}

export async function fetchCourses(): Promise<Array<{ id: string; title: string }>> {
  const res = await fetch("/api/v1/courses");
  return parse(res);
}

export interface TimelineCue {
  t_start: number;
  t_end: number;
  text: string;
}

export interface TimelineSlide {
  page: number;
  t_start: number;
  title: string;
  image_url?: string | null;
}

export interface TimelineResponse {
  course_id: string;
  status: string;
  duration_sec: number;
  cues: TimelineCue[];
  slides: TimelineSlide[];
  message?: string | null;
}

export interface AskResponse {
  course_id: string;
  answer: string;
  sources: string[];
}

export async function fetchTimeline(courseId: string): Promise<TimelineResponse> {
  const res = await fetch(`/api/v1/courses/${encodeURIComponent(courseId)}/timeline`);
  return parse(res);
}

export async function loadTimelineFromFixture(courseId: string): Promise<TimelineResponse> {
  const res = await fetch(
    `/api/v1/courses/${encodeURIComponent(courseId)}/timeline/from-fixture`,
    { method: "POST", headers: JSON_HEADERS },
  );
  return parse(res);
}

export async function askCourse(courseId: string, question: string): Promise<AskResponse> {
  const res = await fetch(`/api/v1/courses/${encodeURIComponent(courseId)}/ask`, {
    method: "POST",
    headers: JSON_HEADERS,
    body: JSON.stringify({ question }),
  });
  return parse(res);
}
