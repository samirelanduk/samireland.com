export const fetchRemoteData = async (path, fallback) => {
  try {
    const resp = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/${path}`);
    return await resp.json();;
  } catch (err) {
    console.log("There was error")
    if (process.env.NEXT_PUBLIC_ALLOW_FALLBACK === "true") {
      console.log("But we catch")
      return fallback;
    } else {
      console.log("NEXT_PUBLIC_ALLOW_FALLBACK:", process.env.NEXT_PUBLIC_ALLOW_FALLBACK)
      throw err;
    }
  }
}