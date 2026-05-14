export async function fetchHealth(): Promise<unknown> {
  const res = await fetch("/health");
  if (!res.ok) throw new Error(`health ${res.status}`);
  return res.json();
}

export async function fetchCourses(): Promise<Array<{ id: string; title: string }>> {
  const res = await fetch("/api/v1/courses");
  if (!res.ok) throw new Error(`courses ${res.status}`);
  return res.json();
}
