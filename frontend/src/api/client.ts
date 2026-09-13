const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
const getCache = new Map<string, Promise<unknown>>();

export async function apiGet<T>(path: string): Promise<T> {
  const url = `${API_BASE_URL}${path}`;
  if (!getCache.has(url)) {
    getCache.set(
      url,
      fetch(url).then((response) => {
        if (!response.ok) {
          throw new Error(`Request failed: ${response.status}`);
        }
        return response.json();
      })
    );
  }
  return getCache.get(url) as Promise<T>;
}

export async function apiPostCsv(path: string): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}${path}`, { method: "POST" });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.blob();
}
