
import { GoogleGenAI, Type } from "@google/genai";
import { BuildingDetection } from "../types";

export class GeminiService {
  private ai: GoogleGenAI;

  constructor() {
    this.ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });
  }

  private async fileToPart(file: File): Promise<{ inlineData: { data: string; mimeType: string } }> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64Data = (reader.result as string).split(",")[1];
        resolve({
          inlineData: {
            data: base64Data,
            mimeType: file.type,
          },
        });
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  async detectNewConstructions(baseline: File, current: File): Promise<BuildingDetection[]> {
    const baselinePart = await this.fileToPart(baseline);
    const currentPart = await this.fileToPart(current);

    const prompt = `Analyze these two satellite images of the same geographic area in Azerbaijan. 
    Image 1 is the baseline (older). Image 2 is the current status.
    Task: Identify all NEW buildings or significant structures present in Image 2 that were NOT present in Image 1.
    Return only the detections for NEW buildings as a JSON array.
    Each detection must include a normalized bounding box [ymin, xmin, ymax, xmax] ranging from 0 to 1000.`;

    const response = await this.ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: {
        parts: [
          { text: prompt },
          baselinePart,
          currentPart
        ],
      },
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.ARRAY,
          items: {
            type: Type.OBJECT,
            properties: {
              bbox: {
                type: Type.ARRAY,
                items: { type: Type.NUMBER },
                description: "[ymin, xmin, ymax, xmax] normalized 0-1000"
              },
              confidence: { type: Type.NUMBER },
              id: { type: Type.STRING }
            },
            required: ["bbox", "confidence", "id"]
          }
        }
      }
    });

    try {
      const detections = JSON.parse(response.text || "[]");
      return detections.map((d: any) => ({
        ...d,
        isNew: true
      }));
    } catch (e) {
      console.error("Failed to parse Gemini response:", e);
      return [];
    }
  }
}

export const geminiService = new GeminiService();
