const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL!;

export async function processDocuments(zipFile: File) {
  const formData = new FormData();
  formData.append("zip_file", zipFile);
  console.log(process.env.NEXT_PUBLIC_API_URL);
  const response = await fetch(`${API_BASE_URL}/api/extract`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Failed to process documents.");
  }

  return data;
}