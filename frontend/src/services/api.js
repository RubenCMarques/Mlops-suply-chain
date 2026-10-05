export async function getSystemStatus(signal) {
  const response = await fetch('/api/v1/status', { signal });
  if (!response.ok) {
    throw new Error(`API request failed (${response.status})`);
  }
  return response.json();
}
