import { v4 as uuidv4 } from "uuid";
import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();
import { uploadToS3 } from "../utils/s3Upload.js";
import sharp from "sharp";
import axios from "axios";

const saveIdentity = async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ message: "No file uploaded" });
    }

    const resizedBuffer = await sharp(req.file.buffer)
      .resize(400, 400)
      .jpeg({ quality: 80 })
      .toBuffer();

    const uniqueFileName = `${uuidv4()}.jpeg`;

    // Step 1: Upload to S3
    const s3Url = await uploadToS3(resizedBuffer, uniqueFileName);
    //console.log("S3 URL:", s3Url);

    // Step 2: Get faissId from Python FIRST
    const aiResponse = await axios.post(`${process.env.AI_SERVICE_URL}/embed`, {
      identity_id: "temp",
      image_url: s3Url,
    });
    const faissId = aiResponse.data.faiss_id;

    // Step 3: Save to DB with real faissId
    const identity = await prisma.identity.create({
      data: {
        userId: req.user.id,
        faceImageUrl: s3Url,
        faissId: faissId,
      },
    });

    res.status(201).json({ message: "Identity saved successfully", identity });
  } catch (error) {
    res
      .status(500)
      .json({ message: "Couldn't save identity", error: error.message });
  }
};

export { saveIdentity };
