export default function handler(req, res) {
  if (req.method === "POST") {
    const { question } = req.body;
    res.status(200).json({ answer: `You asked: ${question}` });
  } else {
    res.status(405).json({ error: "Method Not Allowed" });
  }
}
